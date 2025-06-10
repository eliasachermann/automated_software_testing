import argparse
import subprocess
import sys
import os
import copy
from sqlglot import parse, exp
from sqlglot.expressions import Expression, Select, Insert
from sqlglot import tokenize
import re


def count_tokens(sql_query):
    tokens = list(tokenize(sql_query))
    return len(tokens)


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
            elif (
                isinstance(left, exp.Paren)
                and isinstance(left.this, exp.Boolean)
                and isinstance(right, exp.Paren)
                and isinstance(right.this, exp.Boolean)
            ):
                result = left.this.this != right.this.this
                return exp.Boolean(this=result)
        elif isinstance(expr, exp.EQ):
            if isinstance(left, exp.Boolean) and isinstance(right, exp.Boolean):
                result = left.this == right.this
                return exp.Boolean(this=result)
            elif (
                isinstance(left, exp.Paren)
                and isinstance(left.this, exp.Boolean)
                and isinstance(right, exp.Paren)
                and isinstance(right.this, exp.Boolean)
            ):
                result = left.this.this == right.this.this
                return exp.Boolean(this=result)

            if isinstance(left, exp.Literal) and isinstance(right, exp.Boolean):
                try:
                    left_val = (
                        float(left.this) if "." in str(left.this) else int(left.this)
                    )
                    right_val = 1 if right.this else 0
                    result = left_val == right_val
                    return exp.Boolean(this=result)
                except:
                    pass
            elif isinstance(right, exp.Literal) and isinstance(left, exp.Boolean):
                try:
                    right_val = (
                        float(right.this) if "." in str(right.this) else int(right.this)
                    )
                    left_val = 1 if left.this else 0
                    result = left_val == right_val
                    return exp.Boolean(this=result)
                except:
                    pass

        left_val = None
        right_val = None

        if isinstance(left, exp.Literal):
            left_val = left.this
            if isinstance(left_val, str):
                try:
                    left_val = float(left_val) if "." in left_val else int(left_val)
                except ValueError:
                    left_val = None
        elif isinstance(left, exp.Paren) and isinstance(left.this, exp.Literal):
            left_val = left.this.this
            if isinstance(left_val, str):
                try:
                    left_val = float(left_val) if "." in left_val else int(left_val)
                except ValueError:
                    left_val = None
        elif isinstance(left, exp.Neg) and isinstance(
            left.this, (exp.Literal, exp.Paren)
        ):
            inner = left.this
            if isinstance(inner, exp.Paren):
                inner = inner.this
            if isinstance(inner, exp.Literal):
                try:
                    val = inner.this
                    if isinstance(val, str):
                        val = float(val) if "." in val else int(val)
                    left_val = -val
                except (ValueError, TypeError):
                    left_val = None

        if isinstance(right, exp.Literal):
            right_val = right.this
            if isinstance(right_val, str):
                try:
                    right_val = float(right_val) if "." in right_val else int(right_val)
                except ValueError:
                    right_val = None
        elif isinstance(right, exp.Paren) and isinstance(right.this, exp.Literal):
            right_val = right.this.this
            if isinstance(right_val, str):
                try:
                    right_val = float(right_val) if "." in right_val else int(right_val)
                except ValueError:
                    right_val = None
        elif isinstance(right, exp.Neg) and isinstance(
            right.this, (exp.Literal, exp.Paren)
        ):
            inner = right.this
            if isinstance(inner, exp.Paren):
                inner = inner.this
            if isinstance(inner, exp.Literal):
                try:
                    val = inner.this
                    if isinstance(val, str):
                        val = float(val) if "." in val else int(val)
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
                        val = float(val) if "." in val else int(val)
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


def simplify_boolean_literals(statements, test_script):
    new_statements = []
    modified = False

    def simplify_not_expressions(node):
        if isinstance(node, exp.Not):
            inner = node.this

            if isinstance(inner, exp.Boolean) and inner.this is False:
                return exp.Boolean(this=True)

            if isinstance(inner, exp.Boolean) and inner.this is True:
                return exp.Boolean(this=False)

            if isinstance(inner, exp.Not):
                return simplify_not_expressions(inner.this)

            if isinstance(inner, exp.Paren):
                if isinstance(inner.this, exp.Boolean):
                    if inner.this.this is False:
                        return exp.Boolean(this=True)
                    elif inner.this.this is True:
                        return exp.Boolean(this=False)
                simplified_inner = simplify_not_expressions(inner.this)
                if simplified_inner != inner.this:
                    new_paren = copy.deepcopy(inner)
                    new_paren.set("this", simplified_inner)
                    return exp.Not(this=new_paren)

            simplified_inner = simplify_not_expressions(inner)
            if simplified_inner != inner:
                return exp.Not(this=simplified_inner)

        elif isinstance(node, exp.Paren):
            simplified_inner = simplify_not_expressions(node.this)
            if simplified_inner != node.this:
                if isinstance(simplified_inner, (exp.Boolean, exp.Literal)):
                    return simplified_inner
                new_paren = copy.deepcopy(node)
                new_paren.set("this", simplified_inner)
                return new_paren

        elif isinstance(node, exp.Binary):
            left = simplify_not_expressions(node.left)
            right = simplify_not_expressions(node.right)

            if left != node.left or right != node.right:
                new_binary = copy.deepcopy(node)
                new_binary.set("left", left)
                new_binary.set("right", right)
                return new_binary

        elif hasattr(node, "args") and node.args:
            changed = False
            new_node = copy.deepcopy(node)

            if isinstance(node.args, dict):
                for key, value in node.args.items():
                    if isinstance(value, exp.Expression):
                        simplified_value = simplify_not_expressions(value)
                        if simplified_value != value:
                            new_node.set(key, simplified_value)
                            changed = True
                    elif isinstance(value, list):
                        new_list = []
                        list_changed = False
                        for item in value:
                            if isinstance(item, exp.Expression):
                                simplified_item = simplify_not_expressions(item)
                                if simplified_item != item:
                                    list_changed = True
                                new_list.append(simplified_item)
                            else:
                                new_list.append(item)
                        if list_changed:
                            new_node.set(key, new_list)
                            changed = True

            if changed:
                return new_node

        return node

    for stmt in statements:
        new_stmt = copy.deepcopy(stmt)
        simplified_stmt = simplify_not_expressions(new_stmt)

        if not expressions_equal(simplified_stmt, stmt):
            test_statements = [simplified_stmt if s == stmt else s for s in statements]
            try:
                sql = get_query_from_parsed(test_statements)
                if test_query(sql, test_script):
                    new_statements.append(simplified_stmt)
                    modified = True
                else:
                    new_statements.append(stmt)
            except Exception:
                new_statements.append(stmt)
        else:
            new_statements.append(stmt)

    return new_statements if modified else statements


def remove_unnecessary_parentheses(statements, test_script):
    new_statements = []
    modified = False

    def simplify_parentheses(node):
        if isinstance(node, exp.Paren):
            inner = node.this
            
            if isinstance(inner, (exp.Literal, exp.Column, exp.Boolean, exp.Null)):
                return inner
            
            if isinstance(inner, exp.Paren):
                return simplify_parentheses(inner)
            
            if isinstance(inner, exp.Binary):
                simplified_inner = simplify_parentheses(inner)
                
                if isinstance(simplified_inner, (exp.Literal, exp.Column, exp.Boolean)):
                    return simplified_inner
                
                new_paren = copy.deepcopy(node)
                new_paren.set("this", simplified_inner)
                return new_paren
            
            simplified_inner = simplify_parentheses(inner)
            if simplified_inner != inner:
                if isinstance(simplified_inner, (exp.Literal, exp.Column, exp.Boolean, exp.Null)):
                    return simplified_inner
                new_paren = copy.deepcopy(node)
                new_paren.set("this", simplified_inner)
                return new_paren
                
        elif isinstance(node, exp.Binary):
            left = simplify_parentheses(node.left)
            right = simplify_parentheses(node.right)
            
            if left != node.left or right != node.right:
                new_binary = copy.deepcopy(node)
                new_binary.set("left", left)
                new_binary.set("right", right)
                return new_binary
                
        elif isinstance(node, exp.Unary):
            operand = simplify_parentheses(node.this)
            if operand != node.this:
                new_unary = copy.deepcopy(node)
                new_unary.set("this", operand)
                return new_unary
                
        elif hasattr(node, "args") and node.args:
            changed = False
            new_node = copy.deepcopy(node)
            
            if isinstance(node.args, dict):
                for key, value in node.args.items():
                    if isinstance(value, exp.Expression):
                        simplified_value = simplify_parentheses(value)
                        if simplified_value != value:
                            new_node.set(key, simplified_value)
                            changed = True
                    elif isinstance(value, list):
                        new_list = []
                        list_changed = False
                        for item in value:
                            if isinstance(item, exp.Expression):
                                simplified_item = simplify_parentheses(item)
                                if simplified_item != item:
                                    list_changed = True
                                new_list.append(simplified_item)
                            else:
                                new_list.append(item)
                        if list_changed:
                            new_node.set(key, new_list)
                            changed = True
            
            if changed:
                return new_node
        
        return node

    for stmt in statements:
        new_stmt = copy.deepcopy(stmt)
        simplified_stmt = simplify_parentheses(new_stmt)
        
        if not expressions_equal(simplified_stmt, stmt):
            test_statements = [simplified_stmt if s == stmt else s for s in statements]
            try:
                sql = get_query_from_parsed(test_statements)
                if test_query(sql, test_script):
                    new_statements.append(simplified_stmt)
                    modified = True
                else:
                    new_statements.append(stmt)
            except Exception:
                new_statements.append(stmt)
        else:
            new_statements.append(stmt)
    
    return new_statements if modified else statements


def aggressive_parentheses_removal(statements, test_script):
    def find_and_test_paren_removal(node, test_statements, stmt_index):
        if isinstance(node, exp.Paren):
            test_node = node.this
            temp_statements = copy.deepcopy(test_statements)
            temp_statements[stmt_index] = replace_node_in_statement(
                temp_statements[stmt_index], node, test_node
            )
            
            try:
                sql = get_query_from_parsed(temp_statements)
                if test_query(sql, test_script):
                    return test_node, True
            except Exception:
                pass
        
        if hasattr(node, "args") and node.args:
            if isinstance(node.args, dict):
                for key, value in node.args.items():
                    if isinstance(value, exp.Expression):
                        result, changed = find_and_test_paren_removal(
                            value, test_statements, stmt_index
                        )
                        if changed:
                            new_node = copy.deepcopy(node)
                            new_node.set(key, result)
                            return new_node, True
                    elif isinstance(value, list):
                        for i, item in enumerate(value):
                            if isinstance(item, exp.Expression):
                                result, changed = find_and_test_paren_removal(
                                    item, test_statements, stmt_index
                                )
                                if changed:
                                    new_node = copy.deepcopy(node)
                                    new_list = list(value)
                                    new_list[i] = result
                                    new_node.set(key, new_list)
                                    return new_node, True
        
        return node, False

    def replace_node_in_statement(stmt, old_node, new_node):
        def replace_in_node(current_node):
            if current_node is old_node:
                return new_node
            
            if hasattr(current_node, "args") and current_node.args:
                new_current = copy.deepcopy(current_node)
                if isinstance(current_node.args, dict):
                    for key, value in current_node.args.items():
                        if isinstance(value, exp.Expression):
                            new_current.set(key, replace_in_node(value))
                        elif isinstance(value, list):
                            new_list = []
                            for item in value:
                                if isinstance(item, exp.Expression):
                                    new_list.append(replace_in_node(item))
                                else:
                                    new_list.append(item)
                            new_current.set(key, new_list)
                return new_current
            
            return current_node
        
        return replace_in_node(stmt)

    modified = True
    iteration = 0
    max_iterations = 10
    
    while modified and iteration < max_iterations:
        modified = False
        iteration += 1
        
        for i, stmt in enumerate(statements):
            result, changed = find_and_test_paren_removal(stmt, statements, i)
            if changed:
                statements[i] = result
                modified = True
                break  
    
    return statements


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


def simplify_sql_constants(
    parsed_statements: list[Expression], test_script
) -> list[Expression]:
    original_statements = parsed_statements.copy()

    simplified_statements = []
    for stmt in parsed_statements:
        simplified = simplify_statement(stmt)
        simplified_statements.append(simplified)

    query = get_query_from_parsed(simplified_statements)
    if not test_query(query, test_script):
        return original_statements

    return simplified_statements


def reduce_statements_aggressively(statements, test_script):
    if len(statements) <= 1:
        return statements

    non_true_statements = []
    for stmt in statements:
        if not (
            isinstance(stmt, exp.Select)
            and len(stmt.args.get("expressions", [])) == 1
            and isinstance(stmt.args["expressions"][0], exp.Boolean)
            and stmt.args["expressions"][0].this is True
            and not stmt.args.get("where")
            and not stmt.args.get("from")
        ):
            non_true_statements.append(stmt)

    if len(non_true_statements) < len(statements):
        try:
            sql = get_query_from_parsed(non_true_statements)
            if test_query(sql, test_script):
                return reduce_statements_aggressively(non_true_statements, test_script)
        except Exception:
            pass

    non_trivial = []
    seen_statements = set()

    for stmt in statements:
        if isinstance(stmt, exp.Update) and (
            not stmt.args.get("this") or not stmt.args.get("expressions")
        ):
            continue
        if isinstance(stmt, exp.Delete) and not stmt.args.get("this"):
            continue
        if isinstance(stmt, exp.Insert) and (
            not stmt.args.get("this") or not stmt.args.get("expression")
        ):
            continue

        if isinstance(stmt, exp.Select):
            if (
                len(stmt.args.get("expressions", [])) == 1
                and isinstance(stmt.args["expressions"][0], exp.Boolean)
                and stmt.args["expressions"][0].this is True
                and not stmt.args.get("where")
                and not stmt.args.get("from")
            ):
                if "select_true" in seen_statements:
                    continue
                seen_statements.add("select_true")

        stmt_sql = stmt.sql()
        if stmt_sql in seen_statements:
            continue
        seen_statements.add(stmt_sql)

        non_trivial.append(stmt)

    if len(non_trivial) < len(statements):
        try:
            sql = get_query_from_parsed(non_trivial)
            if test_query(sql, test_script):
                return reduce_statements_aggressively(non_trivial, test_script)
        except Exception:
            pass

    filtered = [s for s in statements if not isinstance(s, (exp.Update, exp.Delete))]
    if len(filtered) < len(statements):
        try:
            sql = get_query_from_parsed(filtered)
            if test_query(sql, test_script):
                return reduce_statements_aggressively(filtered, test_script)
        except Exception:
            pass

    essential = [
        s for s in statements if isinstance(s, (exp.Create, exp.Insert, exp.Select))
    ]
    if len(essential) < len(statements) and essential:
        try:
            sql = get_query_from_parsed(essential)
            if test_query(sql, test_script):
                return reduce_statements_aggressively(essential, test_script)
        except Exception:
            pass

    filtered = [
        s
        for s in statements
        if not (hasattr(s, "kind") and s.kind in ["VIEW", "INDEX", "TRIGGER"])
    ]
    if len(filtered) < len(statements):
        try:
            sql = get_query_from_parsed(filtered)
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
                sql = get_query_from_parsed(test_statements)
                if test_query(sql, test_script):
                    return reduce_statements_aggressively(test_statements, test_script)
            except Exception:
                continue

    return statements


def test_reduced_node(node, test_script, full_statements, stmt_index):
    test_statements = full_statements.copy()
    test_statements[stmt_index] = node
    try:
        sql = get_query_from_parsed(test_statements)
        result = test_query(sql, test_script)
        return result
    except Exception:
        return False


def reduce_create_table(node, test_script, full_statements, stmt_index):
    if not isinstance(node, exp.Create) or node.args.get("kind") != "TABLE":
        return node

    if node.args.get("exists"):
        test_node = copy.deepcopy(node)
        test_node.set("exists", None)
        if test_reduced_node(test_node, test_script, full_statements, stmt_index):
            node = test_node

    if node.args.get("this") and hasattr(node.args["this"], "expressions"):
        columns = node.args["this"].expressions
        for i, col in enumerate(columns):
            if hasattr(col, "args") and col.args.get("constraints"):
                constraints = col.args["constraints"]
                if len(constraints) > 1:
                    test_node = copy.deepcopy(node)
                    test_columns = list(columns)
                    test_col = copy.deepcopy(col)
                    test_col.set("constraints", constraints[:1])
                    test_columns[i] = test_col
                    test_node.args["this"].set("expressions", test_columns)
                    if test_reduced_node(
                        test_node, test_script, full_statements, stmt_index
                    ):
                        node = test_node
                        columns = test_columns

                test_node = copy.deepcopy(node)
                test_columns = list(columns)
                test_col = copy.deepcopy(col)
                test_col.set("constraints", [])
                test_columns[i] = test_col
                test_node.args["this"].set("expressions", test_columns)
                if test_reduced_node(
                    test_node, test_script, full_statements, stmt_index
                ):
                    node = test_node
                    columns = test_columns

            if hasattr(col, "args") and col.args.get("kind"):
                test_node = copy.deepcopy(node)
                test_columns = list(columns)
                test_col = copy.deepcopy(col)
                test_col.set("kind", None)
                test_columns[i] = test_col
                test_node.args["this"].set("expressions", test_columns)
                if test_reduced_node(
                    test_node, test_script, full_statements, stmt_index
                ):
                    node = test_node
                    columns = test_columns

    return node


def reduce_unused_table_inserts(statements, test_script):
    select_stmt = None
    referenced_tables = set()

    for stmt in statements:
        if isinstance(stmt, exp.Select):
            select_stmt = stmt
            for node in stmt.walk():
                if isinstance(node, exp.Table):
                    if hasattr(node, "name"):
                        if hasattr(node.name, "this"):
                            table_name = str(node.name.this).lower()
                            referenced_tables.add(table_name)
                        else:
                            table_name = str(node.name).lower()
                            referenced_tables.add(table_name)
                elif isinstance(node, exp.Column) and node.args.get("table"):
                    table_ref = node.args["table"]
                    if hasattr(table_ref, "this"):
                        table_name = str(table_ref.this).lower()
                        referenced_tables.add(table_name)
                    elif hasattr(table_ref, "name"):
                        table_name = str(table_ref.name).lower()
                        referenced_tables.add(table_name)
                    else:
                        table_name = str(table_ref).lower()
                        referenced_tables.add(table_name)

    if not select_stmt or not referenced_tables:
        return statements

    filtered_statements = []
    for stmt in statements:
        keep_stmt = True

        if isinstance(stmt, exp.Create) and stmt.args.get("this"):
            table_schema = stmt.args["this"]
            if hasattr(table_schema, "this"):
                table_name = str(table_schema.this).lower()
                if hasattr(table_schema.this, "name"):
                    table_name = str(table_schema.this.name).lower()
            else:
                table_name = str(table_schema).lower()

            if table_name not in referenced_tables:
                keep_stmt = False

        elif isinstance(stmt, exp.Insert) and stmt.args.get("this"):
            table_ref = stmt.args["this"]
            table_name = None

            if hasattr(table_ref, "this"):
                table_name = str(table_ref.this).lower()
            elif hasattr(table_ref, "name"):
                if hasattr(table_ref.name, "this"):
                    table_name = str(table_ref.name.this).lower()
                else:
                    table_name = str(table_ref.name).lower()
            else:
                table_str = str(table_ref).lower()
                table_name = table_str

            if table_name and table_name not in referenced_tables:
                keep_stmt = False

        if keep_stmt:
            filtered_statements.append(stmt)

    if len(filtered_statements) < len(statements):
        try:
            sql = get_query_from_parsed(filtered_statements)
            if test_query(sql, test_script):
                return filtered_statements
        except Exception:
            pass

    return statements


def eliminate_unused_tables(statements, test_script):
    select_stmt = None
    table_names = set()

    for stmt in statements:
        if isinstance(stmt, exp.Select):
            select_stmt = stmt
            for node in stmt.walk():
                if isinstance(node, exp.Table):
                    if hasattr(node, "name"):
                        if hasattr(node.name, "this"):
                            table_names.add(str(node.name.this).lower())
                        else:
                            table_names.add(str(node.name).lower())
                    elif hasattr(node, "this"):
                        table_names.add(str(node.this).lower())
                elif isinstance(node, exp.Column) and node.args.get("table"):
                    table_ref = node.args["table"]
                    if hasattr(table_ref, "this"):
                        table_names.add(str(table_ref.this).lower())
                    elif hasattr(table_ref, "name"):
                        table_names.add(str(table_ref.name).lower())
                    else:
                        table_names.add(str(table_ref).lower())

    if not select_stmt:
        return statements

    essential_statements = []
    for stmt in statements:
        if isinstance(stmt, exp.Create) and stmt.args.get("this"):
            table_schema = stmt.args["this"]
            if hasattr(table_schema, "this"):
                table_ref = table_schema.this
                if hasattr(table_ref, "name"):
                    table_name = str(table_ref.name).lower()
                elif hasattr(table_ref, "this"):
                    table_name = str(table_ref.this).lower()
                else:
                    table_name = str(table_ref).lower()
            else:
                table_name = str(table_schema).lower()

            if table_name in table_names:
                essential_statements.append(stmt)

        elif isinstance(stmt, exp.Insert) and stmt.args.get("this"):
            table_ref = stmt.args["this"]
            table_name = None

            if hasattr(table_ref, "sql"):
                table_name = table_ref.sql().lower()
            elif hasattr(table_ref, "name"):
                if hasattr(table_ref.name, "this"):
                    table_name = str(table_ref.name.this).lower()
                else:
                    table_name = str(table_ref.name).lower()
            elif hasattr(table_ref, "this"):
                table_name = str(table_ref.this).lower()
            else:
                table_name = str(table_ref).lower()

            if table_name and table_name in table_names:
                essential_statements.append(stmt)
        else:
            essential_statements.append(stmt)

    if len(essential_statements) < len(statements):
        try:
            sql = get_query_from_parsed(essential_statements)
            if test_query(sql, test_script):
                return essential_statements
        except Exception:
            pass

    return statements


def reduce_insert_statements_aggressively(statements, test_script):
    insert_statements = [
        (i, stmt) for i, stmt in enumerate(statements) if isinstance(stmt, exp.Insert)
    ]
    if len(insert_statements) <= 1:
        return statements

    inserts_by_table = {}
    for i, stmt in insert_statements:
        if stmt.args.get("this"):
            table_name = str(stmt.args["this"].name).lower()
            if table_name not in inserts_by_table:
                inserts_by_table[table_name] = []
            inserts_by_table[table_name].append((i, stmt))

    for table_name, table_inserts in inserts_by_table.items():
        if len(table_inserts) > 1:
            for _, single_insert in table_inserts:
                test_statements = []
                for i, orig_stmt in enumerate(statements):
                    if isinstance(orig_stmt, exp.Insert) and orig_stmt.args.get("this"):
                        orig_table = str(orig_stmt.args["this"].name).lower()
                        if orig_table == table_name:
                            if orig_stmt == single_insert:
                                test_statements.append(orig_stmt)
                        else:
                            test_statements.append(orig_stmt)
                    else:
                        test_statements.append(orig_stmt)

                try:
                    sql = get_query_from_parsed(test_statements)
                    if test_query(sql, test_script):
                        return test_statements
                except Exception:
                    continue

    return statements


def reduce_insert_values(node, test_script, full_statements, stmt_index):
    if not isinstance(node, exp.Insert):
        return node

    if hasattr(node, "args") and node.args.get("alternative"):
        test_node = copy.deepcopy(node)
        test_node.set("alternative", None)
        if test_reduced_node(test_node, test_script, full_statements, stmt_index):
            node = test_node

    if node.args.get("expression") and hasattr(node.args["expression"], "expressions"):
        values_list = node.args["expression"].expressions
        if len(values_list) > 1:
            for single_value in values_list:
                test_node = copy.deepcopy(node)
                test_node.args["expression"].set("expressions", [single_value])
                if test_reduced_node(
                    test_node, test_script, full_statements, stmt_index
                ):
                    node = test_node
                    break

    return node


def simplify_expressions_to_literals(node, test_script, full_statements, stmt_index):
    if isinstance(node, exp.Select) and node.args.get("expressions"):
        expressions = node.args["expressions"]
        for i, expr in enumerate(expressions):
            if isinstance(expr, (exp.Binary, exp.Func)) and not isinstance(
                expr, exp.Literal
            ):
                for literal in [
                    exp.Literal.number("1"),
                    exp.Literal.string("'x'"),
                    exp.Null(),
                    exp.Boolean(this=False),
                ]:
                    test_node = copy.deepcopy(node)
                    test_expressions = list(expressions)
                    test_expressions[i] = literal
                    test_node.set("expressions", test_expressions)
                    if test_reduced_node(
                        test_node, test_script, full_statements, stmt_index
                    ):
                        expressions[i] = literal
                        node.set("expressions", expressions)
                        break

    return node


def reduce_values_expressions(node, test_script, full_statements, stmt_index):
    if not isinstance(node, exp.Insert):
        return node

    if (
        node.args.get("expression")
        and isinstance(node.args["expression"], exp.Select)
        and node.args["expression"].args.get("from")
    ):
        from_clause = node.args["expression"].args["from"]
        if (
            isinstance(from_clause, exp.From)
            and hasattr(from_clause, "this")
            and isinstance(from_clause.this, exp.Subquery)
        ):
            subquery = from_clause.this.this
            if (
                isinstance(subquery, exp.Select)
                and subquery.args.get("from")
                and isinstance(subquery.args["from"].this, exp.Values)
            ):
                values_expr = subquery.args["from"].this
                if (
                    hasattr(values_expr, "expressions")
                    and len(values_expr.expressions) > 0
                ):
                    for i, tuple_expr in enumerate(values_expr.expressions):
                        if hasattr(tuple_expr, "expressions"):
                            for j, val_expr in enumerate(tuple_expr.expressions):
                                if isinstance(
                                    val_expr, (exp.Binary, exp.Unary, exp.Paren)
                                ):
                                    test_node = copy.deepcopy(node)
                                    test_values = copy.deepcopy(values_expr)
                                    test_tuple = copy.deepcopy(tuple_expr)
                                    test_expressions = list(test_tuple.expressions)

                                    if isinstance(val_expr, exp.Not) and isinstance(
                                        val_expr.this, exp.Boolean
                                    ):
                                        simplified = exp.Boolean(
                                            this=not val_expr.this.this
                                        )
                                    else:
                                        simplified = exp.Boolean(this=True)

                                    test_expressions[j] = simplified
                                    test_tuple.set("expressions", test_expressions)

                                    test_values_exprs = list(test_values.expressions)
                                    test_values_exprs[i] = test_tuple
                                    test_values.set("expressions", test_values_exprs)

                                    test_subquery = copy.deepcopy(subquery)
                                    test_subquery.args["from"].set("this", test_values)

                                    test_from = copy.deepcopy(from_clause)
                                    test_from.this.set("this", test_subquery)

                                    test_select = copy.deepcopy(node.args["expression"])
                                    test_select.set("from", test_from)

                                    test_node.set("expression", test_select)

                                    if test_reduced_node(
                                        test_node,
                                        test_script,
                                        full_statements,
                                        stmt_index,
                                    ):
                                        return test_node

    return node


def reduce_node_aggressively(node, test_script, full_statements, stmt_index):
    node = simplify_case_expressions(node, test_script, full_statements, stmt_index)
    node = simplify_boolean_expressions(node, test_script, full_statements, stmt_index)
    node = simplify_subquery_expressions(node, test_script, full_statements, stmt_index)

    if isinstance(node, exp.Create):
        node = reduce_create_table(node, test_script, full_statements, stmt_index)

    if isinstance(node, exp.Insert):
        node = reduce_insert_values(node, test_script, full_statements, stmt_index)
        node = reduce_values_expressions(node, test_script, full_statements, stmt_index)

    if isinstance(node, exp.Select):
        if node.args.get("expressions"):
            expressions = node.args["expressions"]
            for i, expr in enumerate(expressions):
                if isinstance(expr, exp.Exists):
                    if hasattr(expr, "this"):
                        test_node = copy.deepcopy(node)
                        test_expressions = list(expressions)
                        test_expressions[i] = exp.Literal.number("1")
                        test_node.set("expressions", test_expressions)
                        if test_reduced_node(
                            test_node, test_script, full_statements, stmt_index
                        ):
                            node = test_node
                            break

        if node.args.get("where") and isinstance(node.args["where"], exp.Not):
            test_node = copy.deepcopy(node)
            inner_expr = node.args["where"].this
            test_node.set("where", inner_expr)
            if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                node = test_node
        elif node.args.get("where"):
            test_node = copy.deepcopy(node)
            test_node.set("where", None)
            if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                node = test_node

        if node.args.get("group"):
            test_node = copy.deepcopy(node)
            test_node.set("group", None)
            if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                node = test_node

        if node.args.get("having"):
            test_node = copy.deepcopy(node)
            test_node.set("having", None)
            if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                node = test_node

        if hasattr(node, "args") and node.args.get("order"):
            test_node = copy.deepcopy(node)
            test_node.set("order", None)
            if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                node = test_node

    node = simplify_expressions_to_literals(
        node, test_script, full_statements, stmt_index
    )

    result = delta_debug_node(node, test_script, full_statements, stmt_index)
    return result


def reduce_columns_minimally(statements, test_script):
    select_stmt = None
    for stmt in statements:
        if isinstance(stmt, exp.Select):
            select_stmt = stmt
            break

    if not select_stmt:
        return statements

    used_columns = {}
    for node in select_stmt.walk():
        if isinstance(node, exp.Column):
            table_ref = node.args.get("table", "")
            if table_ref:
                if hasattr(table_ref, "this"):
                    table_name = str(table_ref.this).lower()
                else:
                    table_name = str(table_ref).lower()

                if table_name not in used_columns:
                    used_columns[table_name] = set()

                col_name = node.name
                if hasattr(col_name, "this"):
                    col_name = str(col_name.this).lower()
                else:
                    col_name = str(col_name).lower()

                used_columns[table_name].add(col_name)

    if not used_columns:
        return statements

    new_statements = []
    modified = False

    for stmt in statements:
        if isinstance(stmt, exp.Create) and stmt.args.get("this"):
            table_ref = stmt.args["this"].this
            table_name = str(table_ref).lower()

            if table_name in used_columns and hasattr(stmt.args["this"], "expressions"):
                columns = stmt.args["this"].expressions
                used_cols = used_columns[table_name]

                kept_columns = []
                for col in columns:
                    if hasattr(col, "this") and hasattr(col.this, "this"):
                        col_name = str(col.this.this).lower()
                    elif hasattr(col, "this"):
                        col_name = str(col.this).lower()
                    else:
                        col_name = str(col).lower()

                    if col_name in used_cols:
                        kept_columns.append(col)

                if len(kept_columns) < len(columns) and kept_columns:
                    test_stmt = copy.deepcopy(stmt)
                    test_stmt.args["this"].set("expressions", kept_columns)
                    test_statements = [
                        test_stmt if s == stmt else s for s in statements
                    ]

                    try:
                        sql = get_query_from_parsed(test_statements)
                        if test_query(sql, test_script):
                            new_statements.append(test_stmt)
                            modified = True
                            continue
                    except Exception:
                        pass

            new_statements.append(stmt)

        elif isinstance(stmt, exp.Insert) and stmt.args.get("this"):
            new_statements.append(stmt)
        else:
            new_statements.append(stmt)

    return new_statements if modified else statements


def expressions_equal(expr1, expr2):
    if type(expr1) is not type(expr2):
        return False

    if not hasattr(expr1, "args") or not hasattr(expr2, "args"):
        return expr1 == expr2

    if expr1.args.keys() != expr2.args.keys():
        return False

    for k in expr1.args:
        v1 = expr1.args[k]
        v2 = expr2.args[k]

        if isinstance(v1, list) and isinstance(v2, list):
            if len(v1) != len(v2):
                return False
            for i in range(len(v1)):
                if not expressions_equal(v1[i], v2[i]):
                    return False
        elif isinstance(v1, exp.Expression) and isinstance(v2, exp.Expression):
            if not expressions_equal(v1, v2):
                return False
        else:
            if v1 != v2:
                return False

    return True


def delta_debug_node(node, test_script, full_statements, stmt_index):
    if not hasattr(node, "args") or not node.args:
        return node

    def validate_reduction(new_node):
        test_statements = full_statements.copy()
        test_statements[stmt_index] = new_node
        try:
            sql = get_query_from_parsed(test_statements)
            return test_query(sql, test_script)
        except Exception:
            return False

    if not hasattr(node, "args") or not node.args:
        return node

    if isinstance(node, exp.Where):
        if not validate_reduction(node):
            return node

    if isinstance(node, exp.Case):
        if not validate_reduction(node):
            return node

    if isinstance(node, exp.Join):
        if node.args.get("on"):
            test_node = copy.deepcopy(node)
            test_node.args["on"] = None
            if not validate_reduction(test_node):
                return node

    if not isinstance(node.args, (dict, list)):
        return node

    if isinstance(node, exp.Window):
        return node

    if isinstance(node, exp.WindowSpec):
        return node

    if isinstance(node, exp.Func) and hasattr(node, "this"):
        func_name = str(node.this).upper()
        if func_name in ["ROW_NUMBER", "LAG", "LEAD", "RANK", "DENSE_RANK"]:
            return node

    if isinstance(node.args, dict):
        children = [(k, v) for k, v in node.args.items() if v is not None]
    elif isinstance(node.args, list):
        children = [(i, v) for i, v in enumerate(node.args) if v is not None]
    else:
        return node

    if len(children) <= 1:
        if children and hasattr(children[0][1], "args"):
            reduced_child = delta_debug_node(
                children[0][1], test_script, full_statements, stmt_index
            )
            if not expressions_equal(reduced_child, children[0][1]):
                new_node = copy.deepcopy(node)
                if isinstance(node.args, dict):
                    new_args = dict(node.args)
                    new_args[children[0][0]] = reduced_child
                    new_node.set("args", new_args)
                else:
                    new_args = list(node.args)
                    new_args[children[0][0]] = reduced_child
                    new_node.set("args", new_args)
                test_statements = full_statements.copy()
                test_statements[stmt_index] = new_node
                try:
                    sql = get_query_from_parsed(test_statements)
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

            if isinstance(node, (exp.Select, exp.Alias)) and any(
                isinstance(child[1], exp.Window) for child in children
            ):
                continue

            new_node = copy.deepcopy(node)
            if isinstance(node.args, dict):
                new_node.args = {k: v for k, v in kept_children}
            else:
                new_node.args = [v for _, v in kept_children]
            test_statements = full_statements.copy()
            test_statements[stmt_index] = new_node
            try:
                sql = get_query_from_parsed(test_statements)
                if test_query(sql, test_script):
                    return delta_debug_node(
                        new_node, test_script, test_statements, stmt_index
                    )
            except Exception:
                continue
        subset_size //= 2

    for i, (k, v) in enumerate(children):
        if hasattr(v, "args"):
            reduced = delta_debug_node(v, test_script, full_statements, stmt_index)
            if not expressions_equal(reduced, v):
                new_node = copy.deepcopy(node)
                if isinstance(node.args, dict):
                    new_node.args[k] = reduced
                else:
                    new_args = list(node.args)
                    new_args[k] = reduced
                    new_node.set("args", new_args)
                test_statements = full_statements.copy()
                test_statements[stmt_index] = new_node
                try:
                    sql = get_query_from_parsed(test_statements)
                    if test_query(sql, test_script):
                        return new_node
                except Exception:
                    continue

    return node


def delta_debug_statements(statements, test_script):
    if len(statements) <= 1:
        if statements:
            reduced_stmt = delta_debug_node(statements[0], test_script, statements, 0)
            if not expressions_equal(reduced_stmt, statements[0]):
                try:
                    sql = get_query_from_parsed([reduced_stmt])
                    if test_query(sql, test_script):
                        return [reduced_stmt]
                except Exception:
                    pass
            return statements
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
                sql = get_query_from_parsed(remaining)
                if not test_query(sql, test_script):
                    continue

                temp_reduced = delta_debug_statements(remaining, test_script)
                temp_sql = get_query_from_parsed(temp_reduced)
                if test_query(temp_sql, test_script):
                    return temp_reduced
            except Exception:
                continue

        subset_size //= 2

    modified = False
    new_statements = statements.copy()

    for i, stmt in enumerate(statements):
        reduced = delta_debug_node(stmt, test_script, statements, i)
        if not expressions_equal(reduced, stmt):
            temp_statements = new_statements.copy()
            temp_statements[i] = reduced
            try:
                sql = get_query_from_parsed(temp_statements)
                if test_query(sql, test_script):
                    final_sql = get_query_from_parsed(temp_statements)
                    if test_query(final_sql, test_script):
                        new_statements[i] = reduced
                        modified = True
            except Exception:
                continue

    if modified:
        try:
            final_sql = get_query_from_parsed(new_statements)
            if test_query(final_sql, test_script):
                return new_statements
        except Exception:
            pass

    return statements


def simplify_join_conditions(statements, test_script):
    new_statements = []
    modified = False

    def get_conditions(condition):
        if isinstance(condition, exp.And):
            if isinstance(condition.args.get("this"), list):
                return condition.args["this"]
        elif isinstance(condition, exp.Or):
            if isinstance(condition.args.get("this"), list):
                return condition.args["this"]
        return [condition]

    def statements_match(stmt1, stmt2):
        if type(stmt1) is not type(stmt2):
            return False
        if not hasattr(stmt1, "sql") or not hasattr(stmt2, "sql"):
            return False
        return stmt1.sql() == stmt2.sql()

    for stmt in statements:
        node = copy.deepcopy(stmt)
        for join_node in node.walk():
            if isinstance(join_node, exp.Join):
                if join_node.args.get("on"):
                    condition = join_node.args["on"]
                    conditions = get_conditions(condition)

                    for cond in conditions:
                        if isinstance(cond, (exp.Binary, exp.Exists, exp.Not)):
                            test_node = copy.deepcopy(node)
                            for test_join in test_node.walk():
                                if (
                                    isinstance(test_join, exp.Join)
                                    and test_join.args.get("on") == condition
                                ):
                                    test_join.set("on", cond)
                                    break
                            test_statements = [
                                test_node if statements_match(s, stmt) else s
                                for s in statements
                            ]
                            try:
                                sql = get_query_from_parsed(test_statements)
                                if test_query(sql, test_script):
                                    join_node.set("on", cond)
                                    modified = True
                                    break
                            except Exception:
                                continue
        new_statements.append(node)

    if modified:
        try:
            sql = get_query_from_parsed(new_statements)
            if test_query(sql, test_script):
                return new_statements
        except Exception:
            pass

    return statements


def reduce_create_table_columns(statements, test_script):
    for i, stmt in enumerate(statements):
        if isinstance(stmt, exp.Create) and stmt.args.get("kind") == "TABLE":
            used_columns = set()
            for other_stmt in statements:
                if other_stmt != stmt:
                    for node in other_stmt.walk():
                        if isinstance(node, exp.Column):
                            col_name = str(node.name).lower()
                            used_columns.add(col_name)

            if stmt.args.get("this") and hasattr(stmt.args["this"], "expressions"):
                columns = stmt.args["this"].expressions
                kept_columns = []
                for col in columns:
                    if hasattr(col, "this") and str(col.this).lower() in used_columns:
                        kept_columns.append(col)

                if kept_columns:
                    test_stmt = copy.deepcopy(stmt)
                    test_stmt.args["this"].set("expressions", kept_columns)
                    test_statements = statements.copy()
                    test_statements[i] = test_stmt
                    try:
                        sql = get_query_from_parsed(test_statements)
                        if test_query(sql, test_script):
                            statements = test_statements
                            continue
                    except Exception:
                        pass
    return statements


def simplify_boolean_expressions(node, test_script, full_statements, stmt_index):
    if isinstance(node, exp.Binary):
        for literal in [exp.Boolean(this=True), exp.Boolean(this=False)]:
            test_node = literal
            if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                return test_node

        if isinstance(node, (exp.EQ, exp.NEQ, exp.GT, exp.LT, exp.GTE, exp.LTE)):
            for side in [node.left, node.right]:
                test_node = side
                if test_reduced_node(
                    test_node, test_script, full_statements, stmt_index
                ):
                    return test_node

    return node


def simplify_subquery_expressions(node, test_script, full_statements, stmt_index):
    if isinstance(node, exp.Select):
        if node.args.get("order") or node.args.get("limit") or node.args.get("offset"):
            test_node = copy.deepcopy(node)
            test_node.set("order", None)
            test_node.set("limit", None)
            test_node.set("offset", None)
            if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                return test_node

        test_node = exp.Select(
            expressions=[exp.Boolean(this=True)], from_=node.args.get("from")
        )
        if test_reduced_node(test_node, test_script, full_statements, stmt_index):
            return test_node

    return node


def simplify_where_clauses(statements, test_script):
    for i, stmt in enumerate(statements):
        if isinstance(stmt, exp.Select) and stmt.args.get("where"):
            test_stmt = copy.deepcopy(stmt)
            test_stmt.set("where", None)
            test_statements = statements.copy()
            test_statements[i] = test_stmt

            try:
                sql = get_query_from_parsed(test_statements)
                if test_query(sql, test_script):
                    statements = test_statements
                    continue
            except Exception:
                pass

            for node in stmt.args["where"].walk():
                if isinstance(node, exp.Case):
                    test_stmt = copy.deepcopy(stmt)
                    test_stmt.set("where", exp.Where(this=node))
                    test_statements = statements.copy()
                    test_statements[i] = test_stmt

                    try:
                        sql = get_query_from_parsed(test_statements)
                        if test_query(sql, test_script):
                            statements = test_statements
                            break
                    except Exception:
                        pass

    return statements


def simplify_case_expressions(node, test_script, full_statements, stmt_index):
    if isinstance(node, exp.Case):
        if node.args.get("default"):
            test_node = copy.deepcopy(node)
            test_node = node.args["default"]
            if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                return test_node

        for literal in [exp.Boolean(this=True), exp.Boolean(this=False)]:
            test_node = literal
            if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                return test_node

        if node.args.get("ifs"):
            for when_clause in node.args["ifs"]:
                if hasattr(when_clause, "this") and hasattr(when_clause, "result"):
                    test_node = when_clause.result
                    if test_reduced_node(
                        test_node, test_script, full_statements, stmt_index
                    ):
                        return test_node

        if node.args.get("ifs"):
            for i, when_clause in enumerate(node.args["ifs"]):
                if isinstance(when_clause.this, exp.Case):
                    test_node = copy.deepcopy(node)
                    test_ifs = test_node.args["ifs"]
                    test_ifs[i].set("this", exp.Boolean(this=True))
                    if test_reduced_node(
                        test_node, test_script, full_statements, stmt_index
                    ):
                        return test_node

    return node


def reduce_select_columns(statements, test_script):
    def find_dependencies(expr, deps=None):
        if deps is None:
            deps = set()

        if isinstance(expr, exp.Column):
            deps.add(str(expr.name))
            if expr.args.get("table"):
                table = str(expr.args["table"])
                deps.add(f"{table}.{expr.name}")
        elif isinstance(expr, exp.Alias):
            deps.add(str(expr.alias))
            if hasattr(expr.this, "walk"):
                for node in expr.this.walk():
                    if isinstance(node, exp.Column):
                        deps.add(str(node.name))
                        if node.args.get("table"):
                            table = str(node.args["table"])
                            deps.add(f"{table}.{node.name}")
        elif isinstance(expr, exp.Binary):
            if hasattr(expr, "left"):
                deps.update(find_dependencies(expr.left))
            if hasattr(expr, "right"):
                deps.update(find_dependencies(expr.right))
        elif hasattr(expr, "walk"):
            for node in expr.walk():
                if isinstance(node, exp.Column):
                    deps.add(str(node.name))
                    if node.args.get("table"):
                        table = str(node.args["table"])
                        deps.add(f"{table}.{node.name}")

        return deps

    def is_expr_needed(expr, col_deps, where_deps, order_deps):
        if expr_deps := find_dependencies(expr):
            if expr_deps & (where_deps | order_deps | col_deps):
                return True

        if isinstance(expr, exp.Alias):
            alias = str(expr.alias)
            if alias in col_deps:
                return True

        if isinstance(expr, (exp.Case, exp.Binary, exp.Func)):
            return True

        if isinstance(expr, exp.Column):
            return True

        return False

    new_statements = []
    modified = False

    for stmt in statements:
        if isinstance(stmt, exp.Select):
            if stmt.args.get("expressions"):
                all_deps = set()

                if stmt.args.get("where"):
                    for node in stmt.args["where"].walk():
                        all_deps.update(find_dependencies(node))

                if stmt.args.get("order"):
                    for expr in stmt.args["order"].expressions:
                        all_deps.update(find_dependencies(expr.this))

                for expr in stmt.args["expressions"]:
                    all_deps.update(find_dependencies(expr))

                expressions = stmt.args["expressions"]
                kept_exprs = []
                for expr in expressions:
                    if is_expr_needed(expr, all_deps, all_deps, all_deps):
                        kept_exprs.append(expr)

                if len(kept_exprs) > 0 and len(kept_exprs) < len(expressions):
                    test_stmt = copy.deepcopy(stmt)
                    test_stmt.set("expressions", kept_exprs)
                    test_statements = [
                        test_stmt if s == stmt else s for s in statements
                    ]
                    try:
                        sql = get_query_from_parsed(test_statements)
                        if test_query(sql, test_script):
                            stmt = test_stmt
                            modified = True
                    except Exception:
                        pass

        new_statements.append(stmt)

    return new_statements if modified else statements


def aggressively_flatten_subqueries(node, test_script, full_statements, stmt_index):
    if isinstance(node, exp.Select):
        if node.args.get("from") and isinstance(node.args["from"].this, exp.Subquery):
            inner_select = node.args["from"].this.this
            test_node = copy.deepcopy(node)
            test_node.set("from", inner_select.args.get("from"))
            if test_reduced_node(test_node, test_script, full_statements, stmt_index):
                return test_node

        if node.args.get("from") and isinstance(node.args["from"].this, exp.Subquery):
            subq = node.args["from"].this.this
            if isinstance(subq, exp.Select) and subq.args.get("where"):
                if node.args.get("where"):
                    test_node = copy.deepcopy(node)
                    test_node.set(
                        "where", exp.And(this=[node.args["where"], subq.args["where"]])
                    )
                    if test_reduced_node(
                        test_node, test_script, full_statements, stmt_index
                    ):
                        return test_node
                else:
                    test_node = copy.deepcopy(node)
                    test_node.set("where", subq.args["where"])
                    if test_reduced_node(
                        test_node, test_script, full_statements, stmt_index
                    ):
                        return test_node

    return node


def flatten_subqueries(statements, test_script):
    new_statements = []
    modified = False

    for stmt in statements:
        if isinstance(stmt, exp.Select):
            node = copy.deepcopy(stmt)
            if node.args.get("from"):
                from_clause = node.args["from"]
                if isinstance(from_clause, exp.From) and isinstance(
                    from_clause.this, exp.Subquery
                ):
                    subq = from_clause.this.this
                    if (
                        isinstance(subq, exp.Select)
                        and not subq.args.get("group")
                        and not subq.args.get("having")
                    ):
                        if node.args.get("where") and subq.args.get("where"):
                            new_where = exp.And(
                                this=[node.args["where"], subq.args["where"]]
                            )
                            node.set("where", new_where)
                        elif subq.args.get("where"):
                            node.set("where", subq.args["where"])

                        if subq.args.get("from"):
                            node.set("from", subq.args["from"])
                            modified = True
            new_statements.append(node)
        else:
            new_statements.append(stmt)

    if modified:
        try:
            sql = get_query_from_parsed(new_statements)
            if test_query(sql, test_script):
                return new_statements
        except Exception:
            pass

    return statements


def remove_unused_ctes(statements, test_script):
    new_statements = []
    modified = False

    for stmt in statements:
        if isinstance(stmt, exp.Select) and stmt.args.get("with"):
            node = copy.deepcopy(stmt)
            used_ctes = set()

            def find_cte_refs(select_node):
                for subnode in select_node.walk():
                    if isinstance(subnode, exp.Table):
                        if hasattr(subnode, "name"):
                            table_name = str(subnode.name).lower()
                            if table_name.startswith("cte"):
                                used_ctes.add(table_name)

            find_cte_refs(node)

            ctes = node.args["with"].expressions
            kept_ctes = []
            for cte in ctes:
                cte_name = str(cte.alias).lower()
                if cte_name in used_ctes:
                    kept_ctes.append(cte)
                    find_cte_refs(cte.this)

            if not kept_ctes:
                node.set("with", None)
                modified = True
            elif len(kept_ctes) < len(ctes):
                node.args["with"].set("expressions", kept_ctes)
                modified = True

            new_statements.append(node)
        else:
            new_statements.append(stmt)

    if modified:
        try:
            sql = get_query_from_parsed(new_statements)
            if test_query(sql, test_script):
                return new_statements
        except Exception:
            pass

    return statements


def get_query_from_parsed(parsed_statements):
    if not parsed_statements:
        return ""

    sql_string = (
        ";\n".join(stmt.sql(normalize=True, pad=0) for stmt in parsed_statements) + ";"
    )

    sql_string = re.sub(r"BLOB([A-Fa-f0-9]*)BLOB", r"X'\1'", sql_string)
    sql_string = re.sub(r"blob([A-Fa-f0-9]*)blob", r"X'\1'", sql_string)
    sql_string = re.sub(r"\b0\s+AS\s+(x\w*)\b", r"0\1", sql_string, flags=re.IGNORECASE)
    sql_string = re.sub(r"\bCURRENT_TIMESTAMP\(\)", "CURRENT_TIMESTAMP", sql_string)
    return sql_string


def test_query(query: str, test_script: str) -> bool:
    try:
        test_case_location = os.environ.get("TEST_CASE_LOCATION")
        if not test_case_location:
            test_case_location = os.path.join(os.getcwd(), "query.sql")

        with open(test_case_location, "w") as f:
            f.write(query)

        result = subprocess.run(
            ["bash", test_script],
            capture_output=True,
            text=True,
            timeout=30,
            env=os.environ.copy(),
        )

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False


def reduce_sql_query(sql_query: str, test_script: str) -> str:
    try:
        sql_query = re.sub(
            r"OVER\s*\(\s*RA[^)]*\)", "OVER()", sql_query, flags=re.IGNORECASE
        )
        sql_query = re.sub(r"x'([^']*)'", r"BLOB\1BLOB", sql_query, flags=re.IGNORECASE)
        sql_query = re.sub(
            r"\bREPLACE\s+INTO\b",
            "INSERT OR REPLACE INTO",
            sql_query,
            flags=re.IGNORECASE,
        )
        sql_query = re.sub(
            r"\bINSERT\s+OR\s+INSERT\s+OR\s+REPLACE\s+INTO\b",
            "INSERT OR REPLACE INTO",
            sql_query,
            flags=re.IGNORECASE,
        )
        lines = sql_query.strip().split("\n")
        if lines and lines[0].strip().lower().startswith(".mode"):
            sql_query = "\n".join(lines[1:])
        parsed_statements = parse(sql_query, error_level="ignore")

        if not parsed_statements:
            return sql_query
    except Exception as e:
        print(f"Parse error: {e}")
        return sql_query

    parsed_statements = [stmt for stmt in parsed_statements if stmt is not None]

    prev_token_count = count_tokens(sql_query)
    max_iterations = 7

    print(f"\033[91mOriginal query has {prev_token_count} tokens\033[0m\n", sql_query)

    for iteration in range(max_iterations):
        backup_statements = copy.deepcopy(parsed_statements)
        parsed_statements = reduce_unused_table_inserts(parsed_statements, test_script)
        if not test_query(get_query_from_parsed(parsed_statements), test_script):
            parsed_statements = copy.deepcopy(backup_statements)

        backup_statements = copy.deepcopy(parsed_statements)
        parsed_statements = simplify_boolean_literals(parsed_statements, test_script)
        if not test_query(get_query_from_parsed(parsed_statements), test_script):
            parsed_statements = copy.deepcopy(backup_statements)

        backup_statements = copy.deepcopy(parsed_statements)
        parsed_statements = reduce_insert_statements_aggressively(
            parsed_statements, test_script
        )
        if not test_query(get_query_from_parsed(parsed_statements), test_script):
            parsed_statements = copy.deepcopy(backup_statements)

        backup_statements = copy.deepcopy(parsed_statements)
        parsed_statements = reduce_statements_aggressively(
            parsed_statements, test_script
        )
        if not test_query(get_query_from_parsed(parsed_statements), test_script):
            parsed_statements = copy.deepcopy(backup_statements)

        backup_statements = copy.deepcopy(parsed_statements)
        parsed_statements = reduce_columns_minimally(parsed_statements, test_script)
        if not test_query(get_query_from_parsed(parsed_statements), test_script):
            parsed_statements = copy.deepcopy(backup_statements)

        backup_statements = copy.deepcopy(parsed_statements)
        parsed_statements = eliminate_unused_tables(parsed_statements, test_script)
        if not test_query(get_query_from_parsed(parsed_statements), test_script):
            parsed_statements = copy.deepcopy(backup_statements)

        backup_statements = copy.deepcopy(parsed_statements)
        parsed_statements = simplify_join_conditions(parsed_statements, test_script)
        if not test_query(get_query_from_parsed(parsed_statements), test_script):
            parsed_statements = copy.deepcopy(backup_statements)

        backup_statements = copy.deepcopy(parsed_statements)
        parsed_statements = reduce_select_columns(parsed_statements, test_script)
        if not test_query(get_query_from_parsed(parsed_statements), test_script):
            parsed_statements = copy.deepcopy(backup_statements)

        backup_statements = copy.deepcopy(parsed_statements)
        parsed_statements = flatten_subqueries(parsed_statements, test_script)
        if not test_query(get_query_from_parsed(parsed_statements), test_script):
            parsed_statements = copy.deepcopy(backup_statements)

        backup_statements = copy.deepcopy(parsed_statements)
        parsed_statements = remove_unused_ctes(parsed_statements, test_script)
        if not test_query(get_query_from_parsed(parsed_statements), test_script):
            parsed_statements = copy.deepcopy(backup_statements)

        backup_statements = copy.deepcopy(parsed_statements)
        parsed_statements = delta_debug_statements(parsed_statements, test_script)
        if not test_query(get_query_from_parsed(parsed_statements), test_script):
            parsed_statements = copy.deepcopy(backup_statements)

        backup_statements = copy.deepcopy(parsed_statements)
        parsed_statements = simplify_sql_constants(parsed_statements, test_script)
        if not test_query(get_query_from_parsed(parsed_statements), test_script):
            parsed_statements = copy.deepcopy(backup_statements)

        backup_statements = copy.deepcopy(parsed_statements)
        parsed_statements = simplify_where_clauses(parsed_statements, test_script)
        if not test_query(get_query_from_parsed(parsed_statements), test_script):
            parsed_statements = copy.deepcopy(backup_statements)

        parsed_statements = [stmt for stmt in parsed_statements if stmt is not None]

        backup_statements = copy.deepcopy(parsed_statements)
        for i, stmt in enumerate(parsed_statements):
            if stmt is not None:
                reduced_stmt = reduce_node_aggressively(
                    stmt, test_script, backup_statements, i
                )
                if not expressions_equal(reduced_stmt, stmt):
                    test_statements = copy.deepcopy(backup_statements)
                    test_statements[i] = reduced_stmt
                    if test_query(get_query_from_parsed(test_statements), test_script):
                        parsed_statements[i] = reduced_stmt

        backup_statements = copy.deepcopy(parsed_statements)
        parsed_statements = reduce_create_table_columns(parsed_statements, test_script)
        if not test_query(get_query_from_parsed(parsed_statements), test_script):
            parsed_statements = copy.deepcopy(backup_statements)

        parsed_statements = [stmt for stmt in parsed_statements if stmt is not None]

        if not parsed_statements:
            break

        current_sql = get_query_from_parsed(parsed_statements)
        current_token_count = count_tokens(current_sql)

        print(
            f"\033[91mIteration {iteration} has {current_token_count} tokens\033[0m\n",
            current_sql,
        )

        if current_token_count >= prev_token_count:
            break

        prev_token_count = current_token_count

    reduced_statements = [stmt for stmt in parsed_statements if stmt is not None]

    if not reduced_statements:
        return sql_query

    reduced_sql = get_query_from_parsed(reduced_statements)
    return reduced_sql


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--test", required=True)

    args = parser.parse_args()

    try:
        with open(args.query, "r") as f:
            sql_query = f.read().strip()
    except Exception:
        sys.exit(1)

    reduced_query = reduce_sql_query(sql_query, args.test)
    test_case_location = os.environ.get("TEST_CASE_LOCATION")
    if not test_case_location:
        test_case_location = os.path.join(os.getcwd(), "query.sql")

    print("\033[92m\033[1mFINAL REDUCED QUERY:\033[0m\n", reduced_query)

    if not test_query(reduced_query, args.test):
        print(
            "\033[91m\033[1mWARNING: FINAL REDUCED QUERY DOES NOT TRIGGER THE BUG\033[0m"
        )

    with open(test_case_location, "w") as f:
        f.write(reduced_query)
