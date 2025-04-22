#!/usr/bin/env python3
import subprocess
import random
import string
import tempfile
import re

def random_string(length=1, include_special=False):
    """Generate a random string, optionally with special characters."""
    chars = string.ascii_letters + string.digits
    if include_special:
        chars += "_-$#@!%^&*()."
    return ''.join(random.choices(chars, k=length))

def random_hex_string(length):
    """Generate a valid hexadecimal string with even length."""
    hex_chars = "0123456789ABCDEF"
    # Ensure even length (each byte is 2 hex chars)
    if length % 2 != 0:
        length += 1
    return ''.join(random.choices(hex_chars, k=length))

def random_table_name():
    """Generate a random table name."""
    return f"t_{random_string(random.randint(3, 10))}"

def random_column_name():
    """Generate a random column name."""
    return f"c_{random_string(random.randint(3, 10))}"

def random_int(min_val=-1000000, max_val=1000000):
    """Generate a random integer."""
    return random.randint(min_val, max_val)

def random_float():
    """Generate a random float."""
    return random.uniform(-1000000, 1000000)

def random_value(include_null=True, hex_limit=8, data_type=None, is_unique=False, unique_id=0):
    """Generate a random value of various types, optionally making it more unique."""
    if include_null and random.random() < 0.1 and not is_unique:
        return "NULL"
    
    # If a specific data type is provided, generate appropriate values
    if data_type:
        if data_type == "INTEGER":
            # Ensure uniqueness by using the unique_id offset for UNIQUE columns
            offset = unique_id * 10000 if is_unique else 0
            return str(random_int() + offset)
        elif data_type == "REAL":
            offset = unique_id * 10.0 if is_unique else 0
            return str(random_float() + offset)
        elif data_type == "TEXT":
            # Add unique_id for uniqueness
            unique_suffix = f"_{unique_id}" if is_unique else ""
            return f"'{random_string(random.randint(1, 20))}{unique_suffix}'"
        elif data_type == "NUMERIC":
            offset = unique_id * 10000 if is_unique else 0
            return str(random_int() + offset)
        else:
            unique_suffix = f"_{unique_id}" if is_unique else ""
            return f"'{random_string(random.randint(1, 20))}{unique_suffix}'"
    
    # Default random types if no specific type is given
    value_types = [
        lambda: str(random_int()),
        lambda: str(random_float()),
        lambda: f"'{random_string(random.randint(1, 20), include_special=False)}'",
        lambda: f"x'{random_hex_string(random.randint(2, hex_limit))}'",  # hex blob
        lambda: f"'{random.choice(['true', 'false'])}'",
        lambda: f"'{random.randint(1900, 2100)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}'"  # date
    ]
    return random.choice(value_types)()

def random_data_type():
    """Return a random SQL data type."""
    types = ["INTEGER", "TEXT", "REAL", "NUMERIC"]  # Removed VARCHAR/CHAR for better compatibility
    return random.choice(types)

def generate_column_def():
    """Generate a random column definition."""
    col_name = random_column_name()
    data_type = random_data_type()
    
    # Don't include PRIMARY KEY in random constraints
    # We'll handle that separately in generate_create_table
    constraints = ["", "NOT NULL", "DEFAULT " + random_value(data_type=data_type), "UNIQUE"]
    constraint = random.choice(constraints) if random.random() < 0.3 else ""
    
    return col_name, data_type, f"{col_name} {data_type} {constraint}".strip()

def generate_create_table(table_name=None):
    """Generate a CREATE TABLE statement with random columns."""
    table = table_name if table_name else random_table_name()
    num_columns = random.randint(1, 10)
    column_defs = [generate_column_def() for _ in range(num_columns)]
    
    # Unpack column info
    column_names = [col[0] for col in column_defs]
    column_types = {col[0]: col[1] for col in column_defs}
    column_definitions = [col[2] for col in column_defs]
    
    # Occasionally add a foreign key
    if random.random() < 0.2 and num_columns > 1:
        ref_table = random_table_name()
        ref_col = random_column_name()
        fk_col = random.choice(column_names)
        fk = f", FOREIGN KEY ({fk_col}) REFERENCES {ref_table}({ref_col})"
    else:
        fk = ""
    
    # Add PRIMARY KEY to at most one column
    has_primary_key = False
    if random.random() < 0.4 and len(column_defs) > 0:  # 40% chance to have a PRIMARY KEY
        pk_idx = random.randrange(len(column_defs))
        col_name = column_names[pk_idx]
        col_def = column_definitions[pk_idx]
        # Remove any existing UNIQUE constraint to avoid conflict
        col_def = col_def.replace(" UNIQUE", "")
        column_definitions[pk_idx] = f"{col_def} PRIMARY KEY"
        has_primary_key = True
    
    # Make sure WITHOUT ROWID tables have a PRIMARY KEY
    without_rowid = ""
    if random.random() < 0.2 and has_primary_key:
        without_rowid = " WITHOUT ROWID"
        
    create_stmt = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(column_definitions)}{fk}){without_rowid};"
    return table, column_names, column_types, create_stmt

def generate_insert(table_name, column_names, column_types=None):
    """Generate an INSERT statement."""
    if not column_names:
        return f"-- Skipping INSERT for {table_name}: no columns"
    
    # Include all columns to avoid NOT NULL constraint issues
    selected_columns = column_names
    
    # Track NOT NULL constraints for these columns
    not_null_columns = []  # Add logic to populate this from your schema
    
    # Multiple row values
    num_rows = random.randint(1, 3)
    rows = []
    for i in range(num_rows):
        values = []
        for idx, col in enumerate(selected_columns):
            col_type = column_types.get(col) if column_types else None
            
            # Never generate NULL for NOT NULL columns
            include_null = col not in not_null_columns
            
            # Generate type-appropriate values with uniqueness
            values.append(random_value(include_null=include_null, data_type=col_type, 
                                      is_unique=True, unique_id=i*100+idx))
        
        rows.append(f"({', '.join(values)})")
    
    # Use INSERT OR IGNORE to handle constraint violations gracefully
    return f"INSERT OR IGNORE INTO {table_name} ({', '.join(selected_columns)}) VALUES {', '.join(rows)};"

def generate_select(table_name, column_names, column_types=None):
    """Generate a SELECT statement with various clauses."""
    if not column_names:
        return f"SELECT * FROM {table_name} ORDER BY 1;"
    
    column_types = column_types or {}
    
    # Generate column list - sometimes use * or add functions
    if random.random() < 0.2:
        columns = "*"
    else:
        # Make sure we have valid columns
        if not column_names:
            columns = "*"
        else:
            num_columns = min(random.randint(1, 5), len(column_names))
            selected_columns = random.sample(column_names, num_columns)
            col_list = []
            for col in selected_columns:
                col_type = column_types.get(col)
                
                # Sometimes apply a function appropriate for the column type
                if random.random() < 0.3:
                    if col_type in ("INTEGER", "REAL", "NUMERIC"):
                        # Numeric functions for numeric types
                        func = random.choice(["count", "sum", "avg", "max", "min"])
                        col_expr = f"{func}({col})"
                    elif col_type == "TEXT":
                        # Text functions for text types
                        func = random.choice(["count", "length", "upper", "lower"])
                        col_expr = f"{func}({col})"
                    else:
                        col_expr = col
                else:
                    col_expr = col
                    
                # Sometimes add an alias - AVOID using column names as aliases
                if random.random() < 0.3:
                    alias = f"alias_{random_string(3)}"  # Use 'alias_' prefix to avoid confusion
                    col_expr = f"{col_expr} AS {alias}"
                col_list.append(col_expr)
            columns = ", ".join(col_list)
    
    query = f"SELECT {columns} FROM {table_name}"
    
    # Add WHERE clause
    if random.random() < 0.7 and column_names:
        conditions = []
        # Always check that we have columns to use in conditions
        max_conditions = min(3, len(column_names))
        if max_conditions > 0:  # Only add WHERE if we have columns
            for _ in range(random.randint(1, max_conditions)):
                # Use only valid columns
                col = random.choice(column_names)
                col_type = column_types.get(col)
                
                # Choose operators appropriate for the column type
                if col_type in ("INTEGER", "REAL", "NUMERIC"):
                    op = random.choice(["=", ">", "<", ">=", "<=", "!=", "IS NULL", "IS NOT NULL"])
                    if op in ("IS NULL", "IS NOT NULL"):
                        condition = f"{col} {op}"
                    else:
                        # Use type-appropriate value for numeric comparisons
                        val = random_value(data_type=col_type)
                        condition = f"{col} {op} {val}"
                elif col_type == "TEXT":
                    op = random.choice(["=", "!=", "LIKE", "IS NULL", "IS NOT NULL"])
                    if op in ("IS NULL", "IS NOT NULL"):
                        condition = f"{col} {op}"
                    elif op == "LIKE":
                        patterns = [f"'%{random_string(3)}%'", f"'{random_string(3)}%'", f"'%{random_string(3)}'"]
                        condition = f"{col} LIKE {random.choice(patterns)}"
                    else:
                        # Text comparison
                        val = random_value(data_type="TEXT")
                        condition = f"{col} {op} {val}"
                else:
                    # Default for unknown types
                    op = random.choice(["=", "!=", "IS NULL", "IS NOT NULL"])
                    if op in ("IS NULL", "IS NOT NULL"):
                        condition = f"{col} {op}"
                    else:
                        val = random_value(include_null=False)
                        condition = f"{col} {op} {val}"
                
                conditions.append(condition)
        
            connectors = ["AND", "OR"]
            query += " WHERE " + (" " + random.choice(connectors) + " ").join(conditions)
    
    # Always add ORDER BY clause for consistent output ordering
    if column_names:
        # Choose a random column to order by
        order_col = random.choice(column_names)
        direction = random.choice(["ASC", "DESC"]) if random.random() < 0.5 else ""
        query += f" ORDER BY {order_col} {direction}"
    else:
        # If no specific columns are available, use ORDER BY with position
        query += " ORDER BY 1"
    
    return query + ";"

def generate_update(table_name, column_names, column_types=None):
    """Generate an UPDATE statement."""
    if not column_names:
        return f"-- Skipping UPDATE for {table_name}: no columns"
    
    column_types = column_types or {}
    
    num_sets = min(random.randint(1, 3), len(column_names))
    selected_columns = random.sample(column_names, num_sets)
    sets = []
    for col in selected_columns:
        col_type = column_types.get(col)
        val = random_value(data_type=col_type)
        sets.append(f"{col} = {val}")
    
    query = f"UPDATE {table_name} SET {', '.join(sets)}"
    
    # Add WHERE clause
    if random.random() < 0.8 and column_names:  # Usually include a WHERE clause for safety
        col = random.choice(column_names)
        col_type = column_types.get(col)
        
        # Choose operators appropriate for the column type
        if col_type in ("INTEGER", "REAL", "NUMERIC"):
            op = random.choice(["=", ">", "<", ">=", "<=", "!="])
            val = random_value(data_type=col_type)
        elif col_type == "TEXT":
            op = random.choice(["=", "!=", "LIKE"])
            if op == "LIKE":
                patterns = [f"'%{random_string(3)}%'", f"'{random_string(3)}%'", f"'%{random_string(3)}'"]
                val = random.choice(patterns)
            else:
                val = random_value(data_type="TEXT")
        else:
            op = random.choice(["=", "!="])
            val = random_value()
        
        query += f" WHERE {col} {op} {val}"
    
    return query + ";"

def generate_delete(table_name, column_names, column_types=None):
    """Generate a DELETE statement."""
    query = f"DELETE FROM {table_name}"
    
    column_types = column_types or {}
    
    # Add WHERE clause (almost always for safety)
    if random.random() < 0.9 and column_names:
        col = random.choice(column_names)
        col_type = column_types.get(col)
        
        # Similar type-aware logic as update
        if col_type in ("INTEGER", "REAL", "NUMERIC"):
            op = random.choice(["=", ">", "<", ">=", "<=", "!="])
            val = random_value(data_type=col_type)
        elif col_type == "TEXT":
            op = random.choice(["=", "!="])
            val = random_value(data_type="TEXT")
        else:
            op = random.choice(["=", "!="])
            val = random_value()
        
        query += f" WHERE {col} {op} {val}"
    
    return query + ";"

def generate_alter_table(table_name, column_names, column_types=None):
    """Generate an ALTER TABLE statement compatible with both versions."""
    # Only use ADD COLUMN as it's supported in both versions
    data_type = random_data_type()
    # Avoid generated columns and other newer features
    return f"ALTER TABLE {table_name} ADD COLUMN {random_column_name()} {data_type};"

def generate_index(table_name, column_names, column_types=None):
    """Generate a CREATE INDEX statement."""
    if not column_names:
        return f"-- Skipping INDEX for {table_name}: no columns"
        
    index_name = f"idx_{random_string(5)}"
    
    # Generate columns, optionally with collations
    num_cols = min(random.randint(1, 3), len(column_names))
    selected_columns = random.sample(column_names, num_cols)
    index_columns = []
    
    for col in selected_columns:
        col_type = column_types.get(col) if column_types else None
        
        # Add COLLATE only for TEXT columns
        if col_type == "TEXT" and random.random() < 0.3:
            collation = random.choice(["BINARY", "NOCASE", "RTRIM"])
            index_col = f"{col} COLLATE {collation}"
        else:
            index_col = col
        index_columns.append(index_col)
    
    # Less chance for UNIQUE to avoid constraint violations
    unique = "UNIQUE " if random.random() < 0.2 else ""
    return f"CREATE {unique}INDEX IF NOT EXISTS {index_name} ON {table_name}({', '.join(index_columns)});"

def generate_transaction(tables_info):
    """Generate a transaction with multiple statements."""
    if not tables_info:
        return "BEGIN TRANSACTION;\nSELECT 1;\nCOMMIT;"
    
    num_statements = random.randint(2, 5)
    statements = []
    
    for _ in range(num_statements):
        table_name = random.choice(list(tables_info.keys()))
        column_names = tables_info[table_name]["columns"]
        column_types = tables_info[table_name]["types"]
        
        if random.random() < 0.5:
            statements.append(generate_insert(table_name, column_names, column_types))
        else:
            statements.append(generate_update(table_name, column_names, column_types))
    
    return "BEGIN TRANSACTION;\n" + "\n".join(statements) + "\nCOMMIT;"

def generate_join_query(tables_info):
    """Generate a query with JOINs."""
    if len(tables_info) < 2:
        # Fall back to simple select if not enough tables
        if tables_info:
            table_name = next(iter(tables_info.keys()))
            column_names = tables_info[table_name]["columns"]
            column_types = tables_info[table_name]["types"]
            return generate_select(table_name, column_names, column_types)
        return "SELECT 1 ORDER BY 1;"
    
    # Select two tables
    table_names = list(tables_info.keys())
    table1, table2 = random.sample(table_names, 2)
    cols1 = tables_info[table1]["columns"]
    cols2 = tables_info[table2]["columns"]
    types1 = tables_info[table1]["types"]
    types2 = tables_info[table2]["types"]
    
    if not cols1 or not cols2:
        # Fall back if either table has no columns
        if cols1:
            return generate_select(table1, cols1, types1)
        if cols2:
            return generate_select(table2, cols2, types2)
        return "SELECT 1 ORDER BY 1;"
    
    join_types = ["JOIN", "LEFT JOIN", "INNER JOIN", "CROSS JOIN"]
    join_type = random.choice(join_types)
    
    col1 = random.choice(cols1)
    col2 = random.choice(cols2)
    
    query = f"SELECT {table1}.{col1}, {table2}.{col2} FROM {table1}"
    
    if join_type == "CROSS JOIN":
        query += f" {join_type} {table2}"
    else:
        # Try to match compatible types for join conditions
        type1 = types1.get(col1)
        type2 = types2.get(col2)
        
        # If types are not compatible, use CROSS JOIN instead
        if type1 and type2 and type1 != type2 and not (
            type1 in ["INTEGER", "REAL", "NUMERIC"] and 
            type2 in ["INTEGER", "REAL", "NUMERIC"]
        ):
            query += f" CROSS JOIN {table2}"
        else:
            query += f" {join_type} {table2} ON {table1}.{col1} = {table2}.{col2}"
    
    # Add ORDER BY clause for consistent results
    query += f" ORDER BY {table1}.{col1}"
    
    return query + ";"

def generate_subquery(tables_info):
    """Generate a query with a subquery."""
    if not tables_info:
        return "SELECT 1 ORDER BY 1;"
    
    # Select one or two tables
    table_names = list(tables_info.keys())
    if len(table_names) >= 2 and random.random() < 0.5:
        table, inner_table = random.sample(table_names, 2)
    else:
        table = random.choice(table_names)
        inner_table = table
    
    cols = tables_info[table]["columns"]
    inner_cols = tables_info[inner_table]["columns"]
    types = tables_info[table]["types"]
    inner_types = tables_info[inner_table]["types"]
    
    if not cols or not inner_cols:
        # Fall back if no columns
        table_with_cols = next((t for t, info in tables_info.items() if info["columns"]), None)
        if table_with_cols:
            return generate_select(
                table_with_cols, 
                tables_info[table_with_cols]["columns"],
                tables_info[table_with_cols]["types"]
            )
        return "SELECT 1 ORDER BY 1;"
    
    col = random.choice(cols)
    inner_col = random.choice(inner_cols)
    
    # Check for compatible types
    col_type = types.get(col)
    inner_col_type = inner_types.get(inner_col)
    
    # Use a type-compatible approach for subqueries
    if col_type and inner_col_type and (col_type == inner_col_type or (
        col_type in ["INTEGER", "REAL", "NUMERIC"] and 
        inner_col_type in ["INTEGER", "REAL", "NUMERIC"]
    )):
        subquery_types = [
            f"WHERE {col} IN (SELECT {inner_col} FROM {inner_table})",
            f"WHERE {col} = (SELECT {inner_col} FROM {inner_table} LIMIT 1)"
        ]
    else:
        # If types are incompatible, use EXISTS which doesn't compare values
        subquery_types = [
            f"WHERE EXISTS (SELECT 1 FROM {inner_table})"
        ]
    
    return f"SELECT * FROM {table} {random.choice(subquery_types)} ORDER BY {col};"

def generate_view(tables_info):
    """Generate a CREATE VIEW statement."""
    if not tables_info:
        return "SELECT 1;"
    
    # Select a table with columns
    table_with_cols = next((t for t, info in tables_info.items() if info["columns"]), None)
    if not table_with_cols:
        return "SELECT 1;"
    
    table = table_with_cols
    cols = tables_info[table]["columns"]
    
    view_name = f"view_{random_string(5)}"
    # Select a subset of columns
    num_cols = min(random.randint(1, 3), len(cols))
    selected_cols = random.sample(cols, num_cols)
    
    return f"CREATE VIEW IF NOT EXISTS {view_name} AS SELECT {', '.join(selected_cols)} FROM {table};"

def generate_trigger(tables_info):
    """Generate a CREATE TRIGGER statement."""
    if not tables_info:
        return "SELECT 1;"
    
    # Select a table with columns
    table_with_cols = next((t for t, info in tables_info.items() if info["columns"]), None)
    if not table_with_cols:
        return "SELECT 1;"
    
    table = table_with_cols
    cols = tables_info[table]["columns"]
    
    trigger_name = f"trig_{random_string(5)}"
    events = ["INSERT", "UPDATE", "DELETE"]
    event = random.choice(events)
    timings = ["BEFORE", "AFTER"]
    timing = random.choice(timings)
    
    # Create another table for the action
    action_table = random_table_name()
    action_col = random_column_name()
    
    # Include creation of the action table
    action_table_sql = f"CREATE TABLE IF NOT EXISTS {action_table} ({action_col} TEXT);"
    
    if event == "INSERT" and cols:
        col = random.choice(cols)
        action = f"INSERT INTO {action_table} ({action_col}) VALUES (NEW.{col})"
    elif event == "UPDATE" and cols:
        col = random.choice(cols)
        action = f"UPDATE {action_table} SET {action_col} = NEW.{col}"
    else:  # DELETE
        if cols:
            col = random.choice(cols)
            action = f"DELETE FROM {action_table} WHERE {action_col} = OLD.{col}"
        else:
            action = f"DELETE FROM {action_table}"
    
    return f"{action_table_sql}\nCREATE TRIGGER IF NOT EXISTS {trigger_name} {timing} {event} ON {table} BEGIN {action}; END;"

def generate_with_clause(tables_info):
    """Generate a query with a WITH clause (Common Table Expression)."""
    if not tables_info:
        return "SELECT 1 ORDER BY 1;"
    
    # Select a table with columns
    table_with_cols = next((t for t, info in tables_info.items() if info["columns"]), None)
    if not table_with_cols:
        return "SELECT 1 ORDER BY 1;"
    
    table = table_with_cols
    cols = tables_info[table]["columns"]
    
    if not cols:
        return "SELECT 1 ORDER BY 1;"
    
    cte_name = f"cte_{random_string(3)}"
    col = random.choice(cols)
    # Avoid recursive CTEs as they have different implementations
    return f"WITH {cte_name} AS (SELECT {col} FROM {table}) SELECT * FROM {cte_name} ORDER BY {col};"

def generate_union_query(tables_info):
    """Generate a UNION query."""
    if len(tables_info) < 2:
        # Fall back to simple select if not enough tables
        if tables_info:
            table_name = next(iter(tables_info.keys()))
            column_names = tables_info[table_name]["columns"]
            column_types = tables_info[table_name]["types"]
            return generate_select(table_name, column_names, column_types)
        return "SELECT 1 ORDER BY 1;"
    
    # Find two tables with columns
    tables_with_cols = [(t, info["columns"], info["types"]) for t, info in tables_info.items() if info["columns"]]
    if len(tables_with_cols) < 2:
        # Fall back if not enough tables with columns
        if tables_with_cols:
            return generate_select(tables_with_cols[0][0], tables_with_cols[0][1], tables_with_cols[0][2])
        return "SELECT 1 ORDER BY 1;"
    
    table1, cols1, types1 = random.choice(tables_with_cols)
    table2, cols2, types2 = random.choice(tables_with_cols)
    
    set_operators = ["UNION", "UNION ALL", "INTERSECT", "EXCEPT"]
    operator = random.choice(set_operators)
    
    col1 = random.choice(cols1)
    col2 = random.choice(cols2)
    
    # Check for compatible types for set operations
    type1 = types1.get(col1)
    type2 = types2.get(col2)
    
    # If types are not compatible, use count(*) to ensure int-int comparison
    if type1 and type2 and type1 != type2 and not (
        type1 in ["INTEGER", "REAL", "NUMERIC"] and 
        type2 in ["INTEGER", "REAL", "NUMERIC"]
    ):
        return f"SELECT COUNT(*) FROM {table1} {operator} SELECT COUNT(*) FROM {table2} ORDER BY 1;"
    
    return f"SELECT {col1} FROM {table1} {operator} SELECT {col2} FROM {table2} ORDER BY 1;"

def generate_pragma():
    """Generate a random PRAGMA statement."""
    # Common pragmas to test (some read-only, some modifiable)
    pragmas = [
        # Core functionality
        "integrity_check",
        "foreign_keys",
        "case_sensitive_like",
        "ignore_check_constraints",
        "defer_foreign_keys",
        
        # Storage and memory settings
        "journal_mode",
        "synchronous", 
        "cache_size",
        "page_size",
        "mmap_size",
        
        # Query-related
        "temp_store",
        "secure_delete",
        "recursive_triggers",
        "auto_vacuum",
        "locking_mode"
    ]
    
    pragma = random.choice(pragmas)
    
    # For read-only pragmas, just return simple query
    if pragma in ["integrity_check", "foreign_key_check", "quick_check"]:
        return f"PRAGMA {pragma};"
    
    # For setting pragmas, choose appropriate values based on the pragma type
    if random.random() < 0.7:  # 70% chance to just query the value
        return f"PRAGMA {pragma};"
    else:  # 30% chance to set the value
        if pragma == "journal_mode":
            value = random.choice(["DELETE", "TRUNCATE", "PERSIST", "MEMORY", "WAL", "OFF"])
        elif pragma == "synchronous":
            value = random.choice(["0", "1", "2", "OFF", "NORMAL", "FULL"])
        elif pragma == "temp_store":
            value = random.choice(["0", "1", "2", "DEFAULT", "FILE", "MEMORY"])
        elif pragma == "locking_mode":
            value = random.choice(["NORMAL", "EXCLUSIVE"])
        elif pragma == "auto_vacuum":
            value = random.choice(["0", "1", "2", "NONE", "FULL", "INCREMENTAL"])
        elif pragma in ["foreign_keys", "case_sensitive_like", "defer_foreign_keys", 
                        "ignore_check_constraints", "recursive_triggers", "secure_delete"]:
            value = random.choice(["0", "1", "true", "false", "on", "off"])
        elif pragma in ["cache_size", "page_size", "mmap_size"]:
            # Memory-related settings
            multiplier = 1024 if random.random() < 0.5 else 1
            value = str(random.randint(1, 100) * multiplier)
        else:
            # Default to 0/1 for unknown pragmas
            value = random.choice(["0", "1"])
            
        return f"PRAGMA {pragma} = {value};"

def generate_test_case():
    """Generate a complete test case with tables, data, and queries."""
    # First, generate 1-3 random tables
    num_tables = random.randint(1, 3)
    tables_info = {}  # {table_name: {"columns": [column_names], "types": {col_name: type}}}
    statements = []
    
    # Sometimes add initial PRAGMA statements
    if random.random() < 0.3:  # 30% chance to add pragma at the beginning
        statements.append(generate_pragma())
    
    # Create tables and populate tables_info
    for _ in range(num_tables):
        table_name, column_names, column_types, create_stmt = generate_create_table()
        statements.append(create_stmt)
        tables_info[table_name] = {"columns": column_names, "types": column_types}
    
    # Insert data into each table
    for table_name, table_data in tables_info.items():
        column_names = table_data["columns"]
        column_types = table_data["types"]
        # Insert 1-5 rows
        num_rows = random.randint(1, 5)
        for _ in range(num_rows):
            statements.append(generate_insert(table_name, column_names, column_types))
    
    # Define query generators that use our tables_info
    query_generators = []
    
    # Add PRAGMA generator
    query_generators.append(generate_pragma)
    
    # Only add generators if we have tables
    if tables_info:
        # For each query type, use a consistent table selection
        for _ in range(3):  # Add multiple instances to increase variety
            # Select a random table first, then use it consistently
            table_name = random.choice(list(tables_info.keys()))
            column_names = tables_info[table_name]["columns"]
            column_types = tables_info[table_name]["types"]
            
            # Only add if the table has columns
            if column_names:
                query_generators.extend([
                    lambda t=table_name, c=column_names, ct=column_types: generate_select(t, c, ct),
                    lambda t=table_name, c=column_names, ct=column_types: generate_update(t, c, ct),
                    lambda t=table_name, c=column_names, ct=column_types: generate_delete(t, c, ct),
                    lambda t=table_name, c=column_names, ct=column_types: generate_index(t, c, ct),
                    lambda t=table_name, c=column_names, ct=column_types: generate_alter_table(t, c, ct)
                ])
        
        # Only add complex queries if we actually have tables with columns
        tables_with_columns = [t for t, info in tables_info.items() if info["columns"]]
        if tables_with_columns:
            query_generators.extend([
                lambda: generate_join_query(tables_info),
                lambda: generate_subquery(tables_info),
                lambda: generate_with_clause(tables_info),
                lambda: generate_union_query(tables_info),
                lambda: generate_view(tables_info),
                lambda: generate_trigger(tables_info),
                lambda: generate_transaction(tables_info)
            ])
    else:
        # If no tables, just use a simple query
        query_generators.append(lambda: "SELECT 1;")
    
    # Add 2-5 random queries
    num_queries = random.randint(2, 5)
    for _ in range(num_queries):
        query_generator = random.choice(query_generators)
        statements.append(query_generator())
    
    # Sometimes add PRAGMA integrity_check at the end
    if random.random() < 0.2:  # 20% chance
        statements.append("PRAGMA integrity_check;")
    
    # Add a simple query that will definitely produce output
    if tables_info:
        table_name = random.choice(list(tables_info.keys()))
        statements.append(f"SELECT COUNT(*) FROM {table_name} ORDER BY 1;")
    else:
        statements.append("SELECT 1 ORDER BY 1;")
    
    # Combine all statements
    return "\n".join(statements)

def compare_results(out_old, err_old, out_new, err_new):
    """Better detection of significant differences."""
    # Simple string comparison
    if out_old != out_new:
        print("Output different!")
        return True
    
    if err_old != "" and err_new == "":
        print("Old gives error but new not!")
        return True
        
    if err_old and err_new:
            # Split error messages into lines to handle multi-line errors
            err_old_lines = err_old.strip().split('\n')
            err_new_lines = err_new.strip().split('\n')
            
            # First check if line counts differ
            if len(err_old_lines) != len(err_new_lines):
                print("Different number of error lines!")
                return True
            
            # Compare corresponding lines
            for i in range(len(err_old_lines)):
                line_old = err_old_lines[i]
                line_new = err_new_lines[i]
                
                # Extract parts based on colon separator
                err_old_parts = line_old.split(': ')
                old_message = err_old_parts[2] if len(err_old_parts) > 2 else line_old
                old_message = old_message.strip()
                
                err_new_parts = line_new.split(': ')
                new_message = err_new_parts[1] if len(err_new_parts) > 1 else line_new
                new_message = new_message.split('(')[0]  # Remove any additional info after '('
                new_message = new_message.strip()
                
                # If corresponding lines have different core error messages, report a difference
                if old_message and new_message and old_message != new_message:
                    print()
                    print(old_message)
                    print(new_message)
                    print("Error messages different!")
                    return True
            
            # If one has an error and the other doesn't, that's a difference
            if bool(err_old.strip()) != bool(err_new.strip()):
                print("Error presence different!")
                return True
    
    return False
    

def run_sqlite(version_path, sql):
    try:
        with tempfile.NamedTemporaryFile() as tmpdb:
            cmd = [version_path, tmpdb.name]
            result = subprocess.run(
                cmd, input=sql.encode(), capture_output=True, timeout=5
            )
            # Add error handling to prevent UTF-8 decode errors
            stdout = result.stdout.decode(errors='replace')
            stderr = result.stderr.decode(errors='replace')
            return stdout, stderr
    except Exception as e:
        return "", str(e)

def main():
    # Generate a complete test case with table creation, data insertion, and queries
    sql = generate_test_case()
    
    # Run against both SQLite versions
    out_old, err_old = run_sqlite("/usr/bin/sqlite3-3.26.0", sql)
    out_new, err_new = run_sqlite("/usr/bin/sqlite3-3.39.4", sql)

    # More sophisticated comparison
    if compare_results(out_old, err_old, out_new, err_new):
        print("❗ Difference found!")
        print("SQL:")
        print(sql)
        print("--- v3.26.0 ---")
        print("OUT:", out_old)
        print("ERR:", err_old)
        print("--- v3.39.4 ---")
        print("OUT:", out_new)
        print("ERR:", err_new)
        print("---------------------")

if __name__ == "__main__":
    try:
        for i in range(10000):  # Run multiple iterations
            if i % 100 == 0:
                print(f"\rIteration {i}", end="", flush=True)
            main()
    except KeyboardInterrupt:
        print("\nFuzzing stopped by user")