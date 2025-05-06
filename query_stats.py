import re
import json

class SQLStatistics:
    def __init__(self):
        self.total_queries = 0
        self.valid_queries = 0
        self.invalid_queries = 0
        self.clauses_count = {
            "ABORT": 0, "ACTION": 0, "ADD": 0, "AFTER": 0, "ALL": 0, "ALTER": 0, "ANALYZE": 0, "AND": 0,
            "AS": 0, "ASC": 0, "ATTACH": 0, "AUTOINCREMENT": 0, "BEFORE": 0, "BEGIN": 0, "BETWEEN": 0,
            "BY": 0, "CASCADE": 0, "CASE": 0, "CAST": 0, "CHECK": 0, "COLLATE": 0, "COLUMN": 0, "COMMIT": 0,
            "CONFLICT": 0, "CONSTRAINT": 0, "CREATE": 0, "CROSS": 0, "DATABASE": 0, "DEFAULT": 0, "DEFERRABLE": 0, "DEFERRED": 0,
            "DELETE": 0, "DESC": 0, "DETACH": 0, "DISTINCT": 0, "DROP": 0, "EACH": 0, "ELSE": 0, "END": 0,
            "ESCAPE": 0, "EXCEPT": 0, "EXCLUSIVE": 0, "EXISTS": 0, "EXPLAIN": 0, "FAIL": 0, "FOR": 0,
            "FOREIGN": 0, "FROM": 0, "FULL": 0, "GLOB": 0, "GROUP": 0, "HAVING": 0, "IF": 0, "IGNORE": 0,
            "IMMEDIATE": 0, "IN": 0, "INDEX": 0, "INDEXED": 0, "INITIALLY": 0, "INNER": 0, "INSERT": 0,
            "INSTEAD": 0, "INTERSECT": 0, "INTO": 0, "IS": 0, "ISNULL": 0, "JOIN": 0, "KEY": 0, "LEFT": 0,
            "LIKE": 0, "LIMIT": 0, "MATCH": 0, "NATURAL": 0, "NO": 0, "NOT": 0, "NOTNULL": 0, "NULL": 0,
            "OF": 0, "OFFSET": 0, "ON": 0, "OR": 0, "ORDER": 0, "OUTER": 0, "PLAN": 0, "PRAGMA": 0,
            "PRIMARY": 0, "QUERY": 0, "RAISE": 0, "RECURSIVE": 0, "REFERENCES": 0,
            "REINDEX": 0, "RELEASE": 0, "RENAME": 0, "REPLACE": 0, "RESTRICT": 0,
            "ROLLBACK": 0, "ROW": 0, "ROWS": 0, "SAVEPOINT": 0, "SELECT": 0, "SET": 0,
            "TABLE": 0, "TEMP": 0, "TEMPORARY": 0, "THEN": 0, "TO": 0, "TRANSACTION": 0, "TRIGGER": 0,
            "UNION": 0, "UNIQUE": 0, "UPDATE": 0, "USING": 0, "VACUUM": 0, "VALUES": 0, "VIEW": 0,
            "VIRTUAL": 0, "WHEN": 0, "WHERE": 0, "WITH": 0, "WITHOUT": 0, "FIRST_VALUE": 0, "OVER": 0,
            "PARTITION": 0, "RANGE": 0, "PRECEDING": 0, "UNBOUNDED": 0, "CURRENT": 0, "FOLLOWING": 0,
            "CUME_DIST": 0, "DENSE_RANK": 0, "LAG": 0, "LAST_VALUE": 0, "LEAD": 0, "NTH_VALUE": 0,
            "NTILE": 0, "PERCENT_RANK": 0, "RANK": 0, "ROW_NUMBER": 0, "GENERATED": 0, "ALWAYS": 0,
            "STORED": 0, "TRUE": 0, "FALSE": 0, "WINDOW": 0, "NULLS": 0, "FIRST": 0, "LAST": 0, "FILTER": 0,
            "GROUPS": 0, "EXCLUDE": 0, "TIES": 0, "OTHERS": 0, "DO": 0, "NOTHING": 0,  "AND": 0, "OR": 0, "NOT": 0, "IS": 0, "IS NOT": 0, "IN": 0, "LIKE": 0, "GLOB": 0, "MATCH": 0,
            "BETWEEN": 0, "JOIN": 0, "INNER JOIN": 0, "LEFT JOIN": 0, "LEFT OUTER JOIN": 0, "CROSS JOIN": 0,
            "NATURAL JOIN": 0, "NATURAL LEFT JOIN": 0, "AVG": 0, "COUNT": 0, "GROUP_CONCAT": 0, "MAX": 0,
            "MIN": 0, "SUM": 0, "TOTAL": 0, "ABS": 0, "COALESCE": 0, "GLOB": 0, "IFNULL": 0, "INSTR": 0, "HEX": 0,
            "LENGTH": 0, "LIKE": 0, "LIKELIHOOD": 0, "LIKELY": 0, "LOAD_EXTENSION": 0, "LOWER": 0, "LTRIM": 0,
            "MATCH": 0, "NULLIF": 0, "PRINTF": 0, "QUOTE": 0, "REPLACE": 0, "ROUND": 0, "RTRIM": 0, "SOUNDEX": 0,
            "SQLITE_SOURCE_ID": 0, "SUBSTR": 0, "TRIM": 0, "TYPEOF": 0, "UNICODE": 0, "UNLIKELY": 0, "UPPER": 0,
            "ZEROBLOB": 0, "DATE": 0, "TIME": 0, "DATETIME": 0, "JULIANDAY": 0, "STRFTIME": 0, "ROW_NUMBER": 0,
            "RANK": 0, "DENSE_RANK": 0, "PERCENT_RANK": 0, "CUME_DIST": 0, "NTILE": 0, "LAG": 0, "LEAD": 0,
            "FIRST_VALUE": 0, "LAST_VALUE": 0, "NTH_VALUE": 0, "INTEGER": 0, "TEXT": 0, "REAL": 0, "NUMERIC": 0,
            "auto_vacuum": 0, "automatic_index": 0, "busy_timeout": 0, "cache_size": 0,
            "case_sensitive_like": 0, "cell_size_check": 0, "checkpoint_fullfsync": 0, "count_changes": 0,
            "defer_foreign_keys": 0, "foreign_key_check": 0, "foreign_key_list": 0, "foreign_keys": 0, "freelist_count": 0,
            "fullfsync": 0, "ignore_check_constraints": 0, "incremental_vacuum": 0, "integrity_check": 0,
            "journal_mode": 0, "journal_size_limit": 0, "locking_mode": 0, "max_page_count": 0, "mmap_size": 0,
            "page_count": 0, "page_size": 0, "parser_trace": 0, "query_only": 0, "quick_check": 0, "read_uncommitted": 0,
            "recursive_triggers": 0, "reverse_unordered_selects": 0, "secure_delete": 0, "shrink_memory": 0,
            "stats": 0, "synchronous": 0, "table_info": 0, "temp_store": 0, "threads": 0, "wal_autocheckpoint": 0,
            "wal_checkpoint": 0,
        }

        # missing
        # "=": 0, "==": 0, "<>": 0,"!=": 0, "<": 0, "<=": 0, ">": 0, ">=": 0, "+": 0, "-": 0, "*": 0, "/": 0, "%": 0, "||": 0, "&": 0, "|": 0, "<<": 0, ">>": 0, 


        self.total_depth = 0
        self.query_depth_count = 0
    
    def analyze_query(self, query, is_valid):
        # Count clauses in the query
        for clause in self.clauses_count:
            self.clauses_count[clause] += len(re.findall(rf"\b{clause}\b", query.upper()))
        
        # Count query depth (nested expressions)
        depth = self.calculate_depth(query)
        self.total_depth += depth
        self.query_depth_count += 1
        
        # Track validity of the query
        self.total_queries += 1
        if is_valid:
            self.valid_queries += 1
        else:
            self.invalid_queries += 1
    
    def calculate_depth(self, query):
        """
        Calculate nesting depth of SQL query based on subqueries and CASE WHEN nesting.
        Parentheses alone are not a good indicator, so this method focuses on real structures.
        """
        query = query.upper()
        
        # Remove content inside string literals to avoid false positives
        query = re.sub(r"'(.*?)'", '', query)
        query = re.sub(r'"(.*?)"', '', query)
        
        # Tokenize the query
        tokens = re.findall(r'\b\w+\b|\(|\)', query)

        depth = 0
        max_depth = 0

        for idx, token in enumerate(tokens):
            if token == '(':
                # Check if the previous token was FROM or IN (likely a subquery or list)
                prev_tokens = tokens[max(0, idx-3):idx]  # Look back up to 3 tokens
                prev_string = " ".join(prev_tokens)

                # If previous tokens suggest a subquery
                if re.search(r'\bFROM\b|\bIN\b|\bEXISTS\b|\bSELECT\b', prev_string):
                    depth += 1
                    max_depth = max(max_depth, depth)
            elif token == ')':
                if depth > 0:
                    depth -= 1
            elif token == 'CASE':
                # CASE increases depth
                depth += 1
                max_depth = max(max_depth, depth)
            elif token == 'END':
                # END reduces depth
                if depth > 0:
                    depth -= 1

        return max_depth
    
    def get_statistics(self):
        avg_depth = (self.total_depth / self.query_depth_count) if self.query_depth_count else 0
        return {
            'total_queries': self.total_queries,
            'valid_queries': self.valid_queries,
            'invalid_queries': self.invalid_queries,
            'clauses_count': self.clauses_count,
            'average_expression_depth': avg_depth
        }
    
    def print_statistics(self):
        stats = self.get_statistics()
        print("SQL Query Statistics:")
        print(f"Total Queries: {stats['total_queries']}")
        print(f"Valid Queries: {stats['valid_queries']}")
        print(f"Invalid Queries: {stats['invalid_queries']}")
        print("Clause Frequency:")
        for clause, count in stats['clauses_count'].items():
            print(f"  {clause}: {count}")
        print(f"Average Expression Depth: {stats['average_expression_depth']:.2f}")

    def save_statistics(self):
        stats = self.get_statistics()

        # Prepare the data to save
        data = {
            "Total Queries": stats['total_queries'],
            "Valid Queries": stats['valid_queries'],
            "Invalid Queries": stats['invalid_queries'],
            "Clause Frequency": stats['clauses_count'],
            "Average Expression Depth": round(stats['average_expression_depth'], 2)
        }

        # Write the data to a JSON file
        with open("query_stat.json", "w") as f:
            json.dump(data, f, indent=4)

        print("Statistics have been saved to query_stat.json.")
