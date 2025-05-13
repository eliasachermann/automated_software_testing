import random
import string
import re
import time


def likelihood_handler(args):
    return [args[0], str(random.uniform(0.0, 1.0))]


class SQLiteGrammar:
    def __init__(self):
        self.keywords = [
            "ABORT",
            "ACTION",
            "ADD",
            "AFTER",
            "ALL",
            "ALTER",
            "ANALYZE",
            "AND",
            "AS",
            "ASC",
            "ATTACH",
            "AUTOINCREMENT",
            "BEFORE",
            "BEGIN",
            "BETWEEN",
            "BY",
            "CASCADE",
            "CASE",
            "CAST",
            "CHECK",
            "COLLATE",
            "COLUMN",
            "COMMIT",
            "CONFLICT",
            "CONSTRAINT",
            "CREATE",
            "CROSS",
            "DATABASE",
            "DEFAULT",
            "DEFERRABLE",
            "DEFERRED",
            "DELETE",
            "DESC",
            "DETACH",
            "DISTINCT",
            "DROP",
            "EACH",
            "ELSE",
            "END",
            "ESCAPE",
            "EXCEPT",
            "EXCLUSIVE",
            "EXISTS",
            "EXPLAIN",
            "FAIL",
            "FOR",
            "FOREIGN",
            "FROM",
            "FULL",
            "GROUP",
            "HAVING",
            "IF",
            "IGNORE",
            "IMMEDIATE",
            "IN",
            "INDEX",
            "INDEXED",
            "INITIALLY",
            "INNER",
            "INSERT",
            "INSTEAD",
            "INTERSECT",
            "INTO",
            "IS",
            "ISNULL",
            "JOIN",
            "KEY",
            "LEFT",
            "LIKE",
            "LIMIT",
            "NATURAL",
            "NO",
            "NOT",
            "NOTNULL",
            "NULL",
            "OF",
            "OFFSET",
            "ON",
            "OR",
            "ORDER",
            "OUTER",
            "PLAN",
            "PRAGMA",
            "PRIMARY",
            "QUERY",
            "RAISE",
            "RECURSIVE",
            "REFERENCES",
            "REINDEX",
            "RELEASE",
            "RENAME",
            "REPLACE",
            "RESTRICT",
            "ROLLBACK",
            "ROW",
            "ROWS",
            "SAVEPOINT",
            "SELECT",
            "SET",
            "TABLE",
            "TEMP",
            "TEMPORARY",
            "THEN",
            "TO",
            "TRANSACTION",
            "TRIGGER",
            "UNION",
            "UNIQUE",
            "UPDATE",
            "USING",
            "VACUUM",
            "VALUES",
            "VIEW",
            "VIRTUAL",
            "WHEN",
            "WHERE",
            "WITH",
            "WITHOUT",
            "FIRST_VALUE",
            "OVER",
            "PARTITION",
            "RANGE",
            "PRECEDING",
            "UNBOUNDED",
            "CURRENT",
            "FOLLOWING",
            "CUME_DIST",
            "DENSE_RANK",
            "LAG",
            "LAST_VALUE",
            "LEAD",
            "NTH_VALUE",
            "NTILE",
            "PERCENT_RANK",
            "RANK",
            "ROW_NUMBER",
            "GENERATED",
            "ALWAYS",
            "STORED",
            "TRUE",
            "FALSE",
            "WINDOW",
            "NULLS",
            "FIRST",
            "LAST",
            "FILTER",
            "GROUPS",
            "EXCLUDE",
            "TIES",
            "OTHERS",
            "DO",
            "NOTHING",
        ]

        self.operators = [
            "=",
            "==",
            "<>",
            "!=",
            "<",
            "<=",
            ">",
            ">=",
            "+",
            "-",
            "*",
            "/",
            "%",
            "||",
            "&",
            "|",
            "<<",
            ">>",
            "AND",
            "OR",
            "NOT",
            "IS",
            "IS NOT",
            "IN",
            "LIKE",
            "GLOB",
            "BETWEEN",
        ]

        self.join_types = [
            "JOIN",
            "INNER JOIN",
            "LEFT JOIN",
            "LEFT OUTER JOIN",
            "CROSS JOIN",
            "NATURAL JOIN",
            "NATURAL LEFT JOIN",
        ]

        self.aggregate_functions = [
            "AVG",
            "COUNT",
            "GROUP_CONCAT",
            "MAX",
            "MIN",
            "SUM",
            "TOTAL",
        ]

        self.scalar_functions = [
            "ABS",
            "COALESCE",
            "IFNULL",
            "INSTR",
            "HEX",
            "LENGTH",
            "LIKE",
            "LIKELIHOOD",
            "LIKELY",
            "LOWER",
            "LTRIM",
            "NULLIF",
            "PRINTF",
            "QUOTE",
            "REPLACE",
            "ROUND",
            "RTRIM",
            "SUBSTR",
            "TRIM",
            "TYPEOF",
            "UNICODE",
            "UPPER",
            "ZEROBLOB",
            "DATE",
            "TIME",
            "DATETIME",
            "JULIANDAY",
            "STRFTIME",
        ]

        self.window_functions = [
            "ROW_NUMBER",
            "RANK",
            "DENSE_RANK",
            "PERCENT_RANK",
            "CUME_DIST",
            "NTILE",
            "LAG",
            "LEAD",
            "FIRST_VALUE",
            "LAST_VALUE",
            "NTH_VALUE",
        ]

        self.data_types = ["INTEGER", "TEXT", "REAL", "NUMERIC"]

        self.pragmas = [
            "auto_vacuum",
            "automatic_index",
            "busy_timeout",
            "cache_size",
            "case_sensitive_like",
            "cell_size_check",
            "checkpoint_fullfsync",
            "count_changes",
            "defer_foreign_keys",
            "foreign_key_check",
            "foreign_key_list",
            "freelist_count",
            "fullfsync",
            "ignore_check_constraints",
            "incremental_vacuum",
            "integrity_check",
            "journal_size_limit",
            "locking_mode",
            "mmap_size",
            "page_count",
            "page_size",
            "parser_trace",
            "quick_check",
            "read_uncommitted",
            "recursive_triggers",
            "reverse_unordered_selects",
            "secure_delete",
            "shrink_memory",
            "stats",
            "synchronous",
            "table_info",
            "temp_store",
            "threads",
            "wal_autocheckpoint",
            "wal_checkpoint",
        ]

        self.function_requirements = {
            "LIKELIHOOD": {"args": 2, "special": likelihood_handler},
            "NULLIF": {"args": 2},
            "IFNULL": {"args": 2},
            "COALESCE": {"args": [2, 3, 4, 5, 6]},
            "INSTR": {"args": 2},
            "SUBSTR": {"args": [2, 3]},
            "PRINTF": {"args": [1, 2, 3, 4]},
            "REPLACE": {"args": 3},
            "ROUND": {"args": [1, 2]},
            "TRIM": {"args": [1, 2]},
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
            "LTRIM": {"args": [1, 2]},
            "AVG": {"args": 1},
            "TOTAL": {"args": 1},
            "COUNT": {"args": 1},
            "GROUP_CONCAT": {"args": [1, 2]},
            "MAX": {"args": 1},
            "MIN": {"args": 1},
            "SUM": {"args": 1},
            "ROW_NUMBER": {"args": 0},
            "RANK": {"args": 0},
            "DENSE_RANK": {"args": 0},
            "PERCENT_RANK": {"args": 0},
            "CUME_DIST": {"args": 0},
            "FIRST_VALUE": {"args": 1},
            "LAST_VALUE": {"args": 1},
            "LIKELY": {"args": 1},
            "QUOTE": {"args": 1},
            "LIKE": {"args": 2},
            "ZEROBLOB": {"args": 1},
        }

    def generate_default_values_stmt(self, table_name, tables_info=None):
        if not tables_info or table_name not in tables_info:
            return ""

        table_info = tables_info[table_name]
        is_without_rowid = table_info.get("without_rowid", False)

        if is_without_rowid:
            return ""

        table_info = tables_info[table_name]
        column_types = table_info.get("types", {})
        is_without_rowid = table_info.get("without_rowid", False)

        pk_columns = []

        for col, type_def in column_types.items():
            if isinstance(type_def, str) and "PRIMARY KEY" in type_def.upper():
                pk_columns.append(col)

        for constraint in table_info.get("constraints", []):
            if isinstance(constraint, str) and "PRIMARY KEY" in constraint.upper():
                match = re.search(r"PRIMARY\s+KEY\s*\(([^)]+)\)", constraint)
                if match:
                    pks = [col.strip() for col in match.group(1).split(",")]
                    pk_columns.extend(pks)

        if is_without_rowid and pk_columns:
            return ""

        for pk_col in pk_columns:
            col_def = column_types.get(pk_col, "")
            if not isinstance(col_def, str) or "DEFAULT" not in col_def.upper():
                if not (
                    isinstance(col_def, str)
                    and "INTEGER PRIMARY KEY" in col_def.upper()
                    and not is_without_rowid
                ):
                    return ""

        insert_variant = random.choice(
            [
                "INSERT INTO",
                "INSERT OR REPLACE INTO",
                "REPLACE INTO",
                "INSERT OR ABORT INTO",
                "INSERT OR FAIL INTO",
            ]
        )

        return f"{insert_variant} {table_name} DEFAULT VALUES;"

    def get_tie_breaker(self, table_name, tables_info=None):
        """Return appropriate tie-breaking column reference for a table"""
        if not tables_info or table_name not in tables_info:
            return "rowid"
            
        is_without_rowid = tables_info[table_name].get("without_rowid", False)
        
        if is_without_rowid:
            # For WITHOUT ROWID tables, use the first column as tie-breaker
            if tables_info[table_name]["columns"]:
                return f"{table_name}.{tables_info[table_name]['columns'][0]}"
            return "1"  # Fallback if no columns
        else:
            return f"{table_name}.rowid"  # Regular tables use rowid

    def generate_create_table_stmt(self, table_name=None):
        table = (
            table_name if table_name else f"t_{random_string(random.randint(3, 10))}"
        )

        temp = "TEMP " if random.random() < 0.1 else ""

        if_not_exists = "IF NOT EXISTS " if random.random() < 0.7 else ""

        will_be_without_rowid = random.random() < 0.1

        num_columns = random.randint(1, 10)
        columns = []
        column_names = []
        column_types = {}

        has_primary_key = False

        for _ in range(num_columns):
            col_name = f"c_{random_string(random.randint(3, 10))}"
            column_names.append(col_name)

            data_type = random.choice(self.data_types)
            column_types[col_name] = data_type

            constraints = []

            if random.random() < 0.1 and not has_primary_key:
                has_primary_key = True
                constraints.append("PRIMARY KEY")

                if data_type == "REAL":
                    data_type = "INTEGER"
                    column_types[col_name] = data_type

                if (
                    not will_be_without_rowid
                    and random.random() < 0.3
                    and data_type == "INTEGER"
                ):
                    constraints.append("AUTOINCREMENT")

            if random.random() < 0.2:
                default_val = random_value(data_type=data_type)
                constraints.append(f"DEFAULT {default_val}")

            if random.random() < 0.1 and data_type == "TEXT":
                collation = random.choice(["BINARY", "NOCASE", "RTRIM"])
                constraints.append(f"COLLATE {collation}")

            column_def = f"{col_name} {data_type}" + (
                "" if not constraints else f" {' '.join(constraints)}"
            )
            columns.append(column_def)

        table_constraints = []

        if random.random() < 0.2 and not any("PRIMARY KEY" in col for col in columns):
            has_primary_key = True
            chosen_cols = random.sample(
                column_names, min(random.randint(1, 3), len(column_names))
            )
            table_constraints.append(f"PRIMARY KEY ({', '.join(chosen_cols)})")

        if random.random() < 0.2:
            chosen_cols = random.sample(
                column_names, min(random.randint(1, 3), len(column_names))
            )
            table_constraints.append(f"UNIQUE ({', '.join(chosen_cols)})")

        if random.random() < 0.1 and column_names:
            col = random.choice(column_names)
            ref_table = f"t_{random_string(5)}"
            ref_col = f"c_{random_string(5)}"
            table_constraints.append(
                f"FOREIGN KEY ({col}) REFERENCES {ref_table}({ref_col})"
            )

        all_defs = columns + table_constraints
        create_table = (
            f"CREATE {temp}TABLE {if_not_exists}{table} ({', '.join(all_defs)})"
        )

        has_without_rowid = False
        if will_be_without_rowid and has_primary_key:
            create_table += " WITHOUT ROWID"
            has_without_rowid = True

        return table, column_names, column_types, create_table, has_without_rowid

    def generate_recursive_cte(self, tables_info):
        if not tables_info:
            return "WITH RECURSIVE nums(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM nums WHERE x<10) SELECT * FROM nums;"

        table_name = random.choice(list(tables_info.keys()))
        columns = tables_info[table_name]["columns"]

        if not columns:
            return "WITH RECURSIVE nums(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM nums WHERE x<10) SELECT * FROM nums;"

        col = random.choice(columns)
        return f"""
                WITH RECURSIVE counter(n) AS (
                    SELECT MIN(CASE WHEN typeof({col}) IN ('integer','real') THEN {col} ELSE 0 END) FROM {table_name}
                    UNION ALL
                    SELECT n+1 FROM counter 
                    WHERE n < (SELECT MIN(100,MAX(CASE WHEN typeof({col}) IN ('integer','real') THEN {col} ELSE 10 END)) FROM {table_name})
                    AND n < 100
                ) 
                SELECT n, COUNT(*) AS count_matches 
                FROM counter 
                LEFT JOIN {table_name} ON counter.n = CASE WHEN typeof({col}) IN ('integer','real') THEN {col} ELSE NULL END
                GROUP BY n
                ORDER BY n
                LIMIT 20;"""

    def generate_complex_window_query(self, tables_info):
        if not tables_info:
            return "SELECT 1;"

        table_name = random.choice(list(tables_info.keys()))
        columns = tables_info[table_name]["columns"]

        if len(columns) < 2:
            return f"SELECT * FROM {table_name};"

        col1, col2 = random.sample(columns, 2)

        return f"""
                SELECT {col1}, {col2},
                    ROW_NUMBER() OVER (PARTITION BY {col2}) as row_num,
                    RANK() OVER (PARTITION BY {col2} ORDER BY {col1}) as rank_val,
                    DENSE_RANK() OVER (PARTITION BY {col2} ORDER BY {col1}) as dense_rank_val,
                    SUM(CASE WHEN typeof({col1}) IN ('integer','real') THEN {col1} ELSE 0 END) 
                        OVER (PARTITION BY {col2} ORDER BY {col1} 
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total,
                    LAG(CASE WHEN typeof({col1}) IN ('integer','real') THEN {col1} ELSE 0 END, 1, 0) 
                        OVER (PARTITION BY {col2} ORDER BY {col1}) as prev_value,
                    LEAD(CASE WHEN typeof({col1}) IN ('integer','real') THEN {col1} ELSE 0 END, 1, 0) 
                        OVER (PARTITION BY {col2} ORDER BY {col1}) as next_value
                FROM {table_name}
                ORDER BY {col2}, {col1}
                LIMIT 20;
                """

    def generate_json_query(self, tables_info):
        if not tables_info:
            return "SELECT json_extract('{\"a\":1, \"b\":2}', '$.a') as val ORDER BY 1;"

        table_name = random.choice(list(tables_info.keys()))
        columns = tables_info[table_name].get("columns", [])
        is_without_rowid = tables_info[table_name].get("without_rowid", False)

        complex_json = '{"a":1, "b":"text", "c":[3,4,5], "d":{"e":6, "f":null}, "g":true, "h":false, "i":[{"j":10},{"j":20}]}'

        query_style = random.randint(0, 3)

        if query_style == 0:
            return f"""
            SELECT json_extract('{complex_json}', '$.a') as simple_extract,
                json_extract('{complex_json}', '$.c[1]') as array_extract,
                json_extract('{complex_json}', '$.d.e') as nested_extract,
                json_extract('{complex_json}', '$.i[0].j') as nested_array_extract,
                json_type('{complex_json}', '$.a') as type_number,
                json_type('{complex_json}', '$.b') as type_text,
                json_type('{complex_json}', '$.c') as type_array,
                json_type('{complex_json}', '$.d') as type_object,
                json_type('{complex_json}', '$.d.f') as type_null,
                json_array(1, 'text', NULL, 3.14, json_object('key', 'value')) as created_array,
                json_object('a', 1, 'b', 'text', 'c', NULL, 'd', json_array(1,2,3)) as created_object,
                json_valid('{complex_json}') as is_valid_json,
                json_valid('{{invalid json}}') as is_invalid_json
            FROM {table_name}
            LIMIT 1;
            """
        elif query_style == 1:
            if query_style == 1:
                if columns and len(columns) > 0:
                    # Handle WITHOUT ROWID tables by using their first column instead of ROWID
                    id_column = "ROWID"
                    if is_without_rowid:
                        # Use the first column as identifier for WITHOUT ROWID tables
                        id_column = columns[0]

                    return f"""
                    WITH json_data(id, data) AS (
                        SELECT {id_column}, '{complex_json}'
                        FROM {table_name}
                        LIMIT 10
                    )
                    SELECT id,
                        json_extract(data, '$.a') as a_value,
                        json_extract(data, '$.b') as b_value,
                        json_extract(data, '$.c') as c_array,
                        SUM(json_extract(data, '$.a')) OVER () as sum_a,
                        AVG(json_extract(data, '$.a')) OVER () as avg_a,
                        json_group_array(json_extract(data, '$.a')) OVER () as all_a_values,
                        json_group_object(id, json_extract(data, '$.b')) OVER () as id_to_b_map
                    FROM json_data
                    ORDER BY id;
                    """
            else:
                return f"""
                WITH json_data(id, data) AS (
                    SELECT 1, '{complex_json}' UNION ALL
                    SELECT 2, '{{"a":2, "b":"value2", "c":[6,7,8]}}' UNION ALL
                    SELECT 3, '{{"a":3, "b":"value3", "c":[9,10,11]}}'
                )
                SELECT id,
                    json_extract(data, '$.a') as a_value,
                    json_extract(data, '$.b') as b_value,
                    json_extract(data, '$.c') as c_array,
                    SUM(json_extract(data, '$.a')) OVER () as sum_a,
                    AVG(json_extract(data, '$.a')) OVER () as avg_a,
                    json_group_array(json_extract(data, '$.a')) OVER () as all_a_values,
                    json_group_object(id, json_extract(data, '$.b')) OVER () as id_to_b_map
                FROM json_data
                ORDER BY id;
                """
        elif query_style == 2:
            return f"""
            SELECT json_set('{complex_json}', '$.a', 100) as modified_a,
                json_set('{complex_json}', '$.d.e', 200) as modified_nested,
                json_set('{complex_json}', '$.d.new', 'new value') as added_property,
                json_set('{complex_json}', '$.c[1]', 99) as modified_array,
                json_insert('{complex_json}', '$.j', 'inserted') as inserted_j,
                json_insert('{complex_json}', '$.a', 'ignored') as insert_existing,
                json_replace('{complex_json}', '$.a', 999) as replaced_a,
                json_replace('{complex_json}', '$.nonexistent', 'ignored') as replace_nonexistent,
                json_remove('{complex_json}', '$.d') as removed_d,
                json_remove('{complex_json}', '$.c[0]') as removed_array_element,
                json_patch('{complex_json}', '{{"a":null, "z":100}}') as patched
            FROM {table_name}
            LIMIT 1;
            """
        else:
            if columns and len(columns) > 0:
                col1 = random.choice(columns)
                col2 = random.choice(columns) if len(columns) > 1 else col1

                # Handle WITHOUT ROWID tables
                id_column = "ROWID"
                if is_without_rowid:
                    id_column = columns[
                        0
                    ]  # Use the first column for WITHOUT ROWID tables

                return f"""
                WITH row_json AS (
                    SELECT {id_column}, json_object(
                        'id', {id_column},
                        'col1', {col1},
                        'col2', {col2}
                    ) as row_data
                    FROM {table_name}
                    LIMIT 5
                )
                SELECT {id_column},
                    row_data,
                    json_extract(row_data, '$.col1') as extracted_col1,
                    json_extract(row_data, '$.col2') as extracted_col2,
                    json_array(row_data) as array_of_rows,
                    json_type(row_data) as json_type,
                    json_each.key, 
                    json_each.value,
                    json_each.type
                FROM row_json, json_each(row_data)
                ORDER BY {id_column}, json_each.key
                LIMIT 20;
                """
            else:
                return f"""
                WITH json_demo AS (
                    SELECT '{complex_json}' as json_data
                ),
                json_expanded AS (
                    SELECT json_each.key as key, 
                           json_each.value as value, 
                           json_each.type as type,
                           json_each.path as path
                    FROM json_demo, json_each(json_data)
                )
                SELECT key, value, type, path,
                       IIF(type = 'object' OR type = 'array',
                           (SELECT json_group_array(child_key || ': ' || child_type)
                            FROM (SELECT json_tree.key as child_key, json_tree.type as child_type
                                  FROM json_demo, json_tree(json_data, path)
                                  WHERE json_tree.parent = path)),
                           NULL) as children
                FROM json_expanded
                ORDER BY path;
                """

    def generate_subquery_madness(self, tables_info):
        if random.random() < 0.99:
            # Existing code for regular subquery madness
            if not tables_info or len(tables_info) < 1:
                return "SELECT 1;"

            tables = list(tables_info.keys())
            table1 = random.choice(tables)

            if not tables_info[table1]["columns"]:
                return f"SELECT COUNT(*) FROM {table1};"

            col1 = random.choice(tables_info[table1]["columns"])

            return f"""
                    SELECT 
                        t1.{col1},
                        (SELECT COUNT(*) FROM {table1} t2 WHERE t2.{col1} = t1.{col1}) as same_value_count,
                        CASE WHEN EXISTS(SELECT 1 FROM {table1} t3 WHERE t3.{col1} > t1.{col1} LIMIT 1) 
                            THEN 'Not Max' ELSE 'Max' END as is_max_value,
                        (SELECT COUNT(*) FROM (
                            SELECT DISTINCT {col1} FROM {table1}
                        )) as distinct_values_count
                    FROM {table1} t1
                    WHERE t1.{col1} IN (
                        SELECT {col1} 
                        FROM {table1} 
                        WHERE typeof({col1}) NOT IN ('null')
                        GROUP BY {col1}
                        HAVING COUNT(*) > 0
                    )
                    ORDER BY (SELECT COUNT(*) FROM {table1} t4 WHERE t4.{col1} = t1.{col1}) DESC
                    LIMIT 10;
                    """
        else:
            tables = list(tables_info.keys())
            table1 = random.choice(tables)
            alias = f"col_{random_string(1)}"

            inner_query = f"SELECT 1 AS {alias}"
            window_func = random.choice(self.window_functions)

            if window_func in self.function_requirements:
                req = self.function_requirements[window_func]

                if isinstance(req["args"], list):
                    num_args = max(req["args"])
                else:
                    num_args = req["args"]

                args_list = []
                for i in range(num_args):
                    args_list.append("1")

                func_args = ", ".join(args_list)
            else:
                func_args = "1"

            values_expr = self.generate_values_expr(rows=1, cols=1)

            # Generate window clause using positional references (1) instead of column names
            window_clause_type = random.randint(0, 5)

            if window_clause_type == 0:
                # Empty OVER() clause
                window_clause = "OVER()"
            elif window_clause_type == 1:
                # PARTITION BY clause using position
                window_clause = "OVER(PARTITION BY 1)"
            elif window_clause_type == 2:
                # ORDER BY clause with stable ordering using position
                direction = "ASC" if random.random() < 0.5 else "DESC"
                window_clause = f"OVER(ORDER BY 1 {direction})"
            elif window_clause_type == 3:
                # Combined PARTITION BY and ORDER BY with position
                direction = "ASC" if random.random() < 0.5 else "DESC"
                window_clause = f"OVER(PARTITION BY 1 ORDER BY 1 {direction})"
            elif window_clause_type == 4:
                # Window frame with position
                direction = "ASC" if random.random() < 0.5 else "DESC"
                frame_options = [
                    "ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW",
                    "ROWS BETWEEN 1 PRECEDING AND CURRENT ROW",
                    "ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING",
                    f"ROWS BETWEEN {random.randint(1, 5)} PRECEDING AND {random.randint(1, 5)} FOLLOWING",
                ]
                frame = random.choice(frame_options)
                window_clause = f"OVER(ORDER BY 1 {direction} {frame})"
            else:
                # RANGE or GROUPS window frame with position
                direction = "ASC" if random.random() < 0.5 else "DESC"
                frame_type = random.choice(["RANGE", "GROUPS"])
                frame_options = [
                    "BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW",
                    "BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING",
                    "BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING",
                ]
                frame = random.choice(frame_options)
                window_clause = f"OVER(ORDER BY 1 {direction} {frame_type} {frame})"

            return f"""
            SELECT * FROM (
                SELECT * FROM ({inner_query}) 
                WHERE {alias} IN (
                    SELECT ({window_func}({func_args}) {window_clause}) FROM ({values_expr})
                )
            );"""

    def generate_multi_table_join(self, tables_info):
        if not tables_info or len(tables_info) < 2:
            return "SELECT 1;"

        valid_tables = [t for t in tables_info if tables_info[t]["columns"]]
        if len(valid_tables) < 2:
            return f"SELECT * FROM {valid_tables[0]} LIMIT 5;"

        tables_to_join = random.sample(valid_tables, min(3, len(valid_tables)))

        join_parts = []
        select_parts = []

        base_table = tables_to_join[0]
        join_parts.append(f"FROM {base_table}")

        if tables_info[base_table]["columns"]:
            col = random.choice(tables_info[base_table]["columns"])
            select_parts.append(f"{base_table}.{col} as {base_table}_val")

        for i, table in enumerate(tables_to_join[1:], 1):
            join_type = random.choice(["LEFT JOIN", "INNER JOIN", "LEFT OUTER JOIN"])

            if tables_info[table]["columns"]:
                col = random.choice(tables_info[table]["columns"])
                select_parts.append(f"{table}.{col} as {table}_val")

            base_without_rowid = tables_info[base_table].get("without_rowid", False)
            table_without_rowid = tables_info[table].get("without_rowid", False)

            if base_without_rowid or table_without_rowid:
                if tables_info[base_table]["columns"] and tables_info[table]["columns"]:
                    base_col = tables_info[base_table]["columns"][0]
                    table_col = tables_info[table]["columns"][0]
                    join_condition = f"{base_table}.{base_col} = {table}.{table_col}"
                else:
                    join_condition = "1=1"
            else:
                join_condition = f"{base_table}.ROWID = {table}.ROWID"

            join_parts.append(f"{join_type} {table} ON {join_condition}")

        where_clause = ""
        if random.random() < 0.8:
            table = random.choice(tables_to_join)
            if tables_info[table]["columns"]:
                col = random.choice(tables_info[table]["columns"])
                where_clause = f"\nWHERE {table}.{col} IS NOT NULL"

        query = (
            f"SELECT {', '.join(select_parts)}\n" + "\n".join(join_parts) + where_clause
        )

        if select_parts:
            first_part = select_parts[0]
            if " as " in first_part.lower():
                column_part = first_part.split(" as ")[0].strip()
                query += f"\nORDER BY {column_part}"

            else:
                query += f"\nORDER BY {first_part}"
        else:
            query += "\nORDER BY 1"

        query += "\nLIMIT 20;"

        return query

    def generate_literal_value(self):
        options = [
            lambda: str(random.randint(-1000000, 1000000)),
            lambda: f"'{random_string(random.randint(1, 20))}'",
            lambda: f"x'{random_hex_string(random.randint(2, 8))}'",
            lambda: "NULL",
            lambda: "TRUE",
            lambda: "FALSE",
        ]
        return random.choice(options)()

    def generate_values_expr(self, rows=1, cols=1):
        values_rows = []
        for _ in range(rows):
            row_values = [self.generate_literal_value() for _ in range(cols)]
            values_rows.append(f"({', '.join(row_values)})")

        return f"VALUES {', '.join(values_rows)}"

    def generate_expr(
        self,
        depth=0,
        tables_info=None,
        max_depth=3,
        allow_aggregates=True,
        is_where_clause=False,
    ):
        if is_where_clause:
            allow_aggregates = False

        if depth >= max_depth:
            if tables_info and random.random() < 0.7:
                table = random.choice(list(tables_info.keys()))
                if tables_info[table]["columns"]:
                    col = random.choice(tables_info[table]["columns"])
                    return f"{table}.{col}"

            return self.generate_literal_value()

        options = []

        options.append(lambda: self.generate_literal_value())

        if tables_info:
            options.append(lambda: self.generate_column_reference(tables_info))

        options.append(
            lambda: f"{random.choice(['NOT', '+', '-', '~'])} {self.generate_expr(depth + 1, tables_info, max_depth, allow_aggregates)}"
        )

        def binary_op():
            left = self.generate_expr(
                depth + 1, tables_info, max_depth, allow_aggregates
            )
            right = self.generate_expr(
                depth + 1, tables_info, max_depth, allow_aggregates
            )
            op = random.choice(
                [
                    "+",
                    "-",
                    "*",
                    "/",
                    "%",
                    "||",
                    "<<",
                    ">>",
                    "&",
                    "|",
                    "<",
                    "<=",
                    ">",
                    ">=",
                    "=",
                    "==",
                    "!=",
                    "<>",
                    "AND",
                    "OR",
                    "IS",
                    "IS NOT",
                    "LIKE",
                    "GLOB",
                ]
            )
            return f"({left} {op} {right})"

        options.append(binary_op)

        def function_call():
            if is_where_clause:
                func = random.choice(self.scalar_functions)
            elif allow_aggregates:
                func = random.choice(self.scalar_functions + self.aggregate_functions)
            else:
                func = random.choice(self.scalar_functions)

            if func == "COUNT" and random.random() < 0.5 and allow_aggregates:
                return f"{func}(*)"

            if func in self.function_requirements:
                req = self.function_requirements[func]

                if func == "ZEROBLOB":
                    return f"{func}({random.randint(1, 100)})"

                if isinstance(req["args"], list):
                    num_args = random.choice(req["args"])
                else:
                    num_args = req["args"]

                args = []
                for _ in range(num_args):
                    is_aggregate = func in self.aggregate_functions
                    args.append(
                        self.generate_expr(
                            depth + 1,
                            tables_info,
                            max_depth,
                            allow_aggregates=not is_aggregate and not is_where_clause,
                            is_where_clause=is_where_clause,
                        )
                    )

                if "special" in req:
                    args = req["special"](args)

                args_str = ", ".join(args)
                return f"{func}({args_str})"
            else:
                num_args = random.randint(1, 3)

                args = []
                for _ in range(num_args):
                    args.append(
                        self.generate_expr(
                            depth + 1, tables_info, max_depth, allow_aggregates
                        )
                    )

                args_str = ", ".join(args)
                return f"{func}({args_str})"

        options.append(function_call)

        def case_expr():
            if random.random() < 0.5:
                case_val = self.generate_expr(
                    depth + 1, tables_info, max_depth, allow_aggregates=False
                )
                result = f"CASE {case_val} "

                for _ in range(random.randint(1, 3)):
                    when_val = self.generate_expr(
                        depth + 1, tables_info, max_depth, allow_aggregates=False
                    )

                    then_val = self.generate_expr(
                        depth + 1,
                        tables_info,
                        max_depth,
                        allow_aggregates=allow_aggregates,
                    )
                    result += f"WHEN {when_val} THEN {then_val} "

                if random.random() < 0.7:
                    else_val = self.generate_expr(
                        depth + 1,
                        tables_info,
                        max_depth,
                        allow_aggregates=allow_aggregates,
                    )
                    result += f"ELSE {else_val} "

                result += "END"
                return result
            else:
                result = "CASE "

                for _ in range(random.randint(1, 3)):
                    when_condition = self.generate_expr(
                        depth + 1, tables_info, max_depth, allow_aggregates=False
                    )

                    then_val = self.generate_expr(
                        depth + 1,
                        tables_info,
                        max_depth,
                        allow_aggregates=allow_aggregates,
                    )
                    result += f"WHEN {when_condition} THEN {then_val} "

                if random.random() < 0.7:
                    else_val = self.generate_expr(
                        depth + 1,
                        tables_info,
                        max_depth,
                        allow_aggregates=allow_aggregates,
                    )
                    result += f"ELSE {else_val} "

                result += "END"
                return result

        options.append(case_expr)

        if depth < max_depth - 1 and tables_info:

            def subquery_expr():
                if random.random() < 0.5:
                    col_ref = self.generate_column_reference(tables_info)

                    table = random.choice(list(tables_info.keys()))
                    if tables_info[table]["columns"]:
                        col = random.choice(tables_info[table]["columns"])
                        return (
                            f"{col_ref} IN (SELECT {table}.{col} FROM {table} LIMIT 5)"
                        )
                    else:
                        return f"{col_ref} IN (SELECT 1 FROM {table} LIMIT 5)"
                else:
                    return f"EXISTS (SELECT 1 FROM {random.choice(list(tables_info.keys()))} LIMIT 1)"

            options.append(subquery_expr)

        expr_generator = random.choice(options)
        return expr_generator()

    def generate_column_reference(self, tables_info):
        if not tables_info:
            return "1"

        valid_tables = [
            table for table in tables_info.keys() if tables_info[table]["columns"]
        ]

        if not valid_tables:
            return "1"

        table = random.choice(valid_tables)
        col = random.choice(tables_info[table]["columns"])

        if random.random() < 0.5:
            return f"{table}.{col}"
        return col

    def generate_result_column(self, tables_info, is_compound_query=False):
        if not tables_info:
            return "1"

        options = []

        options.append(lambda: self.generate_column_reference(tables_info))

        if not is_compound_query:
            options.append(lambda: "*")

            if random.random() < 0.3:
                options.append(lambda: f"{random.choice(list(tables_info.keys()))}.*")

        def expr_with_alias():
            expr = self.generate_expr(0, tables_info, 2)

            if random.random() < 0.5:
                alias = f"alias_{random_string(3)}"
                return f"{expr} AS {alias}"
            return expr

        options.append(expr_with_alias)

        result_col_generator = random.choice(options)
        return result_col_generator()

    def generate_select_core(
        self,
        tables_info,
        include_order_by=True,
        include_limit=True,
        fixed_num_columns=None,
    ):
        is_compound_query = fixed_num_columns is not None

        if not tables_info:
            return "SELECT 1"

        select_distinct = " DISTINCT" if random.random() < 0.2 else ""
        query = f"SELECT{select_distinct}"

        valid_tables = list(tables_info.keys())
        if not valid_tables:
            return "SELECT 1"

        num_tables = min(random.randint(1, 3), len(valid_tables))
        selected_tables = random.sample(valid_tables, num_tables)

        filtered_tables_info = {table: tables_info[table] for table in selected_tables}

        num_columns = (
            fixed_num_columns if fixed_num_columns is not None else random.randint(1, 5)
        )
        result_columns = []

        for _ in range(num_columns):
            result_columns.append(
                self.generate_result_column(filtered_tables_info, is_compound_query)
            )

        query += f" {', '.join(result_columns)}"

        if random.random() < 0.7 or len(selected_tables) < 2:
            query += f" FROM {', '.join(selected_tables)}"
        else:
            join_tables = random.sample(selected_tables, min(2, len(selected_tables)))
            join_type = random.choice(self.join_types)

            query += f" FROM {join_tables[0]} {join_type} {join_tables[1]}"

            if not join_type.startswith("NATURAL") and join_type != "CROSS JOIN":
                if random.random() < 0.7:
                    table1_col = None
                    table2_col = None

                    if filtered_tables_info[join_tables[0]]["columns"]:
                        table1_col = random.choice(
                            filtered_tables_info[join_tables[0]]["columns"]
                        )

                    if filtered_tables_info[join_tables[1]]["columns"]:
                        table2_col = random.choice(
                            filtered_tables_info[join_tables[1]]["columns"]
                        )

                    if table1_col and table2_col:
                        query += f" ON {join_tables[0]}.{table1_col} = {join_tables[1]}.{table2_col}"
                    else:
                        query += " ON 1=1"
                else:
                    common_cols = []

                    if (
                        filtered_tables_info[join_tables[0]]["columns"]
                        and filtered_tables_info[join_tables[1]]["columns"]
                    ):
                        for col in filtered_tables_info[join_tables[0]]["columns"]:
                            if col in filtered_tables_info[join_tables[1]]["columns"]:
                                common_cols.append(col)

                    if common_cols:
                        using_cols = random.sample(
                            common_cols, min(2, len(common_cols))
                        )
                        query += f" USING ({', '.join(using_cols)})"
                    else:
                        query += " ON 1=1"

            remaining_tables = [t for t in selected_tables if t not in join_tables[:2]]
            for table in remaining_tables:
                join_type = random.choice(self.join_types)
                query += f" {join_type} {table}"

                if not join_type.startswith("NATURAL") and join_type != "CROSS JOIN":
                    query += " ON 1=1"

        if random.random() < 0.7:
            query += f" WHERE {self.generate_expr(0, filtered_tables_info, 2, allow_aggregates=False, is_where_clause=True)}"

        if random.random() < 0.3:
            group_cols = []
            table = None

            if filtered_tables_info:
                table = random.choice(list(filtered_tables_info.keys()))

                if filtered_tables_info[table]["columns"]:
                    num_group_cols = min(
                        random.randint(1, 3),
                        len(filtered_tables_info[table]["columns"]),
                    )
                    group_cols = random.sample(
                        filtered_tables_info[table]["columns"], num_group_cols
                    )

            if group_cols:
                query += f" GROUP BY {', '.join(group_cols)}"

                if random.random() < 0.3:
                    query += f" HAVING {self.generate_expr(0, {table: filtered_tables_info[table]}, 2)}"

        if include_order_by:
            if random.random() < 0.3 and result_columns:
                pos = random.randint(1, len(result_columns))
                direction = " ASC" if random.random() < 0.5 else " DESC"
                query += f" ORDER BY {pos}{direction}"
            else:
                query += " ORDER BY 1"

        if include_limit and random.random() < 0.4:
            limit = random.randint(1, 100)
            query += f" LIMIT {limit}"

            if random.random() < 0.3:
                offset = random.randint(0, 20)
                if random.random() < 0.5:
                    query += f" OFFSET {offset}"
                else:
                    query += f", {offset}"

        return query

    def generate_select_stmt(self, tables_info):
        with_clause = ""
        if random.random() < 0.2 and tables_info:
            cte_name = f"cte_{random_string(3)}"
            table = random.choice(list(tables_info.keys()))
            with_clause = f"WITH {cte_name} AS (SELECT * FROM {table} LIMIT 10) "

        will_use_compound = random.random() < 0.2 and tables_info

        num_columns = random.randint(1, 5) if will_use_compound else None

        select_core = self.generate_select_core(
            tables_info,
            include_order_by=not will_use_compound,
            include_limit=not will_use_compound,
            fixed_num_columns=num_columns,
        )

        compound = ""
        if will_use_compound:
            compound_op = random.choice(["UNION", "UNION ALL", "INTERSECT", "EXCEPT"])

            second_select = self.generate_select_core(
                tables_info,
                include_order_by=False,
                include_limit=False,
                fixed_num_columns=num_columns,
            )
            compound = f" {compound_op} {second_select}"

            pos = random.randint(1, num_columns)
            direction = " ASC" if random.random() < 0.5 else " DESC"
            compound += f" ORDER BY {pos}{direction}"

            if random.random() < 0.4:
                limit = random.randint(1, 100)
                compound += f" LIMIT {limit}"

                if random.random() < 0.3:
                    offset = random.randint(0, 20)
                    if random.random() < 0.5:
                        compound += f" OFFSET {offset}"
                    else:
                        compound = compound.replace(
                            f" LIMIT {limit}", f" LIMIT {limit}, {offset}"
                        )

        return f"{with_clause}{select_core}{compound}"

    def generate_insert_stmt(self, table_name, column_names, column_types=None):
        if not column_names:
            return ""

        column_types = column_types or {}

        with_clause = ""
        if random.random() < 0.1:
            cte_name = f"cte_{random_string(3)}"
            with_clause = f"WITH {cte_name} AS (SELECT 1) "

        insert_variant = random.choice(
            ["INSERT OR IGNORE INTO", "INSERT OR REPLACE INTO", "REPLACE INTO"]
        )

        col_list = f"({', '.join(column_names)})"

        if random.random() < 0.8:
            num_rows = random.randint(1, 2)
            rows = []

            for i in range(num_rows):
                values = []
                timestamp = int(time.time()) % 10000
                for idx, col in enumerate(column_names):
                    col_type = column_types.get(col)

                    unique_id = i * 10000 + idx * 100 + timestamp
                    values.append(
                        random_value(
                            include_null=True,
                            data_type=col_type,
                            is_unique=True,
                            unique_id=unique_id,
                        )
                    )

                rows.append(f"({', '.join(values)})")

            values_clause = f"VALUES {', '.join(rows)}"

            return (
                f"{with_clause}{insert_variant} {table_name} {col_list} {values_clause}"
            )
        else:
            select_cols = []
            timestamp = int(time.time()) % 10000
            for idx, col in enumerate(column_names):
                col_type = column_types.get(col)

                select_cols.append(
                    random_value(
                        include_null=True,
                        data_type=col_type,
                        is_unique=True,
                        unique_id=idx * 100 + timestamp,
                    )
                )

            select_clause = f"SELECT {', '.join(select_cols)}"

            return (
                f"{with_clause}{insert_variant} {table_name} {col_list} {select_clause}"
            )

    def generate_update_stmt(
        self, table_name, column_names, column_types=None, without_rowid=False
    ):
        if not column_names:
            return ""

        valid_columns = column_names if column_names else []
        if not valid_columns:
            return ""

        column_types = column_types or {}

        with_clause = ""
        if random.random() < 0.1:
            cte_name = f"cte_{random_string(3)}"
            with_clause = f"WITH {cte_name} AS (SELECT 1) "

        update_variant = random.choice(
            [
                "UPDATE",
                "UPDATE OR REPLACE",
                "UPDATE OR IGNORE",
                "UPDATE OR IGNORE",
                "UPDATE OR FAIL",
            ]
        )

        num_cols = min(random.randint(1, 3), len(column_names))
        set_cols = random.sample(column_names, num_cols)

        primary_key_cols = []
        for col in column_names:
            col_type = str(column_types.get(col, ""))
            if "PRIMARY KEY" in col_type:
                primary_key_cols.append(col)

        set_exprs = []
        for col in set_cols:
            col_type = column_types.get(col)
            is_primary_key = col in primary_key_cols or (
                isinstance(col_type, str) and "PRIMARY KEY" in col_type
            )

            if is_primary_key:
                continue

            if col_type == "TEXT":
                if without_rowid:
                    set_exprs.append(f"{col} = {col} || '_' || random()")
                else:
                    set_exprs.append(f"{col} = {col} || '_' || ROWID")
            else:
                if random.random() < 0.3:
                    set_exprs.append(f"{col} = NULL")
                else:
                    val = random_value(data_type=col_type)
                    set_exprs.append(f"{col} = {val}")

        if not set_exprs:
            non_pk_cols = [c for c in column_names if c not in primary_key_cols]
            if non_pk_cols:
                col = random.choice(non_pk_cols)
                set_exprs.append(f"{col} = NULL")

        set_clause = f"SET {', '.join(set_exprs)}"

        where_clause = ""
        if random.random() < 0.8 and column_names:
            col = random.choice(column_names)

            op = random.choice(["=", "IS NULL", "IS NOT NULL", ">", "<"])

            if op in ("IS NULL", "IS NOT NULL"):
                where_clause = f" WHERE {col} {op}"
            else:
                if without_rowid:
                    where_clause = f" WHERE {col} {op} {random_value(data_type=column_types.get(col))}"
                else:
                    where_clause = f" WHERE ROWID = (SELECT MIN(ROWID) FROM {table_name} WHERE ROWID IS NOT NULL)"
        else:
            if without_rowid:
                pk_col = column_names[0] if column_names else "pk"
                where_clause = f" WHERE {pk_col} IS NOT NULL"
            else:
                where_clause = f" WHERE ROWID = (SELECT MIN(ROWID) FROM {table_name} WHERE ROWID IS NOT NULL)"

        return f"{with_clause}{update_variant} {table_name} {set_clause}{where_clause}"

    def generate_delete_stmt(self, table_name, column_names, column_types=None):
        with_clause = ""
        if random.random() < 0.1:
            cte_name = f"cte_{random_string(3)}"
            with_clause = f"WITH {cte_name} AS (SELECT 1) "

        delete_clause = f"DELETE FROM {table_name}"

        where_clause = ""
        if random.random() < 0.3 and column_names:

            expr = self.generate_expr(
                0,
                {table_name: {"columns": column_names}},
                max_depth=2,
                allow_aggregates=False,
                is_where_clause=True,
            )
            where_clause = f" WHERE {expr}"

        return f"{with_clause}{delete_clause}{where_clause}"

    def generate_alter_table_stmt(self, tables_info):
        """Generate ALTER TABLE statements with proper updates to tables_info."""
        if not tables_info:
            return None, tables_info

        # Choose a table to alter
        table_name = random.choice(list(tables_info.keys()))
        table_data = tables_info[table_name]

        # Choose the ALTER TABLE operation
        op_type = random.choice(["RENAME TABLE", "RENAME COLUMN", "ADD COLUMN"])

        # Create a copy of tables_info to modify
        updated_tables_info = {k: v.copy() for k, v in tables_info.items()}

        if op_type == "RENAME TABLE":
            new_table_name = f"t_{random_string(random.randint(3, 10))}"

            # Update the tables_info structure
            updated_tables_info[new_table_name] = updated_tables_info.pop(table_name)

            # Generate the ALTER TABLE statement
            return (
                f"ALTER TABLE {table_name} RENAME TO {new_table_name};",
                updated_tables_info,
            )

        elif op_type == "RENAME COLUMN" and table_data.get("columns"):
            # Choose a column to rename
            if not table_data["columns"]:
                return None, tables_info

            col_name = random.choice(table_data["columns"])
            new_col_name = f"c_{random_string(random.randint(3, 10))}"

            # Update the column list
            column_index = updated_tables_info[table_name]["columns"].index(col_name)
            updated_tables_info[table_name]["columns"][column_index] = new_col_name

            # Update the column types dictionary
            if "types" in updated_tables_info[table_name]:
                if col_name in updated_tables_info[table_name]["types"]:
                    updated_tables_info[table_name]["types"][new_col_name] = (
                        updated_tables_info[table_name]["types"].pop(col_name)
                    )

            # Generate the ALTER TABLE statement
            return (
                f"ALTER TABLE {table_name} RENAME COLUMN {col_name} TO {new_col_name};",
                updated_tables_info,
            )

        elif op_type == "ADD COLUMN":
            # Generate new column
            new_col_name = f"c_{random_string(random.randint(3, 10))}"
            data_type = random.choice(self.data_types)

            # Prepare constraints
            constraints = []

            # SQLite doesn't allow adding NOT NULL columns without DEFAULT
            if random.random() < 0.3:
                constraints.append(f"DEFAULT {random_value(data_type=data_type)}")

            if random.random() < 0.1 and data_type == "TEXT":
                collation = random.choice(["BINARY", "NOCASE", "RTRIM"])
                constraints.append(f"COLLATE {collation}")

            column_def = f"{new_col_name} {data_type}" + (
                "" if not constraints else f" {' '.join(constraints)}"
            )

            # Update the tables_info structure
            updated_tables_info[table_name]["columns"].append(new_col_name)
            if "types" in updated_tables_info[table_name]:
                updated_tables_info[table_name]["types"][new_col_name] = data_type

            # Generate the ALTER TABLE statement
            return (
                f"ALTER TABLE {table_name} ADD COLUMN {column_def};",
                updated_tables_info,
            )

        return None, tables_info

    def generate_create_index_stmt(self, table_name, column_names):
        if not column_names:
            return ""

        unique = "UNIQUE " if random.random() < 0.2 else ""

        if_not_exists = "IF NOT EXISTS " if random.random() < 0.7 else ""

        index_name = f"idx_{random_string(5)}"

        num_cols = min(random.randint(1, 3), len(column_names))
        chosen_cols = random.sample(column_names, num_cols)

        indexed_columns = []
        for col in chosen_cols:
            col_def = col

            if random.random() < 0.2:
                func = random.choice(["UPPER", "LOWER", "ABS", "LENGTH"])
                col_def += f"{func}({col})"

            if random.random() < 0.2:
                collation = random.choice(["BINARY", "NOCASE", "RTRIM"])
                col_def += f" COLLATE {collation}"

            if random.random() < 0.5:
                direction = random.choice(["ASC", "DESC"])
                col_def += f" {direction}"

            indexed_columns.append(col_def)

        where_clause = ""
        if random.random() < 0.3 and column_names:
            col = random.choice(column_names)
            op = random.choice(
                ["=", ">", "<", ">=", "<=", "!=", "IS NULL", "IS NOT NULL"]
            )

            if op in ("IS NULL", "IS NOT NULL"):
                where_clause = f" WHERE {col} {op}"
            else:
                val = random_value()
                where_clause = f" WHERE {col} {op} {val}"

        return f"CREATE {unique}INDEX {if_not_exists}{index_name} ON {table_name}({', '.join(indexed_columns)}){where_clause}"

    def generate_create_trigger_stmt(self, table_name, column_names):
        if not column_names:
            return ""

        trigger_name = f"trg_{random_string(5)}"
        trigger_time = random.choice(["BEFORE", "AFTER"])
        trigger_event = random.choice(["INSERT", "UPDATE", "DELETE"])

        event_clause = trigger_event
        if trigger_event == "UPDATE" and random.random() < 0.3:
            update_cols = random.sample(column_names, min(2, len(column_names)))
            event_clause = f"{trigger_event} OF {', '.join(update_cols)}"

        action = f"""BEGIN
                    SELECT RAISE(IGNORE) WHERE (SELECT count(*) FROM {table_name}) > 1000;
                END"""

        return f"""
                CREATE TRIGGER {trigger_name}
                {trigger_time} {event_clause} ON {table_name}
                {action};"""

    def generate_pragma_stmt(self):
        pragma_name = random.choice(self.pragmas)

        if random.random() < 0.7:
            return f"PRAGMA {pragma_name};"

        pragma_value = None

        if pragma_name in ["journal_mode"]:
            pragma_value = random.choice(
                ["DELETE", "TRUNCATE", "PERSIST", "MEMORY", "WAL", "OFF"]
            )
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
        elif pragma_name in ["foreign_key_check"]:
            return f"PRAGMA {pragma_name};"
        else:
            pragma_value = random.choice(["0", "1"])

        if random.random() < 0.5:
            return f"PRAGMA {pragma_name} = {pragma_value};"
        else:
            return f"PRAGMA {pragma_name}({pragma_value});"

    def generate_upsert_stmt(self, table_name, column_names, column_types=None):
        if not column_names or len(column_names) < 2:
            return ""

        conflict_candidates = []

        for col in column_names:
            col_type = str(column_types.get(col, ""))
            if "PRIMARY KEY" in col_type or "UNIQUE" in col_type:
                conflict_candidates.append(col)

        if not conflict_candidates:
            return ""

        num_cols = min(len(column_names), random.randint(2, len(column_names)))
        chosen_cols = random.sample(column_names, num_cols)

        col_list = f"({', '.join(chosen_cols)})"

        target_col = random.choice(conflict_candidates)

        if random.random() < 0.3:
            conflict_action = "DO NOTHING"
        else:
            update_cols = random.sample(
                [c for c in chosen_cols if c != target_col],
                min(random.randint(1, 3), len(chosen_cols) - 1),
            )

            set_pairs = []
            for col in update_cols:
                set_pairs.append(f"{col} = excluded.{col}")

            conflict_action = f"DO UPDATE SET {', '.join(set_pairs)}"

        values = []
        timestamp = int(time.time()) % 10000

        for idx, col in enumerate(chosen_cols):
            col_type = column_types.get(col) if column_types else None
            unique_id = idx * 100 + timestamp

            if col == target_col:
                if col_type == "REAL":
                    return str(int(random_int() + unique_id))
                else:
                    values.append(
                        random_value(
                            include_null=False,
                            data_type=col_type,
                            is_unique=True,
                            unique_id=unique_id,
                        )
                    )
            else:
                values.append(
                    random_value(
                        include_null=False,
                        data_type=col_type,
                        is_unique=True,
                        unique_id=unique_id,
                    )
                )

        return f"""INSERT INTO {table_name} {col_list}
                VALUES ({", ".join(values)})
                ON CONFLICT({target_col}) {conflict_action};"""


def random_string(length=1, include_special=False):
    chars = string.ascii_letters + string.digits
    if include_special:
        chars += "_-$#@!%^&*()."
    return "".join(random.choices(chars, k=length))


def random_hex_string(length):
    hex_chars = "0123456789ABCDEF"

    if length % 2 != 0:
        length += 1
    return "".join(random.choices(hex_chars, k=length))


def random_table_name():
    return f"t_{random_string(random.randint(3, 10))}"


def random_column_name():
    return f"c_{random_string(random.randint(3, 10))}"


def random_int(min_val=-1000000, max_val=1000000):
    return random.randint(min_val, max_val)


def random_float():
    return round(random.uniform(-1000000, 1000000), random.randint(1, 6))


def random_value(
    include_null=True, hex_limit=8, data_type=None, is_unique=False, unique_id=0
):
    if include_null and random.random() < 0.1 and not is_unique:
        return "NULL"

    if data_type:
        if data_type == "INTEGER":
            offset = unique_id * 10000 if is_unique else 0
            return str(random_int() + offset)
        elif data_type == "REAL":
            offset = unique_id * 10.0 if is_unique else 0
            return str(random_float() + offset)
        elif data_type == "TEXT":
            unique_suffix = f"_{unique_id}" if is_unique else ""
            return f"'{random_string(random.randint(1, 20))}{unique_suffix}'"
        elif data_type == "NUMERIC":
            offset = unique_id * 10000 if is_unique else 0
            return str(random_int() + offset)
        elif data_type == "BLOB":
            return f"x'{random_hex_string(random.randint(2, hex_limit))}'"
        else:
            unique_suffix = f"_{unique_id}" if is_unique else ""
            return f"'{random_string(random.randint(1, 20))}{unique_suffix}'"

    value_types = [
        lambda: str(random_int()),
        lambda: str(random_float()),
        lambda: f"'{random_string(random.randint(1, 20), include_special=False)}'",
        lambda: f"x'{random_hex_string(random.randint(2, hex_limit))}'",
        lambda: f"'{random.choice(['true', 'false'])}'",
        lambda: f"'{random.randint(1900, 2100)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}'",
    ]
    return random.choice(value_types)()


def generate_test_case():
    grammar = SQLiteGrammar()
    num_tables = random.randint(1, 5)
    tables_info = {}
    statements = []
    in_transaction = False

    if random.random() < 0.3:
        statements.append(grammar.generate_pragma_stmt())

    for _ in range(num_tables):
        table_name, column_names, column_types, create_stmt, has_without_rowid = (
            grammar.generate_create_table_stmt()
        )
        statements.append(create_stmt + ";")
        tables_info[table_name] = {
            "columns": column_names,
            "types": column_types,
            "without_rowid": has_without_rowid,
        }

    if random.random() < 0.4 and tables_info:
        num_alters = random.randint(1, 3)
        for _ in range(num_alters):
            alter_stmt, updated_tables_info = grammar.generate_alter_table_stmt(
                tables_info
            )
            if alter_stmt:
                statements.append(alter_stmt)
                tables_info = updated_tables_info

    if random.random() < 0.3:
        for table_name, table_data in tables_info.items():
            if random.random() < 0.5:
                column_names = table_data["columns"]
                trigger_stmt = grammar.generate_create_trigger_stmt(
                    table_name, column_names
                )
                statements.append(trigger_stmt)

    for table_name, table_data in tables_info.items():
        column_names = table_data["columns"]
        column_types = table_data["types"]
        num_rows = random.randint(1, 5)
        for _ in range(num_rows):
            insert_stmt = grammar.generate_insert_stmt(
                table_name, column_names, column_types
            )
            statements.append(insert_stmt + ";")

    for table_name in tables_info:
        if random.random() < 0.2:
            statements.append(
                grammar.generate_default_values_stmt(table_name, tables_info)
            )

    if random.random() < 0.3:
        for table_name, table_data in tables_info.items():
            column_names = table_data["columns"]
            column_types = table_data["types"]
            if len(column_names) >= 2:
                upsert_stmt = grammar.generate_upsert_stmt(
                    table_name, column_names, column_types
                )
                statements.append(upsert_stmt)

    if random.random() < 0.25 and tables_info:
        table_name = random.choice(list(tables_info.keys()))
        statements.append(f"""
        SELECT json_extract('{{"a": 1, "b": 2}}', '$.a') as json_value,
            json_type('{{"a": [1, 2]}}', '$.a') as json_type,
            json_array(1, 2, 3) as json_arr,
            json_object('key', 'value') as json_obj
        FROM {table_name} LIMIT 1;
            """)

    num_queries = random.randint(2, 5)

    for i in range(num_queries):
        if (
            in_transaction
            and i > 0
            and (
                "OR ROLLBACK" in statements[-1].upper()
                or "ROLLBACK" in statements[-1].upper()
            )
        ):
            in_transaction = False

            if random.random() < 0.3:
                statements.append("BEGIN TRANSACTION;")
                in_transaction = True

        stmt_type = random.choice(
            [
                "SELECT",
                "UPDATE",
                "DELETE",
                "CREATE INDEX",
                "PRAGMA",
                "ALTER",
                "WITH",
                "TRANSACTION",
            ]
        )

        if in_transaction and stmt_type == "TRANSACTION":
            stmt_type = "SELECT"

        elif stmt_type == "TRANSACTION" and not in_transaction:
            transaction = ["BEGIN TRANSACTION;"]
            in_transaction = True

            if tables_info:
                table_name = random.choice(list(tables_info.keys()))
                table_data = tables_info[table_name]
                column_names = table_data["columns"]
                column_types = table_data["types"]
                without_rowid = table_data.get("without_rowid", False)

                primary_key_cols = []
                for col in column_names:
                    col_type = str(column_types.get(col, ""))
                    if "PRIMARY KEY" in col_type:
                        primary_key_cols.append(col)

                tx_statements = []
                for _ in range(random.randint(1, 3)):
                    if random.random() < 0.5:
                        stmt = grammar.generate_insert_stmt(
                            table_name, column_names, column_types
                        )
                        if not any(
                            x in stmt
                            for x in ["OR IGNORE", "OR REPLACE", "REPLACE INTO"]
                        ):
                            stmt = stmt.replace("INSERT INTO", "INSERT OR IGNORE INTO")
                        tx_statements.append(stmt + ";")
                    else:
                        available_cols = []
                        for col in column_names:
                            col_type = str(column_types.get(col, ""))

                            if (
                                col not in primary_key_cols
                                and "PRIMARY KEY" not in col_type
                            ):
                                available_cols.append(col)

                        if available_cols:
                            if without_rowid:
                                where_clause = f" WHERE {column_names[0]} IS NOT NULL"
                            else:
                                where_clause = f" WHERE ROWID = (SELECT MIN(ROWID) FROM {table_name})"

                            col = random.choice(available_cols)
                            col_type = column_types.get(col)

                            if col_type == "TEXT":
                                val = f"'{random_string(5)}_{int(time.time())}'"
                                update_stmt = f"UPDATE OR IGNORE {table_name} SET {col} = {val}{where_clause}"
                            else:
                                is_primary_key = (
                                    col in primary_key_cols
                                    or "PRIMARY KEY" in str(col_type)
                                )

                                if is_primary_key:
                                    val = str(random.randint(-1000, 1000))
                                else:
                                    val = (
                                        random.random() < 0.3
                                        and "NULL"
                                        or str(random.randint(-1000, 1000))
                                    )

                                update_stmt = f"UPDATE OR IGNORE {table_name} SET {col} = {val}{where_clause}"

                            tx_statements.append(update_stmt + ";")
            else:
                tx_statements.append("SELECT 1;")

            if tx_statements:
                transaction.extend(tx_statements)
                transaction.append("COMMIT;")
                statements.extend(transaction)
                in_transaction = False
            else:
                in_transaction = False

    if tables_info:
        if random.random() < 0.05:
            statements.append(grammar.generate_recursive_cte(tables_info))

        if random.random() < 0.3:
            statements.append(grammar.generate_complex_window_query(tables_info))

        if random.random() < 0.3:
            statements.append(grammar.generate_json_query(tables_info))

        if random.random() < 0.3:
            statements.append(grammar.generate_subquery_madness(tables_info))

        if random.random() < 0.3:
            if len(tables_info) >= 2:
                statements.append(grammar.generate_multi_table_join(tables_info))

    if tables_info:
        for _ in range(random.randint(1, 3)):
            if random.random() < 0.7:
                table_name = random.choice(list(tables_info.keys()))
                column_names = tables_info[table_name]["columns"]

                if len(column_names) > 0:
                    cols_to_show = random.sample(
                        column_names, min(len(column_names), random.randint(1, 5))
                    )
                    cols_str = ", ".join(
                        [f"{table_name}.{col}" for col in cols_to_show]
                    )

                    if random.random() < 0.5 and len(cols_to_show) > 0:
                        col = random.choice(cols_to_show)
                        funcs = ["LENGTH", "UPPER", "LOWER", "TYPEOF", "ABS"]
                        func = random.choice(funcs)
                        cols_str += f", {func}({table_name}.{col}) AS computed_{col}"

                    order_clause = ""
                    if random.random() < 0.7 and len(cols_to_show) > 0:
                        order_col = random.choice(cols_to_show)
                        order_dir = "ASC" if random.random() < 0.5 else "DESC"
                        order_clause = f" ORDER BY {table_name}.{order_col} {order_dir}"

                    statements.append(
                        f"SELECT {cols_str} FROM {table_name}{order_clause} LIMIT 10;"
                    )
                else:
                    statements.append(f"SELECT * FROM {table_name} LIMIT 10;")
            else:
                statements.append(grammar.generate_select_stmt(tables_info) + ";")

        if random.random() < 0.2:
            table_name = random.choice(list(tables_info.keys()))
            columns = tables_info[table_name]["columns"]

            if columns:
                col1 = random.choice(columns)
                col2 = random.choice(columns)

                # Add stable ordering with multiple tie-breakers
                statements.append(f"""
                SELECT DISTINCT {table_name}.{col1},
                    COUNT(*) OVER (PARTITION BY {table_name}.{col2}) as window_count,
                    RANK() OVER (ORDER BY 
                            CASE WHEN typeof({table_name}.{col1}) IN ('null') THEN 0 
                            ELSE {table_name}.{col1} END DESC,
                            {table_name}.{col2} ASC     /* Only use columns that definitely exist */
                    ) as rank_val,
                    CASE WHEN {table_name}.{col1} IS NULL THEN 'Unknown' ELSE 'Known' END as status
                FROM {table_name}
                WHERE {table_name}.{col1} IS NOT NULL
                GROUP BY {table_name}.{col1}, {table_name}.{col2}
                HAVING COUNT(*) > 0
                /* Only use columns that definitely exist in ORDER BY */
                ORDER BY {table_name}.{col1} ASC, {table_name}.{col2} ASC, window_count DESC
                LIMIT 20;
                """)

                statements.append(f"""
                SELECT {table_name}.{col1},
                    {table_name}.{col2},
                    SUM(CASE WHEN typeof({table_name}.{col1}) IN ('integer', 'real', 'numeric') THEN {table_name}.{col1} ELSE 0 END) 
                        OVER (PARTITION BY {table_name}.{col2} ORDER BY {table_name}.{col1} ASC) as window_total
                FROM {table_name}
                GROUP BY {table_name}.{col1}, {table_name}.{col2}
                HAVING SUM(CASE WHEN typeof({table_name}.{col1}) IN ('integer', 'real', 'numeric') THEN {table_name}.{col1} ELSE 0 END) > 0
                ORDER BY window_total DESC, {table_name}.{col1} ASC, {table_name}.{col2} ASC
                LIMIT 10;
                """)
    else:
        statements.append("SELECT 1;")

    if in_transaction:
        statements.append("COMMIT;")

    return "\n".join(statements)
