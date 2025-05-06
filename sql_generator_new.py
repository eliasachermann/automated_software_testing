import random
import string
import sqlglot

SQL_TYPES = ["INTEGER", "TEXT", "REAL", "NUMERIC"]

class TableGenerator:
    def __init__(self):
        self.table_defs = {}

    def random_column_def(self, col_index):
        col_name = f"col{col_index}"
        col_type = random.choice(SQL_TYPES)
        constraints = []

        if random.random() < 0.3:
            constraints.append("PRIMARY KEY")
        if random.random() < 0.5:
            constraints.append("NOT NULL")

        col_def = f"{col_name} {col_type} {' '.join(constraints)}"
        return col_name, col_type, constraints, col_def

    def generate_create_table(self, table_name):
        num_cols = random.randint(2, 5)
        columns = []
        schema = {}

        for i in range(num_cols):
            col_name, col_type, constraints, col_def = self.random_column_def(i)
            columns.append(col_def)
            schema[col_name] = (col_type, constraints)

        create_stmt = f"CREATE TABLE {table_name} ({', '.join(columns)});"
        self.table_defs[table_name] = schema
        return create_stmt


class InsertGenerator:
    def __init__(self, table_defs):
        self.table_defs = table_defs
        self.pk_tracker = {}  # to avoid duplicate primary keys

    def random_value(self, col_type, not_null=True):
        # Handle NULL if allowed
        if not not_null and random.random() < 0.2:
            return "NULL"

        if col_type == "INTEGER":
            return str(random.randint(1, 1000))
        elif col_type == "REAL":
            return str(round(random.uniform(0.1, 1000.0), 2))
        elif col_type == "TEXT":
            return f"'{self.random_string()}'"
        else:
            return "NULL"  # fallback

    def random_string(self, length=5):
        return ''.join(random.choices(string.ascii_letters, k=length))

    def generate_insert(self, table_name):
        if table_name not in self.table_defs:
            raise ValueError(f"Unknown table: {table_name}")

        schema = self.table_defs[table_name]
        column_names = list(schema.keys())
        values = []

        for col_name, (col_type, constraints) in schema.items():
            not_null = "NOT NULL" in constraints or "PRIMARY KEY" in constraints
            val = self.random_value(col_type, not_null=not_null)

            # Simple primary key duplicate avoidance
            if "PRIMARY KEY" in constraints:
                used = self.pk_tracker.setdefault(table_name, set())
                while val in used:
                    val = self.random_value(col_type, not_null=True)
                used.add(val)

            values.append(val)

        insert_stmt = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(values)});"
        return insert_stmt

# Function to generate a random SQL query
def generate_random_query():
    query = ""

    return query

def generate_query():
    query = ""
    tg = TableGenerator()
    table_sql = tg.generate_create_table("t1")
    query += table_sql + "\n"
    print(table_sql)

    ig = InsertGenerator(tg.table_defs)
    for _ in range(5):
        query += ig.generate_insert("t1") + "\n"

    return query