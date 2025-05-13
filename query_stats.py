import re
import json
import sqlglot
from sqlglot.expressions import Expression

class SQLStatistics:
    def __init__(self):
        self.total_queries = 0
        self.valid_queries = 0
        self.invalid_queries = 0
        self.clauses_count = {
            "ABORT": 0, "ACTION": 0, "ADD": 0, "AFTER": 0, "ALL": 0, "ALTER": 0, "ALWAYS": 0,
            "ANALYZE": 0, "AND": 0, "AS": 0, "ASC": 0, "ATTACH": 0, "AUTOINCREMENT": 0,
            "BEFORE": 0, "BEGIN": 0, "BETWEEN": 0, "BINARY": 0, "BY": 0,
            "CASCADE": 0, "CASE": 0, "CAST": 0, "CHECK": 0, "COLLATE": 0, "COLUMN": 0,
            "COMMIT": 0, "CONFLICT": 0, "CONSTRAINT": 0, "CREATE": 0, "CROSS": 0,
            "CUME_DIST": 0, "CURRENT": 0, "DATABASE": 0, "DEFAULT": 0, "DEFERRABLE": 0,
            "DEFERRED": 0, "DELETE": 0, "DENSE_RANK": 0, "DESC": 0, "DETACH": 0,
            "DISTINCT": 0, "DO": 0, "DROP": 0, "EACH": 0, "ELSE": 0, "END": 0,
            "ESCAPE": 0, "EXCEPT": 0, "EXCLUDE": 0, "EXCLUSIVE": 0, "EXISTS": 0,
            "EXPLAIN": 0, "FAIL": 0, "FALSE": 0, "FILTER": 0, "FIRST": 0, "FIRST_VALUE": 0,
            "FOLLOWING": 0, "FOR": 0, "FOREIGN": 0, "FROM": 0, "FULL": 0,
            "GENERATED": 0, "GLOB": 0, "GROUP": 0, "GROUPS": 0, "HAVING": 0,
            "IF": 0, "IGNORE": 0, "IMMEDIATE": 0, "IN": 0, "INDEX": 0, "INDEXED": 0,
            "INITIALLY": 0, "INNER": 0, "INSERT": 0, "INSTEAD": 0, "INTERSECT": 0,
            "INTO": 0, "IS": 0, "ISNULL": 0, "JOIN": 0, "KEY": 0, "LAG": 0, "LAST": 0,
            "LAST_VALUE": 0, "LEAD": 0, "LEFT": 0, "LIKE": 0, "LIMIT": 0,
            "MEMORY": 0, "NATURAL": 0, "NO": 0, "NOT": 0, "NOTHING": 0, "NOTNULL": 0,
            "NTH_VALUE": 0, "NTILE": 0, "NULL": 0, "NULLS": 0, "OF": 0, "OFFSET": 0,
            "ON": 0, "OR": 0, "ORDER": 0, "OTHERS": 0, "OUTER": 0, "OVER": 0,
            "PARTITION": 0, "PERCENT_RANK": 0, "PLAN": 0, "PRAGMA": 0, "PRECEDING": 0,
            "PRIMARY": 0, "QUERY": 0, "RAISE": 0, "RANGE": 0, "RANK": 0, "RECURSIVE": 0,
            "REFERENCES": 0, "REINDEX": 0, "RELEASE": 0, "RENAME": 0, "REPLACE": 0,
            "RESTRICT": 0, "ROLLBACK": 0, "ROW": 0, "ROW_NUMBER": 0, "ROWS": 0,
            "RTRIM": 0, "SAVEPOINT": 0, "SELECT": 0, "SET": 0, "STORED": 0,
            "TABLE": 0, "TEMP": 0, "TEMPORARY": 0, "THEN": 0, "TIES": 0, "TO": 0,
            "TRANSACTION": 0, "TRIGGER": 0, "TRUE": 0, "UNBOUNDED": 0, "UNION": 0,
            "UNIQUE": 0, "UPDATE": 0, "USING": 0, "VACUUM": 0, "VALUES": 0, "VIEW": 0,
            "VIRTUAL": 0, "WHEN": 0, "WHERE": 0, "WINDOW": 0, "WITH": 0, "WITHOUT": 0,
        }

        self.query_depth_count = 0
    
    def analyze_query(self, query, is_valid):
        for clause in self.clauses_count:
            self.clauses_count[clause] += len(re.findall(rf"\b{clause}\b", query.upper()))       
        # Track validity of the query
        self.total_queries += 1
        if is_valid:
            self.valid_queries += 1
        else:
            self.invalid_queries += 1
    
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

    def save_statistics(self):
        stats = self.get_statistics()

        # Prepare the data to save
        data = {
            "Total Queries": stats['total_queries'],
            "Valid Queries": stats['valid_queries'],
            "Invalid Queries": stats['invalid_queries'],
            "Clause Frequency": stats['clauses_count'],
        }

        # Write the data to a JSON file
        with open("query_stat.json", "w") as f:
            json.dump(data, f, indent=4)

        print("Statistics have been saved to query_stat.json.")
