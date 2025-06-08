import sqlglot
import ast
import argparse
import subprocess
import sys
import os
import copy
import time
from sqlglot import parse, parse_one
from sqlglot.errors import ParseError
from sqlglot import parse, exp
from sqlglot.optimizer.simplify import simplify
from sqlglot.optimizer import optimize
from sqlglot.expressions import Expression, Select, Insert, Where, Values

def evaluate_arithmetic_expr(expr: Expression) -> Expression:
    if isinstance(expr, exp.Literal):
        return expr
    
    if isinstance(expr, exp.Boolean):
        return expr
    
    if isinstance(expr, exp.Null):
        return expr
    
    if isinstance(expr, exp.Binary):
        left = evaluate_arithmetic_expr(expr.left)
        right = evaluate_arithmetic_expr(expr.right)
        
        if isinstance(expr, exp.NEQ):
            if isinstance(left, exp.Boolean) and isinstance(right, exp.Boolean):
                result = left.this != right.this
                return exp.Boolean(this=result)
            elif isinstance(left, exp.Paren) and isinstance(left.this, exp.Boolean) and isinstance(right, exp.Paren) and isinstance(right.this, exp.Boolean):
                result = left.this.this != right.this.this
                return exp.Boolean(this=result)
        elif isinstance(expr, exp.EQ):
            if isinstance(left, exp.Boolean) and isinstance(right, exp.Boolean):
                result = left.this == right.this
                return exp.Boolean(this=result)
            elif isinstance(left, exp.Paren) and isinstance(left.this, exp.Boolean) and isinstance(right, exp.Paren) and isinstance(right.this, exp.Boolean):
                result = left.this.this == right.this.this
                return exp.Boolean(this=result)
            
            if isinstance(left, exp.Literal) and isinstance(right, exp.Boolean):
                try:
                    left_val = float(left.this) if '.' in str(left.this) else int(left.this)
                    right_val = 1 if right.this else 0
                    result = (left_val == right_val)
                    return exp.Boolean(this=result)
                except:
                    pass
            elif isinstance(right, exp.Literal) and isinstance(left, exp.Boolean):
                try:
                    right_val = float(right.this) if '.' in str(right.this) else int(right.this)
                    left_val = 1 if left.this else 0
                    result = (left_val == right_val)
                    return exp.Boolean(this=result)
                except:
                    pass
        
        left_val = None
        right_val = None
        
        if isinstance(left, exp.Literal):
            left_val = left.this
            if isinstance(left_val, str):
                try:
                    left_val = float(left_val) if '.' in left_val else int(left_val)
                except ValueError:
                    left_val = None
        elif isinstance(left, exp.Paren) and isinstance(left.this, exp.Literal):
            left_val = left.this.this
            if isinstance(left_val, str):
                try:
                    left_val = float(left_val) if '.' in left_val else int(left_val)
                except ValueError:
                    left_val = None
        elif isinstance(left, exp.Neg) and isinstance(left.this, (exp.Literal, exp.Paren)):
            inner = left.this
            if isinstance(inner, exp.Paren):
                inner = inner.this
            if isinstance(inner, exp.Literal):
                try:
                    val = inner.this
                    if isinstance(val, str):
                        val = float(val) if '.' in val else int(val)
                    left_val = -val
                except (ValueError, TypeError):
                    left_val = None
        
        if isinstance(right, exp.Literal):
            right_val = right.this
            if isinstance(right_val, str):
                try:
                    right_val = float(right_val) if '.' in right_val else int(right_val)
                except ValueError:
                    right_val = None
        elif isinstance(right, exp.Paren) and isinstance(right.this, exp.Literal):
            right_val = right.this.this
            if isinstance(right_val, str):
                try:
                    right_val = float(right_val) if '.' in right_val else int(right_val)
                except ValueError:
                    right_val = None
        elif isinstance(right, exp.Neg) and isinstance(right.this, (exp.Literal, exp.Paren)):
            inner = right.this
            if isinstance(inner, exp.Paren):
                inner = inner.this
            if isinstance(inner, exp.Literal):
                try:
                    val = inner.this
                    if isinstance(val, str):
                        val = float(val) if '.' in val else int(val)
                    right_val = -val
                except (ValueError, TypeError):
                    right_val = None
        
        if left_val is not None and right_val is not None:
            try:
                result = None
                if isinstance(expr, exp.Add):
                    result = left_val + right_val
                elif isinstance(expr, exp.Sub):
                    result = left_val - right_val
                elif isinstance(expr, exp.Mul):
                    result = left_val * right_val
                elif isinstance(expr, exp.Div):
                    if right_val != 0:
                        result = left_val / right_val
                elif isinstance(expr, exp.EQ):
                    result = left_val == right_val
                elif isinstance(expr, exp.NEQ):
                    result = left_val != right_val
                elif isinstance(expr, exp.LT):
                    result = left_val < right_val
                elif isinstance(expr, exp.GT):
                    result = left_val > right_val
                elif isinstance(expr, exp.LTE):
                    result = left_val <= right_val
                elif isinstance(expr, exp.GTE):
                    result = left_val >= right_val
                
                if result is not None:
                    if isinstance(result, bool):
                        return exp.Boolean(this=result)
                    elif isinstance(result, (int, float)):
                        return exp.Literal.number(str(result))
                        
            except (ZeroDivisionError, TypeError, ValueError):
                pass
        
        new_expr = copy.deepcopy(expr)
        new_expr.set("left", left)
        new_expr.set("right", right)
        return new_expr
    
    if isinstance(expr, exp.Unary):
        operand = evaluate_arithmetic_expr(expr.this)
        
        if isinstance(operand, exp.Literal):
            try:
                val = operand.this
                if isinstance(val, str):
                    try:
                        val = float(val) if '.' in val else int(val)
                    except ValueError:
                        pass
                
                if isinstance(expr, exp.Neg):
                    result = -val
                    return exp.Literal.number(str(result))
            except (TypeError, ValueError):
                pass
        
        if isinstance(expr, exp.Not):
            if isinstance(operand, exp.Boolean):
                result = not operand.this
                return exp.Boolean(this=result)
        
        new_expr = copy.deepcopy(expr)
        new_expr.set("this", operand)
        return new_expr
    
    if isinstance(expr, exp.Paren):
        inner = evaluate_arithmetic_expr(expr.this)
        if isinstance(inner, (exp.Literal, exp.Boolean)):
            return inner
        new_expr = copy.deepcopy(expr)
        new_expr.set("this", inner)
        return new_expr
    
    return expr

def simplify_where_clause(where_expr: Expression) -> Expression:
    if where_expr is None:
        return None
    
    simplified = where_expr.this
    max_passes = 20
    
    for pass_num in range(max_passes):
        old_simplified = simplified
        new_simplified = evaluate_arithmetic_expr(simplified)
        
        if new_simplified == simplified:
            break
        
        if pass_num > 0 and new_simplified == old_simplified:
            break
            
        simplified = new_simplified
    
    if simplified != where_expr.this:
        new_where = copy.deepcopy(where_expr)
        new_where.set("this", simplified)
        return new_where
    
    return where_expr

def simplify_statement(stmt: Expression) -> Expression:
    if isinstance(stmt, Insert):
        select_expr = stmt.args.get("expression")
        if isinstance(select_expr, Select):
            where_expr = select_expr.args.get("where")
            if where_expr is not None:
                simplified_where = simplify_where_clause(where_expr)
                if simplified_where != where_expr:
                    new_stmt = copy.deepcopy(stmt)
                    new_select = copy.deepcopy(select_expr)
                    new_select.set("where", simplified_where)
                    new_stmt.set("expression", new_select)
                    return new_stmt
    
    elif isinstance(stmt, Select):
        where_expr = stmt.args.get("where")
        if where_expr is not None:
            simplified_where = simplify_where_clause(where_expr)
            if simplified_where != where_expr:
                new_stmt = copy.deepcopy(stmt)
                new_stmt.set("where", simplified_where)
                return new_stmt
    
    return stmt

def simplify_sql_constants(parsed_statements: list[Expression]) -> list[Expression]:
    simplified_statements = []
    for stmt in parsed_statements:
        simplified = simplify_statement(stmt)
        simplified_statements.append(simplified)
    
    return simplified_statements

def reduce_statements_aggressively(statements, test_script):
    if len(statements) <= 1:
        return statements
    
    filtered = [s for s in statements if not isinstance(s, (exp.Transaction, exp.Commit))]
    if len(filtered) < len(statements):
        try:
            sql = ";\n".join(stmt.sql(normalize=True, pad=0) for stmt in filtered) + ";"
            if test_query(sql, test_script):
                return reduce_statements_aggressively(filtered, test_script)
        except Exception:
            pass
    
    filtered = [s for s in statements if not isinstance(s, (exp.Update, exp.Delete))]
    if len(filtered) < len(statements):
        try:
            sql = ";\n".join(stmt.sql(normalize=True, pad=0) for stmt in filtered) + ";"
            if test_query(sql, test_script):
                return reduce_statements_aggressively(filtered, test_script)
        except Exception:
            pass
    
    essential = [s for s in statements if isinstance(s, (exp.Create, exp.Insert, exp.Select))]
    if len(essential) < len(statements) and essential:
        try:
            sql = ";\n".join(stmt.sql(normalize=True, pad=0) for stmt in essential) + ";"
            if test_query(sql, test_script):
                return reduce_statements_aggressively(essential, test_script)
        except Exception:
            pass
    
    filtered = [s for s in statements if not (hasattr(s, 'kind') and s.kind in ['VIEW', 'INDEX', 'TRIGGER'])]
    if len(filtered) < len(statements):
        try:
            sql = ";\n".join(stmt.sql(normalize=True, pad=0) for stmt in filtered) + ";"
            if test_query(sql, test_script):
                return reduce_statements_aggressively(filtered, test_script)
        except Exception:
            pass
    
    inserts = [s for s in statements if isinstance(s, exp.Insert)]
    if len(inserts) > 1:
        non_inserts = [s for s in statements if not isinstance(s, exp.Insert)]
        for single_insert in inserts:
            test_statements = non_inserts + [single_insert]
            try:
                sql = ";\n".join(stmt.sql(normalize=True, pad=0) for stmt in test_statements) + ";"
                if test_query(sql, test_script):
                    return reduce_statements_aggressively(test_statements, test_script)
            except Exception:
                continue
    
    return statements

def test_reduced_node(node, test_script, full_statements, stmt_index):
    test_statements = full_statements.copy()
    test_statements[stmt_index] = node
    try:
        sql = ";\n".join(stmt.sql(normalize=True, pad=0) for stmt in test_statements) + ";"
        result = test_query(sql, test_script)
        return result
    except Exception:
        return False

def reduce_create_table(node, test_script, full_statements, stmt_index):
    if not isinstance(node, exp.Create) or node.args.get('kind') != 'TABLE':
        return node
    
    if node.args.get('exists'):
        test_node = copy.deepcopy(node)
        test_node.set('exists', None)
        if test_reduced_node(test_node, test_script, full_statements, stmt_index):
            node = test_node
    
    if node.args.get('this') and hasattr(node.args['this'], 'expressions'):
        columns = node.args['this'].expressions
        for i, col in enumerate(columns):
            if hasattr(col, 'args') and col.args.get('constraints'):
                constraints = col.args['constraints']
                if len(constraints) > 1:
                    test_node = copy.deepcopy(node)
                    test_columns = list(columns)
                    test_col = copy.deepcopy(col)
                    test_col.set('constraints', constraints[:1])
                    test_columns[i] = test_col
                    test_node.args['this'].set('expressions', test_columns)
                    if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                        node = test_node
                        columns = test_columns
                
                test_node = copy.deepcopy(node)
                test_columns = list(columns)
                test_col = copy.deepcopy(col)
                test_col.set('constraints', [])
                test_columns[i] = test_col
                test_node.args['this'].set('expressions', test_columns)
                if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                    node = test_node
                    columns = test_columns
            
            if hasattr(col, 'args') and col.args.get('kind'):
                test_node = copy.deepcopy(node)
                test_columns = list(columns)
                test_col = copy.deepcopy(col)
                test_col.set('kind', None)
                test_columns[i] = test_col
                test_node.args['this'].set('expressions', test_columns)
                if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                    node = test_node
                    columns = test_columns
    
    return node

def reduce_insert_values(node, test_script, full_statements, stmt_index):
    if not isinstance(node, exp.Insert):
        return node
    
    if hasattr(node, 'args') and node.args.get('alternative'):
        test_node = copy.deepcopy(node)
        test_node.set('alternative', None)
        if test_reduced_node(test_node, test_script, full_statements, stmt_index):
            node = test_node
    
    if node.args.get('expression') and hasattr(node.args['expression'], 'expressions'):
        values_list = node.args['expression'].expressions
        if len(values_list) > 1:
            for single_value in values_list:
                test_node = copy.deepcopy(node)
                test_node.args['expression'].set('expressions', [single_value])
                if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                    node = test_node
                    break
    
    return node

def simplify_expressions_to_literals(node, test_script, full_statements, stmt_index):
    if isinstance(node, exp.Select) and node.args.get('expressions'):
        expressions = node.args['expressions']
        for i, expr in enumerate(expressions):
            if isinstance(expr, (exp.Binary, exp.Func)) and not isinstance(expr, exp.Literal):
                for literal in [exp.Literal.number("1"), exp.Literal.string("'x'"), exp.Null(), exp.Boolean(this=False)]:
                    test_node = copy.deepcopy(node)
                    test_expressions = list(expressions)
                    test_expressions[i] = literal
                    test_node.set('expressions', test_expressions)
                    if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                        expressions[i] = literal
                        node.set('expressions', expressions)
                        break
    
    return node

def reduce_values_expressions(node, test_script, full_statements, stmt_index):
    if not isinstance(node, exp.Insert):
        return node
    
    if (node.args.get('expression') and 
        isinstance(node.args['expression'], exp.Select) and
        node.args['expression'].args.get('from')):
        
        from_clause = node.args['expression'].args['from']
        if (isinstance(from_clause, exp.From) and 
            hasattr(from_clause, 'this') and
            isinstance(from_clause.this, exp.Subquery)):
            
            subquery = from_clause.this.this
            if (isinstance(subquery, exp.Select) and 
                subquery.args.get('from') and
                isinstance(subquery.args['from'].this, exp.Values)):
                
                values_expr = subquery.args['from'].this
                if hasattr(values_expr, 'expressions') and len(values_expr.expressions) > 0:
                    for i, tuple_expr in enumerate(values_expr.expressions):
                        if hasattr(tuple_expr, 'expressions'):
                            for j, val_expr in enumerate(tuple_expr.expressions):
                                if isinstance(val_expr, (exp.Binary, exp.Unary, exp.Paren)):
                                    test_node = copy.deepcopy(node)
                                    test_values = copy.deepcopy(values_expr)
                                    test_tuple = copy.deepcopy(tuple_expr)
                                    test_expressions = list(test_tuple.expressions)
                                    
                                    if isinstance(val_expr, exp.Not) and isinstance(val_expr.this, exp.Boolean):
                                        simplified = exp.Boolean(this=not val_expr.this.this)
                                    else:
                                        simplified = exp.Boolean(this=True)
                                    
                                    test_expressions[j] = simplified
                                    test_tuple.set('expressions', test_expressions)
                                    
                                    test_values_exprs = list(test_values.expressions)
                                    test_values_exprs[i] = test_tuple
                                    test_values.set('expressions', test_values_exprs)
                                    
                                    test_subquery = copy.deepcopy(subquery)
                                    test_subquery.args['from'].set('this', test_values)
                                    
                                    test_from = copy.deepcopy(from_clause)
                                    test_from.this.set('this', test_subquery)
                                    
                                    test_select = copy.deepcopy(node.args['expression'])
                                    test_select.set('from', test_from)
                                    
                                    test_node.set('expression', test_select)
                                    
                                    if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                                        return test_node
    
    return node

def reduce_node_aggressively(node, test_script, full_statements, stmt_index):
    if isinstance(node, exp.Create):
        node = reduce_create_table(node, test_script, full_statements, stmt_index)
    
    if isinstance(node, exp.Insert):
        node = reduce_insert_values(node, test_script, full_statements, stmt_index)
        node = reduce_values_expressions(node, test_script, full_statements, stmt_index)
    
    if isinstance(node, exp.Select):
        if node.args.get('expressions'):
            expressions = node.args['expressions']
            for i, expr in enumerate(expressions):
                if isinstance(expr, exp.Exists):
                    if hasattr(expr, 'this'):
                        test_node = copy.deepcopy(node)
                        test_expressions = list(expressions)
                        test_expressions[i] = exp.Literal.number("1")
                        test_node.set('expressions', test_expressions)
                        if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                            node = test_node
                            break
        
        if node.args.get('where') and isinstance(node.args['where'], exp.Not):
            test_node = copy.deepcopy(node)
            inner_expr = node.args['where'].this
            test_node.set('where', inner_expr)
            if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                node = test_node
        elif node.args.get('where'):
            test_node = copy.deepcopy(node)
            test_node.set('where', None)
            if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                node = test_node
        
        if node.args.get('group'):
            test_node = copy.deepcopy(node)
            test_node.set('group', None)
            if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                node = test_node
        
        if node.args.get('having'):
            test_node = copy.deepcopy(node)
            test_node.set('having', None)
            if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                node = test_node
        
        if hasattr(node, 'args') and node.args.get('order'):
            test_node = copy.deepcopy(node)
            test_node.set('order', None)
            if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                node = test_node
    
    node = simplify_expressions_to_literals(node, test_script, full_statements, stmt_index)
    
    result = delta_debug_node(node, test_script, full_statements, stmt_index)
    return result

def reduce_columns_minimally(statements, test_script):
    create_stmt = None
    insert_stmt = None
    select_stmt = None
    
    for stmt in statements:
        if isinstance(stmt, exp.Create):
            create_stmt = stmt
        elif isinstance(stmt, exp.Insert):
            insert_stmt = stmt
        elif isinstance(stmt, exp.Select):
            select_stmt = stmt
    
    if not (create_stmt and insert_stmt and select_stmt):
        return statements
    
    used_columns = set()
    if select_stmt.args.get('where'):
        for node in select_stmt.args['where'].walk():
            if isinstance(node, exp.Column):
                used_columns.add(node.name)
    
    if len(used_columns) >= 2:
        used_columns_list = list(used_columns)[:2]
        
        if create_stmt.args.get('this') and hasattr(create_stmt.args['this'], 'expressions'):
            columns = create_stmt.args['this'].expressions
            reduced_columns = []
            for col in columns:
                if hasattr(col, 'this') and col.this.name in used_columns_list:
                    simple_col = exp.ColumnDef(this=col.this)
                    reduced_columns.append(simple_col)
            
            if reduced_columns:
                test_statements = statements.copy()
                test_create = copy.deepcopy(create_stmt)
                test_create.args['this'].set('expressions', reduced_columns)
                
                if insert_stmt.args.get('this') and insert_stmt.args.get('expression'):
                    test_insert = copy.deepcopy(insert_stmt)
                    values_list = insert_stmt.args['expression'].expressions
                    for values_tuple in values_list:
                        if hasattr(values_tuple, 'expressions') and len(values_tuple.expressions) >= len(used_columns_list):
                            test_insert.set('this', exp.Table(this=create_stmt.args['this'].this))
                            col_list = [exp.Column(this=col) for col in used_columns_list]
                            test_insert.set('this', exp.Schema(this=test_insert.args['this'], expressions=col_list))
                            
                            orig_columns = [col.this.name for col in columns]
                            new_values = []
                            for col_name in used_columns_list:
                                if col_name in orig_columns:
                                    idx = orig_columns.index(col_name)
                                    if idx < len(values_tuple.expressions):
                                        new_values.append(values_tuple.expressions[idx])
                            
                            if new_values:
                                new_tuple = exp.Tuple(expressions=new_values)
                                test_insert.args['expression'].set('expressions', [new_tuple])
                                
                                test_statements[statements.index(create_stmt)] = test_create
                                test_statements[statements.index(insert_stmt)] = test_insert
                                
                                try:
                                    sql = ";\n".join(stmt.sql(normalize=True, pad=0) for stmt in test_statements) + ";"
                                    if test_query(sql, test_script):
                                        return test_statements
                                except Exception:
                                    pass
                            break
    
    return statements

def delta_debug_node(node, test_script, full_statements, stmt_index):
    if not hasattr(node, 'args') or not node.args:
        return node
    
    if not isinstance(node.args, (dict, list)):
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
                    sql = ";\n".join(stmt.sql(normalize=True, pad=0) for stmt in test_statements) + ";"
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
                sql = ";\n".join(stmt.sql(normalize=True, pad=0) for stmt in test_statements) + ";"
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
                    new_args = list(node.args)
                    new_args[k] = reduced
                    new_node.set("args", new_args)
                new_node = simplify_expression(new_node)
                test_statements = full_statements.copy()
                test_statements[stmt_index] = new_node
                try:
                    sql = ";\n".join(stmt.sql(normalize=True, pad=0) for stmt in test_statements) + ";"
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
                sql = ";\n".join(stmt.sql(normalize=True, pad=0) for stmt in remaining) + ";"
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
                sql = ";\n".join(s.sql(normalize=True, pad=0) for s in new_statements) + ";"
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
        return sql_query

    if not test_query(sql_query, test_script):
        return sql_query

    prev_size = len(sql_query)
    max_iterations = 7
    
    for iteration in range(max_iterations):
        parsed_statements = simplify_sql_constants(parsed_statements)
        parsed_statements = reduce_statements_aggressively(parsed_statements, test_script)
        parsed_statements = reduce_columns_minimally(parsed_statements, test_script)
        parsed_statements = delta_debug_statements(parsed_statements, test_script)
        
        parsed_statements = [stmt for stmt in parsed_statements if stmt is not None]
        
        for i, stmt in enumerate(parsed_statements):
            if stmt is not None:
                parsed_statements[i] = reduce_node_aggressively(stmt, test_script, parsed_statements, i)
        
        parsed_statements = [stmt for stmt in parsed_statements if stmt is not None]
        
        if not parsed_statements:
            break
            
        current_sql = ";\n".join(stmt.sql(normalize=True, pad=0) for stmt in parsed_statements) + ";"
        current_size = len(current_sql)
        
        if current_size >= prev_size:
            break
            
        prev_size = current_size
    
    reduced_statements = [stmt for stmt in parsed_statements if stmt is not None]
    
    if not reduced_statements:
        return sql_query
        
    reduced_sql = ";\n".join(stmt.sql(normalize=True, pad=0) for stmt in reduced_statements) + ";"
    return reduced_sql

def simplify_expression(node):
    if not isinstance(node, exp.Expression):
        return node
        
    items = list(node.args.items())
    for k, v in items:
        if isinstance(v, list):
            node.set(k, [simplify_expression(child) for child in v])
        elif isinstance(v, exp.Expression):
            node.set(k, simplify_expression(v))

    try:
        simplified = simplify(node)
        if isinstance(simplified, exp.Expression):
            return simplified
    except Exception:
        pass

    return node

def test_query(query: str, test_script: str) -> bool:    
    try:
        test_case_location = os.environ.get('TEST_CASE_LOCATION')
        if not test_case_location:
            test_case_location = os.path.join(os.getcwd(), "query.sql")

        with open(test_case_location, 'w') as f:
            f.write(query)

        result = subprocess.run(['bash', test_script], capture_output=True, text=True, timeout=30, env=os.environ.copy())
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
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
        sys.exit(1)
    
    reduced_query = reduce_sql_query(sql_query, args.test)
    test_case_location = os.environ.get('TEST_CASE_LOCATION')
    if not test_case_location:
        test_case_location = os.path.join(os.getcwd(), "query.sql")

    with open(test_case_location, 'w') as f:
        f.write(reduced_query)

    if not test_query(sql_query, args.test):
        print("WARNING: FINAL REDUCED QUERY DOES NOT TRIGGER THE BUG")

    print(reduced_query)