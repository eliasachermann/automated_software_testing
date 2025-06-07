from sqlglot import parse, parse_one
from sqlglot.errors import ParseError
from sqlglot import parse, exp
from sqlglot.optimizer.simplify import simplify
import argparse
import subprocess
import sys
import os
import copy



def delta_debug_node(node, test_script, full_statements, stmt_index):
    if not hasattr(node, 'args') or not node.args:
        return node

    if isinstance(node.args, dict):
        children = [(k, v) for k, v in node.args.items() if v is not None]
    elif isinstance(node.args, list):
        children = [(i, v) for i, v in enumerate(node.args) if v is not None]
    else:
        return node

    if len(children) <= 1:
        if children and hasattr(children[0][1], 'args'):
            reduced_child = delta_debug_node(children[0][1], test_script, full_statements, stmt_index)
            if reduced_child != children[0][1]:
                new_node = copy.deepcopy(node)
                if isinstance(node.args, dict):
                    new_args = dict(node.args)
                    new_args[children[0][0]] = reduced_child
                    new_node.set("args", new_args)
                else:
                    new_args = list(node.args)
                    new_args[children[0][0]] = reduced_child
                    new_node.set("args", new_args)
                new_node = simplify_expression(new_node)
                test_statements = full_statements.copy()
                test_statements[stmt_index] = new_node
                try:
                    sql = ";\n".join(stmt.sql(pretty=False) for stmt in test_statements) + ";"
                    if test_query(sql, test_script):
                        return new_node
                except Exception:
                    pass
        return node

    n = len(children)
    subset_size = n // 2

    while subset_size >= 1:
        for i in range(0, n, subset_size):
            remove_idxs = set(range(i, min(i + subset_size, n)))
            kept_children = [c for j, c in enumerate(children) if j not in remove_idxs]
            if not kept_children:
                continue
            new_node = copy.deepcopy(node)
            if isinstance(node.args, dict):
                new_node.args = {k: v for k, v in kept_children}
            else:
                new_node.args = [v for _, v in kept_children]
            new_node = simplify_expression(new_node)
            test_statements = full_statements.copy()
            test_statements[stmt_index] = new_node
            try:
                sql = ";\n".join(stmt.sql(pretty=False) for stmt in test_statements) + ";"
                if test_query(sql, test_script):
                    return delta_debug_node(new_node, test_script, test_statements, stmt_index)
            except Exception:
                continue
        subset_size //= 2

    for i, (k, v) in enumerate(children):
        if hasattr(v, 'args'):
            reduced = delta_debug_node(v, test_script, full_statements, stmt_index)
            if reduced != v:
                new_node = copy.deepcopy(node)
                if isinstance(node.args, dict):
                    new_node.args[k] = reduced
                else:
                    new_node.args[k] = reduced
                new_node = simplify_expression(new_node)
                test_statements = full_statements.copy()
                test_statements[stmt_index] = new_node
                try:
                    sql = ";\n".join(stmt.sql(pretty=False) for stmt in test_statements) + ";"
                    if test_query(sql, test_script):
                        return new_node
                except Exception:
                    continue

    return node

def delta_debug_statements(statements, test_script):
    statements = [simplify_expression(s) for s in statements]
    if len(statements) <= 1:
        if statements:
            reduced_stmt = delta_debug_node(statements[0], test_script, statements, 0)
            return [reduced_stmt]
        return statements

    n = len(statements)
    subset_size = n // 2

    while subset_size >= 1:
        for i in range(0, n, subset_size):
            remove_idxs = set(range(i, min(i + subset_size, n)))
            remaining = [statements[j] for j in range(n) if j not in remove_idxs]
            if not remaining:
                continue
            try:
                sql = ";\n".join(stmt.sql(pretty=False) for stmt in remaining) + ";"
                if test_query(sql, test_script):
                    return delta_debug_statements(remaining, test_script)
            except Exception:
                continue
        subset_size //= 2

    for i, stmt in enumerate(statements):
        reduced = delta_debug_node(stmt, test_script, statements, i)
        if reduced != stmt:
            new_statements = statements.copy()
            new_statements[i] = reduced
            try:
                sql = ";\n".join(s.sql(pretty=False) for s in new_statements) + ";"
                if test_query(sql, test_script):
                    return new_statements
            except Exception:
                continue

    return statements

def reduce_sql_query(sql_query: str, test_script: str) -> str:
    try:
        parsed_statements = parse(sql_query, error_level="ignore")
        if not parsed_statements:
            return sql_query
    except Exception as e:
        print(f"Parse error: {e}")
        return sql_query

    if not test_query(sql_query, test_script):
        print("Original query does not trigger bug.")
        return sql_query

    reduced_statements = delta_debug_statements(parsed_statements, test_script)
    reduced_sql = ";\n".join(stmt.sql(pretty=False) for stmt in reduced_statements) + ";"
    return reduced_sql

def simplify_expression(node):
    if isinstance(node, exp.Expression):
        items = list(node.args.items())
        for k, v in items:
            if isinstance(v, list):
                node.set(k, [simplify_expression(child) for child in v])
            elif isinstance(v, exp.Expression):
                node.set(k, simplify_expression(v))

        simplified = simplify(node)
        if isinstance(simplified, exp.Expression):
            return simplified

    return node

def test_query(query: str, test_script: str) -> bool:    
    try:

        test_case_location = os.environ.get('TEST_CASE_LOCATION')
        if not test_case_location:
            test_case_location = os.path.join(os.getcwd(), "query.sql")

        with open(test_case_location, 'w') as f:
            f.write(query)

        result = subprocess.run(['bash', test_script], capture_output=True, text=True, timeout=30, env=os.environ.copy())
        
        # print(f"Test script stdout: {result.stdout}")
        # print(f"Test script stderr: {result.stderr}")

        return_code = result.returncode

        return return_code == 0
        
    except subprocess.TimeoutExpired:
        print("Test script timed out")
        return False
    except Exception as e:
        print(f"Error running test script: {e}")
        return False
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--test", required=True)
    
    args = parser.parse_args()

    try:
        with open(args.query, 'r') as f:
            sql_query = f.read().strip()
    except Exception as e:
        print(f"Error reading query file: {e}")
        sys.exit(1)
    
    print(f"Original query length: {len(sql_query)} characters")
    print(f"Original query: \n{sql_query}")
    reduced_query = reduce_sql_query(sql_query, args.test)
    test_case_location = os.environ.get('TEST_CASE_LOCATION')
    if not test_case_location:
        test_case_location = os.path.join(os.getcwd(), "query.sql")

    with open(test_case_location, 'w') as f:
        f.write(reduced_query)

    print(f"Reduced query length: {len(reduced_query)} characters")
    print(reduced_query)