import random
import string

def likelihood_handler(args):
    """Special handler for LIKELIHOOD function arguments."""
    return [args[0], str(random.uniform(0.0, 1.0))]

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

def random_float(min_val=-1000000, max_val=1000000):
    """Generate a random float."""
    return random.uniform(min_val, max_val)

def random_value(is_not_null=True, hex_limit=8, data_type=None, is_unique=False, min=None, max=None, unique_id=0):
    """Generate a random value of various types, optionally making it more unique."""
    if not is_not_null and random.random() < 0.1 and not is_unique:
        return "NULL"
    
    if min == None:
        min = -1000000
    if max == None:
        max = 1000000
    
    # If a specific data type is provided, generate appropriate values
    if data_type:
        if data_type == "INTEGER":
            # Ensure uniqueness by using the unique_id offset for UNIQUE columns
            offset = unique_id * 10000 if is_unique else 1
            return str(random_int(min, max) + offset)
        elif data_type == "REAL":
            offset = unique_id * 10.0 if is_unique else 1
            return str(random_float(min, max) + offset)
        elif data_type == "TEXT":
            # Add unique_id for uniqueness
            unique_suffix = f"_{unique_id}" if is_unique else ""
            return f"'{random_string(random.randint(1, 20))}{unique_suffix}'"
        elif data_type == "NUMERIC":
            offset = unique_id * 10000 if is_unique else 1
            return str(random_int(min, max) + offset)
        elif data_type == "BLOB":
            return f"x'{random_hex_string(random.randint(2, hex_limit))}'"
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

class SQLiteGrammar:
    """Implements the formal SQLite grammar according to the ANTLR4 specification."""
    
    def __init__(self):
        # Keywords/tokens from lexer grammar
        self.keywords = [
            "ABORT", "ACTION", "ADD", "AFTER", "ALL", "ALTER", "ANALYZE", "AND", 
            "AS", "ASC", "ATTACH", "AUTOINCREMENT", "BEFORE", "BEGIN", "BETWEEN", 
            "BY", "CASCADE", "CASE", "CAST", "CHECK", "COLLATE", "COLUMN", "COMMIT", 
            "CONFLICT", "CONSTRAINT", "CREATE", "CROSS", "DATABASE", "DEFAULT", "DEFERRABLE", "DEFERRED", 
            "DELETE", "DESC", "DETACH", "DISTINCT", "DROP", "EACH", "ELSE", "END", 
            "ESCAPE", "EXCEPT", "EXCLUSIVE", "EXISTS", "EXPLAIN", "FAIL", "FOR", 
            "FOREIGN", "FROM", "FULL", "GLOB", "GROUP", "HAVING", "IF", "IGNORE", 
            "IMMEDIATE", "IN", "INDEX", "INDEXED", "INITIALLY", "INNER", "INSERT", 
            "INSTEAD", "INTERSECT", "INTO", "IS", "ISNULL", "JOIN", "KEY", "LEFT", 
            "LIKE", "LIMIT", "MATCH", "NATURAL", "NO", "NOT", "NOTNULL", "NULL", 
            "OF", "OFFSET", "ON", "OR", "ORDER", "OUTER", "PLAN", "PRAGMA", 
            "PRIMARY", "QUERY", "RAISE", "RECURSIVE", "REFERENCES", 
            "REINDEX", "RELEASE", "RENAME", "REPLACE", "RESTRICT", 
            "ROLLBACK", "ROW", "ROWS", "SAVEPOINT", "SELECT", "SET", 
            "TABLE", "TEMP", "TEMPORARY", "THEN", "TO", "TRANSACTION", "TRIGGER", 
            "UNION", "UNIQUE", "UPDATE", "USING", "VACUUM", "VALUES", "VIEW", 
            "VIRTUAL", "WHEN", "WHERE", "WITH", "WITHOUT", "FIRST_VALUE", "OVER", 
            "PARTITION", "RANGE", "PRECEDING", "UNBOUNDED", "CURRENT", "FOLLOWING", 
            "CUME_DIST", "DENSE_RANK", "LAG", "LAST_VALUE", "LEAD", "NTH_VALUE", 
            "NTILE", "PERCENT_RANK", "RANK", "ROW_NUMBER", "GENERATED", "ALWAYS", 
            "STORED", "TRUE", "FALSE", "WINDOW", "NULLS", "FIRST", "LAST", "FILTER", 
            "GROUPS", "EXCLUDE", "TIES", "OTHERS", "DO", "NOTHING"
        ]
        
        self.operators = [
            "=", "==", "<>", "!=", "<", "<=", ">", ">=", "+", "-", "*", "/", "%",
            "||", "&", "|", "<<", ">>", "AND", "OR", "NOT", "IS", "IS NOT", 
            "IN", "LIKE", "GLOB", "MATCH", "BETWEEN"
        ]
        
        self.join_types = [
            "JOIN", "INNER JOIN", "LEFT JOIN", "LEFT OUTER JOIN", "CROSS JOIN", "NATURAL JOIN",
            "NATURAL LEFT JOIN"
        ]
        
        self.aggregate_functions = [
            "AVG", "COUNT", "GROUP_CONCAT", "MAX", "MIN", "SUM", "TOTAL"
        ]
        
        self.scalar_functions = [
            "ABS", "COALESCE", "GLOB", "IFNULL", "INSTR", "HEX", "LENGTH",
            "LIKE", "LIKELIHOOD", "LIKELY", "LOAD_EXTENSION", "LOWER",
            "LTRIM", "MATCH", "NULLIF", "PRINTF", "QUOTE", "REPLACE", "ROUND", "RTRIM", "SOUNDEX",
            "SQLITE_SOURCE_ID", 
            "SUBSTR", "TRIM", "TYPEOF", "UNICODE", "UNLIKELY", "UPPER",
            "ZEROBLOB", "DATE", "TIME", "DATETIME", "JULIANDAY", "STRFTIME"
        ]
        
        self.window_functions = [
            "ROW_NUMBER", "RANK", "DENSE_RANK", "PERCENT_RANK", "CUME_DIST",
            "NTILE", "LAG", "LEAD", "FIRST_VALUE", "LAST_VALUE", "NTH_VALUE"
        ]
        
        self.data_types = [
            "INTEGER", "TEXT", "REAL", "NUMERIC"
        ]
        
        self.pragmas = [
            "auto_vacuum", "automatic_index", "busy_timeout", "cache_size", 
            "case_sensitive_like", "cell_size_check", "checkpoint_fullfsync", "count_changes",
            "defer_foreign_keys", "foreign_key_check", 
            "foreign_key_list", "foreign_keys", "freelist_count", "fullfsync", 
            "ignore_check_constraints", "incremental_vacuum", "integrity_check", 
            "journal_mode", "journal_size_limit", "locking_mode", 
            "mmap_size", "page_count", "page_size", "parser_trace", 
            "query_only", "quick_check", "read_uncommitted", "recursive_triggers", 
            "reverse_unordered_selects", "secure_delete", 
            "shrink_memory", "stats", "synchronous", "table_info", 
            "temp_store", "threads", "wal_autocheckpoint", "wal_checkpoint"
            # removed "max_page_count"
        ]

        self.function_requirements = {
            "LIKELIHOOD": {"args": 2, "special": likelihood_handler},
            "NULLIF": {"args": 2},
            "IFNULL": {"args": 2},
            "COALESCE": {"args": [1, 2, 3]},  # Accepts variable number of arguments
            "INSTR": {"args": 2},
            "SUBSTR": {"args": [2, 3]},  # 2 or 3 arguments
            "PRINTF": {"args": [1, 2, 3, 4]},  # Variable arguments
            "REPLACE": {"args": 3},
            "ROUND": {"args": [1, 2]},  # 1 or 2 arguments
            "TRIM": {"args": [1, 2, 3]},  # 1-3 arguments
            "LAG": {"args": [1, 2, 3]},
            "LEAD": {"args": [1, 2, 3]},
            "NTH_VALUE": {"args": 2},
            "NTILE": {"args": 1},
            "LOWER": {"args": 1},
            "UPPER": {"args": 1},
            "LENGTH": {"args": 1},
            "HEX": {"args": 1},
            "TYPEOF": {"args": 1},
            "ABS": {"args": 1},
            "UNICODE": {"args": 1},
            "RTRIM": {"args": [1, 2]},
            "LTRIM": {"args": [1, 2]}
        }

    def generate_literal_value(self):
        """Generate a random literal value according to SQLite grammar."""
        options = [
            lambda: str(random.randint(-1000000, 1000000)),  # NUMERIC_LITERAL
            lambda: f"'{random_string(random.randint(1, 20))}'",  # STRING_LITERAL
            lambda: f"x'{random_hex_string(random.randint(2, 8))}'",  # BLOB_LITERAL
            lambda: "NULL",  # NULL
            lambda: "TRUE",  # TRUE
            lambda: "FALSE",  # FALSE
        ]
        return random.choice(options)()
    
    def generate_expr(self, depth=0, tables_info=None, max_depth=3):
        """Generate a random SQLite expression following the formal grammar."""
        if depth >= max_depth:
            # At max depth, return a simple expression
            if tables_info and random.random() < 0.7:
                # Use a column reference
                table = random.choice(list(tables_info.keys()))
                if tables_info[table]["columns"]:
                    col = random.choice(tables_info[table]["columns"])
                    return f"{table}.{col}"
            
            # Or a literal value
            return self.generate_literal_value()
        
        options = []
        
        # Add literal values
        options.append(lambda: self.generate_literal_value())
        
        # Add column references if tables_info is provided
        if tables_info:
            options.append(lambda: self.generate_column_reference(tables_info))
        
        # Add unary operations
        options.append(lambda: f"{random.choice(['NOT', '+', '-', '~'])} {self.generate_expr(depth+1, tables_info, max_depth)}")
        
        # Add binary operations
        def binary_op():
            left = self.generate_expr(depth+1, tables_info, max_depth)
            right = self.generate_expr(depth+1, tables_info, max_depth)
            op = random.choice([
                '+', '-', '*', '/', '%', '||', '<<', '>>', '&', '|', 
                '<', '<=', '>', '>=', '=', '==', '!=', '<>', 
                'AND', 'OR', 'IS', 'IS NOT', 'LIKE', 'GLOB', 'MATCH'
            ])
            return f"({left} {op} {right})"
        
        options.append(binary_op)
        
        # Add function calls
        def function_call():
            func = random.choice(self.scalar_functions + self.aggregate_functions)
            
            # Special case for COUNT(*)
            if func == "COUNT" and random.random() < 0.5:
                return f"{func}(*)"
            
            # Handle functions with specific requirements
            if func in self.function_requirements:
                req = self.function_requirements[func]
                
                # Determine number of arguments
                if isinstance(req["args"], list):
                    # If args is a list, randomly select one of the allowed argument counts
                    num_args = random.choice(req["args"])
                else:
                    # If args is an integer, use that fixed number
                    num_args = req["args"]
                
                # Generate arguments
                args = []
                for _ in range(num_args):
                    args.append(self.generate_expr(depth+1, tables_info, max_depth))
                
                # Apply special handling if needed
                if "special" in req:
                    args = req["special"](args)
                
                args_str = ', '.join(args)
                return f"{func}({args_str})"
            else:
                # Default handling for other functions
                num_args = random.randint(1, 3)  # Most functions need at least 1 arg
                
                args = []
                for _ in range(num_args):
                    args.append(self.generate_expr(depth+1, tables_info, max_depth))
                
                args_str = ', '.join(args)
                return f"{func}({args_str})"
        
        options.append(function_call)
        
        # Add CASE expressions
        def case_expr():
            if random.random() < 0.5:
                # Simple CASE
                case_val = self.generate_expr(depth+1, tables_info, max_depth)
                result = f"CASE {case_val} "
                
                for _ in range(random.randint(1, 3)):
                    when_val = self.generate_expr(depth+1, tables_info, max_depth)
                    then_val = self.generate_expr(depth+1, tables_info, max_depth)
                    result += f"WHEN {when_val} THEN {then_val} "
                
                if random.random() < 0.7:
                    else_val = self.generate_expr(depth+1, tables_info, max_depth)
                    result += f"ELSE {else_val} "
                
                result += "END"
                return result
            else:
                # Searched CASE
                result = "CASE "
                
                for _ in range(random.randint(1, 3)):
                    when_condition = self.generate_expr(depth+1, tables_info, max_depth)
                    then_val = self.generate_expr(depth+1, tables_info, max_depth)
                    result += f"WHEN {when_condition} THEN {then_val} "
                
                if random.random() < 0.7:
                    else_val = self.generate_expr(depth+1, tables_info, max_depth)
                    result += f"ELSE {else_val} "
                
                result += "END"
                return result
        
        options.append(case_expr)
        
        # Add subquery expressions (e.g. IN, EXISTS)
        if depth < max_depth - 1 and tables_info:
            def subquery_expr():
                if random.random() < 0.5:
                    # IN subquery
                    col_ref = self.generate_column_reference(tables_info)
                    return f"{col_ref} IN (SELECT {self.generate_result_column(tables_info)} FROM {random.choice(list(tables_info.keys()))} LIMIT 5)"
                else:
                    # EXISTS subquery
                    return f"EXISTS (SELECT 1 FROM {random.choice(list(tables_info.keys()))} LIMIT 1)"
            
            options.append(subquery_expr)
        
        # Choose and return a random expression type
        expr_generator = random.choice(options)
        return expr_generator()
    
    def generate_column_reference(self, tables_info):
        """Generate a reference to a column in one of the available tables."""
        if not tables_info:
            return "1"  # Fallback if no tables available
            
        # Only choose tables that actually exist and have columns
        valid_tables = [table for table in tables_info.keys() 
                        if tables_info[table]["columns"]]
        
        if not valid_tables:
            return "1"  # Fallback if no tables have columns
        
        table = random.choice(valid_tables)
        col = random.choice(tables_info[table]["columns"])
        
        # Sometimes qualify with table name
        if random.random() < 0.5:
            return f"{table}.{col}"
        return col
    
    def generate_result_column(self, tables_info):
        """Generate a result column for SELECT statements."""
        if not tables_info:
            return "1"
            
        options = []
        
        # Simple column reference
        options.append(lambda: self.generate_column_reference(tables_info))
        
        # Star notation
        options.append(lambda: "*")
        
        # Table qualified star
        if random.random() < 0.3:
            options.append(lambda: f"{random.choice(list(tables_info.keys()))}.*")
        
        # Expression with optional alias
        def expr_with_alias():
            expr = self.generate_expr(0, tables_info, 2)
            
            if random.random() < 0.5:
                alias = f"alias_{random_string(3)}"
                return f"{expr} AS {alias}"
            return expr
            
        options.append(expr_with_alias)
        
        # Choose a random result column type
        result_col_generator = random.choice(options)
        return result_col_generator()
    
    def generate_subquery_select(self, tables_info):
        """Generate a subquery for use in SELECT."""
        # Pick a random table to base the subquery on
        table = random.choice(list(tables_info.keys()))
        
        # Pick a random column from the table for the subquery
        column = random.choice(tables_info[table]["columns"])
        
        # Randomly decide the type of subquery (aggregate)
        subquery_type = random.choice(["COUNT", "SUM", "AVG", "MAX", "MIN"])
        
        # Generate the subquery
        subquery = f"{subquery_type}({column}) FROM {table} WHERE {self.generate_expr(0, tables_info, 2)}"
        
        return subquery

    def generate_select_core(self, tables_info, include_order_by=True, include_limit=True):
        """Generate a SELECT core statement following the formal grammar."""
        if not tables_info:
            return "SELECT 1"
        
        # Generate the SELECT keyword with optional DISTINCT
        select_distinct = " DISTINCT" if random.random() < 0.2 else ""
        query = f"SELECT{select_distinct}"
        
        # Generate result columns (1-5)
        num_columns = random.randint(1, 5)
        result_columns = []
        
        for _ in range(num_columns):
            result_columns.append(self.generate_result_column(tables_info))
        
        query += f" {', '.join(result_columns)}"
        
        # Generate FROM clause with either a table list or a join
        if random.random() < 0.7:
            # Simple table list - only select from existing tables
            valid_tables = list(tables_info.keys())
            if not valid_tables:
                query += " FROM (SELECT 1)"
            else:
                num_tables = min(random.randint(1, 3), len(valid_tables))
                table_names = random.sample(valid_tables, num_tables)
                query += f" FROM {', '.join(table_names)}"
        else:
            # Join clause - ensure we have at least 2 tables before attempting joins
            valid_tables = list(tables_info.keys())
            if len(valid_tables) >= 2:
                tables = random.sample(valid_tables, 2)
                join_type = random.choice(self.join_types)
                
                query += f" FROM {tables[0]} {join_type} {tables[1]}"
                
                # Add join constraint with columns that exist in both tables
                if "NATURAL" not in join_type and join_type != "CROSS JOIN":
                    # ON condition
                    if random.random() < 0.7:
                        table1_col = None
                        table2_col = None
                        
                        if tables_info[tables[0]]["columns"]:
                            table1_col = random.choice(tables_info[tables[0]]["columns"])
                        
                        if tables_info[tables[1]]["columns"]:
                            table2_col = random.choice(tables_info[tables[1]]["columns"])
                        
                        if table1_col and table2_col:
                            query += f" ON {tables[0]}.{table1_col} = {tables[1]}.{table2_col}"
                        else:
                            query += " ON 1=1"
                    else:
                        # USING clause with columns that exist in both tables
                        common_cols = []
                        
                        if tables_info[tables[0]]["columns"] and tables_info[tables[1]]["columns"]:
                            for col in tables_info[tables[0]]["columns"]:
                                if col in tables_info[tables[1]]["columns"]:
                                    common_cols.append(col)
                        
                        if common_cols:
                            using_cols = random.sample(common_cols, min(2, len(common_cols)))
                            query += f" USING ({', '.join(using_cols)})"
                        else:
                            query += " ON 1=1"
            else:
                # Fallback to simple table selection if we don't have enough tables
                if valid_tables:
                    query += f" FROM {random.choice(valid_tables)}"
                else:
                    query += " FROM (SELECT 1)"
        
        # Generate WHERE clause
        if random.random() < 0.7:
            query += f" WHERE {self.generate_expr(0, tables_info, 2)}"
        
        # Generate GROUP BY clause
        if random.random() < 0.3:
            group_cols = []
            table = None
            
            if tables_info:
                table = random.choice(list(tables_info.keys()))
                
                if tables_info[table]["columns"]:
                    num_group_cols = min(random.randint(1, 3), len(tables_info[table]["columns"]))
                    group_cols = random.sample(tables_info[table]["columns"], num_group_cols)
            
            if group_cols:
                query += f" GROUP BY {', '.join(group_cols)}"
                
                # Generate HAVING clause
                if random.random() < 0.3:
                    query += f" HAVING {self.generate_expr(0, {table: tables_info[table]}, 2)}"
        
        # Generate ORDER BY clause only if include_order_by is True
        if include_order_by and random.random() < 0.6:
            order_cols = []
            
            if tables_info:
                table = random.choice(list(tables_info.keys()))
                
                if tables_info[table]["columns"]:
                    num_order_cols = min(random.randint(1, 2), len(tables_info[table]["columns"]))
                    order_cols = random.sample(tables_info[table]["columns"], num_order_cols)
            
            if order_cols:
                order_terms = []
                
                for col in order_cols:
                    direction = " ASC" if random.random() < 0.5 else " DESC"
                    order_terms.append(f"{col}{direction if random.random() < 0.5 else ''}")
                
                query += f" ORDER BY {', '.join(order_terms)}"
            else:
                query += " ORDER BY 1"  # Safe fallback
        
        # Generate LIMIT clause only if include_limit is True
        if include_limit and random.random() < 0.4:
            limit = random.randint(1, 100)
            query += f" LIMIT {limit}"
            
            # Generate optional OFFSET
            if random.random() < 0.3:
                offset = random.randint(0, 20)
                if random.random() < 0.5:
                    query += f" OFFSET {offset}"
                else:
                    query += f", {offset}"  # Alternative syntax
        
        return query
    
    def generate_select_stmt(self, tables_info):
        """Generate a complete SELECT statement."""
        # Add optional WITH clause TODO
        with_clause = ""
        if random.random() < 0 and tables_info:
            cte_name = f"cte_{random_string(3)}"
            table = random.choice(list(tables_info.keys()))
            with_clause = f"WITH {cte_name} AS (SELECT * FROM {table} LIMIT 10) "
        
        # Generate main SELECT without ORDER BY or LIMIT if we're going to use a compound
        will_use_compound = random.random() < 0.2 and tables_info
        
        # Generate first SELECT core - tell it not to include ORDER BY or LIMIT if we'll have a compound
        select_core = self.generate_select_core(
            tables_info, 
            include_order_by=not will_use_compound,
            include_limit=not will_use_compound
        )
        
        # Add compound operator
        compound = ""
        if will_use_compound:
            compound_op = random.choice(["UNION", "UNION ALL", "INTERSECT", "EXCEPT"])
            # Don't include ORDER BY or LIMIT in the second part of the compound either
            second_select = self.generate_select_core(
                tables_info, 
                include_order_by=False,
                include_limit=False
            )
            compound = f" {compound_op} {second_select}"
            
            # Add ORDER BY at the end of the entire statement if needed
            if random.random() < 0.6:
                order_cols = []
                if tables_info:
                    table = random.choice(list(tables_info.keys()))
                    if tables_info[table]["columns"]:
                        num_order_cols = min(random.randint(1, 2), len(tables_info[table]["columns"]))
                        order_cols = random.sample(tables_info[table]["columns"], num_order_cols)
                
                if order_cols:
                    order_terms = []
                    for col in order_cols:
                        direction = " ASC" if random.random() < 0.5 else " DESC"
                        order_terms.append(f"{col}{direction if random.random() < 0.5 else ''}")
                    compound += f" ORDER BY {', '.join(order_terms)}"
                else:
                    compound += " ORDER BY 1"  # Safe fallback
            
            # Add LIMIT at the end of the entire statement if needed
            if random.random() < 0.4:
                limit = random.randint(1, 100)
                compound += f" LIMIT {limit}"
                
                # Generate optional OFFSET
                if random.random() < 0.3:
                    offset = random.randint(0, 20)
                    if random.random() < 0.5:
                        compound += f" OFFSET {offset}"
                    else:
                        # Use alternative comma syntax
                        # Replace the existing LIMIT with LIMIT n, offset
                        compound = compound.replace(f" LIMIT {limit}", f" LIMIT {limit}, {offset}")
        
        return f"{with_clause}{select_core}{compound}"

    def generate_conflict_clause(self):

        if random.random() < 0.5:
            return ""
        else:
            query = "ON CONFLICT "
            choice = random.random()
            if choice < 0.2:
                query += "ROLLBACK "
            elif choice < 0.4:
                query += "ABORT "
            elif choice < 0.6:
                query += "FAIL "
            elif choice < 0.8:
                query += "IGNORE "
            else:
                query += "REPLACE "
            return query

    def generate_insert_stmt(self, table_name, column_names, column_types=None, column_constraints=None):
        """Generate an INSERT statement according to the formal grammar."""
        if not column_names:
            return f"-- Skipping INSERT for {table_name}: no columns"
        
        column_types = column_types or {}
        column_constraints = column_constraints or {}
        
        # Optional WITH clause
        with_clause = ""
        if random.random() < 0.1:
            cte_name = f"cte_{random_string(3)}"
            with_clause = f"WITH {cte_name} AS (SELECT 1) "
        
        # INSERT variants
        insert_variant = random.choice([
            "INSERT INTO",
            "INSERT OR REPLACE INTO",
            "INSERT OR ABORT INTO",
            "INSERT OR FAIL INTO",
            "INSERT OR IGNORE INTO",
            "REPLACE INTO"
        ])
        
        # Column list
        col_list = f"({', '.join(column_names)})"
        
        # Generate values
        if random.random() < 0.8:
            # Use VALUES clause
            num_rows = random.randint(1, 3)
            rows = []
            
            for i in range(num_rows):
                values = []
                for idx, col in enumerate(column_names):
                    col_type = column_types.get(col)
                    col_constraint = column_constraints.get(col)
                    values.append(random_value(is_not_null=col_constraint["is_not_null"], data_type=col_type, is_unique=col_constraint["is_unique"], min=col_constraint["min"], max=col_constraint["max"], unique_id=i*100+idx))
                rows.append(f"({', '.join(values)})")
            
            values_clause = f"VALUES {', '.join(rows)}"
            
            
            return f"{with_clause}{insert_variant} {table_name} {col_list} {values_clause}"
        else:
            # Use a SELECT statement instead of VALUES
            select_cols = []
            for col in column_names:
                col_type = column_types.get(col)
                col_constraint = column_constraints.get(col)
                select_cols.append(random_value(is_not_null=col_constraint["is_not_null"], data_type=col_type, is_unique=col_constraint["is_unique"], min=col_constraint["min"], max=col_constraint["max"]))
            select_clause = f"SELECT {', '.join(select_cols)}"
            
            return f"{with_clause}{insert_variant} {table_name} {col_list} {select_clause}"
    
    def generate_update_stmt(self, table_name, column_names, column_types=None):
        """Generate an UPDATE statement according to the formal grammar."""
        if not column_names:
            return f"-- Skipping UPDATE for {table_name}: no columns"
        
        # Check that columns actually exist
        valid_columns = column_names if column_names else []
        if not valid_columns:
            return f"-- Skipping UPDATE for {table_name}: no valid columns"
        
        column_types = column_types or {}
        
        # Optional WITH clause
        with_clause = ""
        if random.random() < 0.1:
            cte_name = f"cte_{random_string(3)}"
            with_clause = f"WITH {cte_name} AS (SELECT 1) "
        
        # UPDATE variants
        update_variant = random.choice([
            "UPDATE",
            "UPDATE OR REPLACE",
            "UPDATE OR ROLLBACK",
            "UPDATE OR ABORT",
            "UPDATE OR FAIL",
            "UPDATE OR IGNORE"
        ])
        
        # Generate SET clause
        num_cols = min(random.randint(1, 3), len(column_names))
        set_cols = random.sample(column_names, num_cols)
        
        set_exprs = []
        for col in set_cols:
            col_type = column_types.get(col)
            val = random_value(data_type=col_type)
            set_exprs.append(f"{col} = {val}")
        
        set_clause = f"SET {', '.join(set_exprs)}"
        
        # Generate WHERE clause
        where_clause = ""
        if random.random() < 0.8 and column_names:
            col = random.choice(column_names)
            col_type = column_types.get(col)
            
            op = random.choice(["=", ">", "<", ">=", "<=", "!=", "IS NULL", "IS NOT NULL"])
            
            if op in ("IS NULL", "IS NOT NULL"):
                where_clause = f" WHERE {col} {op}"
            else:
                val = random_value(data_type=col_type)
                where_clause = f" WHERE {col} {op} {val}"
        

        
        return f"{with_clause}{update_variant} {table_name} {set_clause}{where_clause}"
    
    def generate_delete_stmt(self, table_name, column_names, column_types=None):
        """Generate a DELETE statement according to the formal grammar."""
        # Optional WITH clause
        with_clause = ""
        if random.random() < 0.1:
            cte_name = f"cte_{random_string(3)}"
            with_clause = f"WITH {cte_name} AS (SELECT 1) "
        
        # Basic DELETE FROM clause
        delete_clause = f"DELETE FROM {table_name}"
        
        # Generate WHERE clause (almost always for safety)
        where_clause = ""
        if random.random() < 0.9 and column_names:
            col = random.choice(column_names)
            col_type = column_types.get(col) if column_types else None
            
            op = random.choice(["=", ">", "<", ">=", "<=", "!=", "IS NULL", "IS NOT NULL"])
            
            if op in ("IS NULL", "IS NOT NULL"):
                where_clause = f" WHERE {col} {op}"
            else:
                val = random_value(data_type=col_type)
                where_clause = f" WHERE {col} {op} {val}"
        
        
        return f"{with_clause}{delete_clause}{where_clause}"
    
    def generate_create_table_stmt(self, table_counter, table_name=None):
        """Generate a CREATE TABLE statement according to the formal grammar."""
        grammar = SQLiteGrammar()
        query = "CREATE "

        # if choice < 0.33:
        #     query += "TEMP "
        # elif choice > 0.66:
        #     query += "TEMPORARY "
        
        query += "TABLE "
        
        # EXISTS clause
        query += "IF NOT EXISTS " if random.random() < 0.7 else ""

        # TODO add possible: schema-name . 

        # table_name
        table_name = table_name if table_name else f"t_{table_counter}"
        query += table_name + " "
        column_names = []
        column_types = {}
        column_constraints = {}
        primary_key_already_set = False

        if random.random() < 1:
            query += "( "
            # add columns
            num_columns = random.randint(1, 10)
            for column in range(num_columns):
                if column > 0:
                    query += ", "
                col_name = f"c_{column}"
                column_names.append(col_name)
                
                # possible type
                # if random.random() < 0.99:
                # Generate data type (not same as docs type-name)
                data_type = random.choice(self.data_types)
                column_types[col_name] = data_type

                save_constraint = {
                        "is_pk": False,
                        "is_not_null": False,
                        "is_unique": False,
                        "min": None,
                        "max": None,
                    }

                query += f"{col_name} {data_type} "

                # column constraint
                n_col_constraints = random.randint(0, 3)
                
                column_constraint = ""

                auto_increment_set = False
                conflict_clause = ""

                # PRIMARY KEY
                if random.random() < 0.1:
                    if random.random() < 0.1 and not primary_key_already_set:
                        column_constraint += "PRIMARY KEY "
                        primary_key_already_set = True
                        save_constraint["is_pk"] = True
                        if random.random() < 0.33:
                            column_constraint += "ASC "
                        elif random.random() > 0.66:
                            column_constraint += "DESC "
                        # conflict clause
                        # column_constraint += grammar.generate_conflict_clause()
                        elif random.random() < 0.3 and data_type == "INTEGER":
                            column_constraint += ("AUTOINCREMENT ")
                            auto_increment_set = True
                # NOT NULL
                if random.random() < 0.1 and not auto_increment_set:
                    column_constraint += "NOT NULL "
                    save_constraint["is_not_null"] = True
                    #column_constraint += grammar.generate_conflict_clause()
                # UNIQUE
                if random.random() < 0.1 and not auto_increment_set:
                    column_constraint += "UNIQUE "
                    save_constraint["is_unique"]= True
                    #column_constraint += grammar.generate_conflict_clause()
                # CHECK
                if random.random() < 0.1 and not auto_increment_set and data_type in ["INTEGER", "REAL", "NUMERIC"] :
                    column_constraint += "CHECK ("
                    check_expr = f"{col_name} >= 0" if data_type in ["INTEGER", "REAL", "NUMERIC"] else "" #f"length({col_name}) > 0"    
                    save_constraint["min"]= 0                 
                    column_constraint += check_expr + ") "
                # DEFAULT
                if random.random() < 0.1 and not auto_increment_set:
                    default_val = random_value(data_type=data_type) #(expr) or literal or signed number
                    column_constraint += f"DEFAULT {default_val} "
                # COLLATE
                if random.random() < 0.1 and not auto_increment_set:
                    collation = random.choice(["BINARY", "NOCASE", "RTRIM"])
                    column_constraint += "COLLATE " + collation + " "
                    
                # foreign-key-clause 
                # GENERATED ALWAYS
                if column_constraint != "" and random.random() < 0.5:
                    query += "CONSTRAINT " + f"c_{random_string(random.randint(3, 10))} "
                query += column_constraint

                column_constraints[col_name] = save_constraint

            # add table constraints
            if random.random() < 0.5:
                query += ", "
                table_constraint = f"CONSTRAINT c_{random_string(random.randint(3, 10))} "
                query += table_constraint

            if random.random() < 0.25 and not primary_key_already_set:
                query += ", "
                query += "PRIMARY KEY ( "
                n_cols = random.randint(1, min(2, len(column_names)))  # pick 1 or 2 columns
                chosen_cols = random.sample(column_names, n_cols)
                query += ", ".join(chosen_cols) + ") "
                conflict_clause = grammar.generate_conflict_clause()
                query += conflict_clause
                for col in chosen_cols:
                    column_constraints[col]["is_pk"] = True
            
            if random.random() < 0.25:
                query += ", "
                query += "UNIQUE ( "
                n_cols = random.randint(1, min(2, len(column_names)))  # pick 1 or 2 columns
                chosen_cols = random.sample(column_names, n_cols)
                query += ", ".join(chosen_cols) + ") "
                if conflict_clause == "":
                    query += grammar.generate_conflict_clause()
                for col in chosen_cols:
                    column_constraints[col]["is_unique"] = True

            if random.random() < 0.25:
                query += ", "
                query += "CHECK ("
                chosen_cols = random.choice(column_names)
                query += f"{chosen_cols} IS NOT NULL"  # simple check expression => expr
                query += ") "
                column_constraints[chosen_cols]["is_not_null"] = True
            
            # TODO FOREIGN KEY

            query += ") "
            # TODO add table-options
        else:
            # TODO AS select-stmt
            query += ""

        return table_name, column_names, column_types, column_constraints, query
    
    def generate_create_index_stmt(self, table_name, column_names):
        """Generate a CREATE INDEX statement according to the formal grammar."""
        if not column_names:
            return f"-- Skipping INDEX for {table_name}: no columns"
        
        # UNIQUE index?
        unique = "UNIQUE " if random.random() < 0.2 else ""
        
        # EXISTS clause
        if_not_exists = "IF NOT EXISTS " if random.random() < 0.7 else ""
        
        # Index name
        index_name = f"idx_{random_string(5)}"
        
        # Indexed columns
        num_cols = min(random.randint(1, 3), len(column_names))
        chosen_cols = random.sample(column_names, num_cols)
        
        # Column definitions with potential collations/order
        indexed_columns = []
        for col in chosen_cols:
            col_def = col
            
            # Add COLLATE
            if random.random() < 0.2:
                collation = random.choice(["BINARY", "NOCASE", "RTRIM"])
                col_def += f" COLLATE {collation}"
            
            # Add sort order
            if random.random() < 0.3:
                direction = random.choice(["ASC", "DESC"])
                col_def += f" {direction}"
            
            indexed_columns.append(col_def)
        
        # WHERE clause
        where_clause = ""
        if random.random() < 0.3 and column_names:
            col = random.choice(column_names)
            op = random.choice(["=", ">", "<", ">=", "<=", "!=", "IS NULL", "IS NOT NULL"])
            
            if op in ("IS NULL", "IS NOT NULL"):
                where_clause = f" WHERE {col} {op}"
            else:
                val = random_value()
                where_clause = f" WHERE {col} {op} {val}"
        
        return f"CREATE {unique}INDEX {if_not_exists}{index_name} ON {table_name}({', '.join(indexed_columns)}){where_clause}"
    
    def generate_pragma_stmt(self):
        """Generate a PRAGMA statement according to the formal grammar."""
        pragma_name = random.choice(self.pragmas)
        
        # Just query the pragma value
        if random.random() < 0.7:
            return f"PRAGMA {pragma_name};"
        
        # Set the pragma value
        pragma_value = None
        
        if pragma_name in ["journal_mode"]:
            pragma_value = random.choice(["DELETE", "TRUNCATE", "PERSIST", "MEMORY", "WAL", "OFF"])
        elif pragma_name in ["synchronous"]:
            pragma_value = random.choice(["0", "1", "2", "OFF", "NORMAL", "FULL"])
        elif pragma_name in ["temp_store"]:
            pragma_value = random.choice(["0", "1", "2", "DEFAULT", "FILE", "MEMORY"])
        elif pragma_name in ["locking_mode"]:
            pragma_value = random.choice(["NORMAL", "EXCLUSIVE"])
        elif pragma_name in ["auto_vacuum"]:
            pragma_value = random.choice(["0", "1", "2", "NONE", "FULL", "INCREMENTAL"])
        elif pragma_name in ["foreign_keys", "recursive_triggers", "secure_delete"]:
            pragma_value = random.choice(["0", "1", "true", "false", "on", "off"])
        elif pragma_name in ["cache_size", "page_size", "mmap_size"]:
            multiplier = 1024 if random.random() < 0.5 else 1
            pragma_value = str(random.randint(1, 100) * multiplier)
        else:
            pragma_value = random.choice(["0", "1"])
        
        # Random assignment syntax
        if random.random() < 0.5:
            return f"PRAGMA {pragma_name} = {pragma_value};"
        else:
            return f"PRAGMA {pragma_name}({pragma_value});"


# Function to generate a simple SQL SELECT query
def generate_query(tables_info):
    """Generate a complete test case using the formal grammar."""

    grammar = SQLiteGrammar()
    statements = []
    # First create tables
    if tables_info == {}:
        for i in range(5):
            table_name, column_names, column_types, column_constraints, query = grammar.generate_create_table_stmt(i)
            statements.append(query + ";")
            tables_info[table_name] = {"columns": column_names, "types": column_types, "constraints": column_constraints}
        # Insert data
        for table_name, table_data in tables_info.items():
            column_names = table_data["columns"]
            column_types = table_data["types"]
            column_constraints = table_data["constraints"]
            num_rows = random.randint(1, 5)
            for _ in range(num_rows):
                insert_stmt = grammar.generate_insert_stmt(table_name, column_names, column_types, column_constraints)
                statements.append(insert_stmt + ";")

    
    # Sometimes add initial PRAGMA statements
    if random.random() < 0.3:
        statements.append(grammar.generate_pragma_stmt())
    
    # Generate various statement types
    num_queries = random.randint(2, 5) 
    
    for _ in range(num_queries):
        stmt_type = random.choice([
            "SELECT", # "UPDATE", "DELETE", "CREATE INDEX", "PRAGMA", 
            # "ALTER", "WITH", "TRANSACTION"
        ])
        
        if stmt_type == "SELECT":
            statements.append(grammar.generate_select_stmt(tables_info) + ";")

        elif stmt_type == "UPDATE" and tables_info:
            table_name = random.choice(list(tables_info.keys()))
            column_names = tables_info[table_name]["columns"]
            column_types = tables_info[table_name]["types"]
            statements.append(grammar.generate_update_stmt(table_name, column_names, column_types) + ";")
        elif stmt_type == "DELETE" and tables_info:
            table_name = random.choice(list(tables_info.keys()))
            column_names = tables_info[table_name]["columns"]
            column_types = tables_info[table_name]["types"]
            statements.append(grammar.generate_delete_stmt(table_name, column_names, column_types) + ";")
        elif stmt_type == "CREATE INDEX" and tables_info:
            table_name = random.choice(list(tables_info.keys()))
            column_names = tables_info[table_name]["columns"]
            statements.append(grammar.generate_create_index_stmt(table_name, column_names) + ";")
        elif stmt_type == "PRAGMA":
            statements.append(grammar.generate_pragma_stmt() + ";")
        elif stmt_type == "ALTER" and tables_info:
            table_name = random.choice(list(tables_info.keys()))
            # Simple ALTER TABLE ADD COLUMN
            data_type = random.choice(grammar.data_types)
            col_name = random_column_name()
            statements.append(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {data_type};")
        elif stmt_type == "WITH" and tables_info:
            # WITH clause followed by a query
            cte_name = f"cte_{random_string(3)}"
            table_name = random.choice(list(tables_info.keys()))
            cte_stmt = f"WITH {cte_name} AS (SELECT * FROM {table_name} LIMIT 10) SELECT * FROM {cte_name};"
            statements.append(cte_stmt)
        elif stmt_type == "TRANSACTION":
            # Transaction with multiple statements
            transaction = ["BEGIN TRANSACTION;"]
            
            for _ in range(random.randint(1, 3)):
                if tables_info:
                    table_name = random.choice(list(tables_info.keys()))
                    column_names = tables_info[table_name]["columns"]
                    column_types = tables_info[table_name]["types"]
                    
                    if random.random() < 0.5:
                        transaction.append(grammar.generate_insert_stmt(table_name, column_names, column_types) + ";")
                    else:
                        transaction.append(grammar.generate_update_stmt(table_name, column_names, column_types) + ";")
                else:
                    transaction.append("SELECT 1;")
            
            transaction.append("COMMIT;")
            statements.extend(transaction)
    
    # End with a simple query that will definitely produce output
    if tables_info:
        table_name = random.choice(list(tables_info.keys()))
        statements.append(f"SELECT COUNT(*) FROM {table_name};")
    else:
        statements.append("SELECT 1;")
    
    return "\n".join(statements), tables_info
