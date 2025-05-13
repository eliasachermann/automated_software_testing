import random
import re
import string

def mutate_sql_statement(sql: str) -> str:
    """
    Apply random mutations to a SQL statement while preserving syntactic validity.
    """
    # Don't mutate empty statements
    if not sql or sql.isspace():
        return sql
        
    mutations = []
    
    # Basic binary operator flips (already present, enhanced)
    operator_flips = {
        '=': ['<>', '!=', 'IS', '<=', '>='],
        '==': ['<>', '!=', 'IS', '<=', '>='],
        '<>': ['=', '==', 'IS NOT', '<', '>'],
        '!=': ['=', '==', 'IS NOT', '<', '>'],
        '>': ['>=', '<', '<=', '=', '!='],
        '<': ['<=', '>', '>=', '=', '!='],
        '>=': ['>', '=', '<>', '!=', '<='],
        '<=': ['<', '=', '<>', '!=', '>='],
        'IS NULL': ['IS NOT NULL', 'IS 0', '= 0', '= NULL'],
        'IS NOT NULL': ['IS NULL', 'IS NOT 0', '<> 0', '<> NULL'],
        'LIKE': ['NOT LIKE', 'GLOB', '=', 'REGEXP'],
        'NOT LIKE': ['LIKE', 'NOT GLOB', '<>', 'NOT REGEXP'],
    }
    mutations.append(lambda s: flip_operators(s, operator_flips))
    
    # Boolean logic transformations
    mutations.append(lambda s: transform_boolean_logic(s))
    
    # Add redundant conditions
    mutations.append(lambda s: add_redundant_condition(s))
    
    # Nest in subquery
    mutations.append(lambda s: nest_in_subquery(s))
    
    # Convert between equivalent forms
    mutations.append(lambda s: convert_query_form(s))
    
    # Modify result columns
    mutations.append(lambda s: modify_result_columns(s))
    
    # Add or modify sorting
    mutations.append(lambda s: modify_ordering(s))
    
    # Wrapping functions
    mutations.append(lambda s: wrap_with_cte(s))
    
    # Shuffle JOINs if possible
    mutations.append(lambda s: shuffle_joins(s))
    
    # Add harmless CASE expressions
    mutations.append(lambda s: add_case_expressions(s))
    
    # Add group by if possible
    mutations.append(lambda s: modify_grouping(s))
    
    # Modify input values
    mutations.append(lambda s: mutate_input_values(s))
    
    # Apply 1-3 random mutations
    num_mutations = random.randint(1, 3)
    mutated_sql = sql
    attempts = 0
    max_attempts = 10  # Add maximum attempts to prevent infinite loops
    
    for _ in range(num_mutations):
        mutation_applied = False
        attempts = 0
        
        while not mutation_applied and attempts < max_attempts:
            mutation_func = random.choice(mutations)
            new_sql = mutation_func(mutated_sql)
            # Only apply if the mutation produced a change and didn't break anything
            if new_sql != mutated_sql and is_valid_sql(new_sql):
                mutated_sql = new_sql
                mutation_applied = True
            attempts += 1
    
    return mutated_sql

def flip_operators(sql, operator_flips):
    """Flip binary operators in the SQL query."""
    result = sql
    for old_op, new_ops in operator_flips.items():
        if old_op in sql.upper() and random.random() < 0.3:
            # Use word boundaries to avoid partial replacement
            new_op = random.choice(new_ops)
            # Be careful with replacement to avoid breaking syntax
            pattern = rf'(?<!\w)({re.escape(old_op)})(?!\w)'
            result = re.sub(pattern, new_op, result, flags=re.IGNORECASE)
    return result

def transform_boolean_logic(sql):
    """Transform boolean logic expressions."""
    if random.random() > 0.3:
        return sql
        
    # Sample transformations
    transformations = [
        # NOT (A AND B) -> NOT A OR NOT B
        (r'NOT\s*\(\s*([^()]+?)\s+AND\s+([^()]+?)\s*\)', r'NOT (\1) OR NOT (\2)'),
        # NOT (A OR B) -> NOT A AND NOT B
        (r'NOT\s*\(\s*([^()]+?)\s+OR\s+([^()]+?)\s*\)', r'NOT (\1) AND NOT (\2)'),
        # A OR B -> NOT(NOT A AND NOT B)
        (r'([^()]+?)\s+OR\s+([^()]+?)', r'NOT(NOT (\1) AND NOT (\2))'),
    ]
    
    result = sql
    transformation = random.choice(transformations)
    try:
        pattern, replacement = transformation
        # Only apply to WHERE or HAVING clauses to be safer
        where_clause_match = re.search(r'(WHERE|HAVING)\s+(.+?)(?:ORDER BY|GROUP BY|LIMIT|$)', result, re.IGNORECASE | re.DOTALL)
        if where_clause_match:
            where_part = where_clause_match.group(0)
            new_where_part = re.sub(pattern, replacement, where_part, flags=re.IGNORECASE)
            result = result.replace(where_part, new_where_part)
    except Exception:
        pass  # If transformation fails, return original
    return result

def add_redundant_condition(sql):
    """Add redundant WHERE/AND/OR conditions."""
    if random.random() > 0.4:
        return sql
        
    redundant_conds = [
        "1=1", "TRUE", "0=0", "'x'='x'", "NULL IS NULL",
        "EXISTS(SELECT 1)", "2>1", "1<2"
    ]
    
    result = sql
    cond = random.choice(redundant_conds)
    
    # Add to WHERE clause
    if re.search(r'\bWHERE\b', result, re.IGNORECASE):
        result = re.sub(r'\bWHERE\b', f'WHERE {cond} AND ', result, flags=re.IGNORECASE, count=1)
    # Add WHERE if there isn't one but there's FROM
    elif re.search(r'\bFROM\b.*?(?:ORDER BY|GROUP BY|LIMIT|;|$)', result, re.IGNORECASE | re.DOTALL):
        from_clause_end = re.search(r'\bFROM\b.*?(?=ORDER BY|GROUP BY|LIMIT|;|$)', result, re.IGNORECASE | re.DOTALL)
        if from_clause_end:
            pos = from_clause_end.end()
            result = f"{result[:pos]} WHERE {cond}{result[pos:]}"
    
    return result

def nest_in_subquery(sql):
    """Nest the query in a subquery."""
    if random.random() > 0.3 or not sql.upper().startswith('SELECT'):
        return sql
    
    nesting_patterns = [
        f"SELECT * FROM ({sql.rstrip(';')})",
        f"SELECT sub.* FROM ({sql.rstrip(';')}) AS sub",
        f"WITH subquery AS ({sql.rstrip(';')}) SELECT * FROM subquery"
    ]
    
    return random.choice(nesting_patterns)

def convert_query_form(sql):
    """Convert between equivalent query forms."""
    if random.random() > 0.3:
        return sql
        
    # Convert IN to EXISTS or vice versa
    if "IN (SELECT" in sql.upper():
        match = re.search(r'([^\s]+)\s+IN\s+\(SELECT\s+([^\s]+)\s+FROM\s+([^\s]+)(\s+WHERE\s+.+?)?(\))', sql, re.IGNORECASE)
        if match:
            left_expr, select_expr, from_table, where_clause, closing = match.groups()
            where_clause = where_clause or ""
            new_form = f"EXISTS (SELECT 1 FROM {from_table}{where_clause} AND {select_expr} = {left_expr}{closing}"
            return sql.replace(match.group(0), new_form)
    elif "EXISTS (SELECT" in sql.upper():
        match = re.search(r'EXISTS\s+\(SELECT\s+\w+\s+FROM\s+(\w+)(\s+WHERE\s+.+?\s+AND\s+(\w+)\s+=\s+(\w+))?(\))', sql, re.IGNORECASE)
        if match:
            from_table, _, right_expr, left_expr, closing = match.groups()
            if all([right_expr, left_expr]):
                new_form = f"{left_expr} IN (SELECT {right_expr} FROM {from_table}{closing}"
                return sql.replace(match.group(0), new_form)
    
    return sql

def modify_result_columns(sql):
    """Modify the result columns of the query."""
    if random.random() > 0.3 or not sql.upper().startswith('SELECT'):
        return sql
        
    # Replace * with explicit columns or vice versa - now handles table.* properly
    select_star_pattern = r'SELECT\s+(\w+\.)?\*'
    select_match = re.search(select_star_pattern, sql, re.IGNORECASE)
    
    if select_match:
        # Extract table names from FROM clause
        from_match = re.search(r'FROM\s+(\w+)(?:\s+AS\s+\w+)?', sql, re.IGNORECASE)
        if from_match:
            table = from_match.group(1)
            # Replace * with some dummy columns
            cols = [f"{table}.rowid", f"{table}.*, 1 AS constant"]
            replacement = random.choice(cols)
            return re.sub(select_star_pattern, f'SELECT {replacement}', sql, flags=re.IGNORECASE, count=1)
    
    # Add DISTINCT or remove it
    if re.search(r'SELECT\s+DISTINCT', sql, re.IGNORECASE):
        return re.sub(r'SELECT\s+DISTINCT', 'SELECT', sql, flags=re.IGNORECASE, count=1)
    else:
        return re.sub(r'SELECT', 'SELECT DISTINCT', sql, flags=re.IGNORECASE, count=1)

def modify_ordering(sql):
    """Add or modify ORDER BY clause."""
    if random.random() > 0.4:
        return sql
        
    if re.search(r'ORDER BY', sql, re.IGNORECASE):
        # Replace existing ORDER BY
        order_match = re.search(r'ORDER BY\s+(.+?)(?:LIMIT|;|$)', sql, re.IGNORECASE)
        if order_match:
            current_order = order_match.group(1).strip()
            new_direction = "DESC" if "DESC" not in current_order.upper() else "ASC"
            new_order = f"{current_order} {new_direction}"
            return sql.replace(order_match.group(0), f"ORDER BY {new_order}{order_match.group(0)[order_match.end(1):]}") 
    else:
        # Add ORDER BY if not present
        if "SELECT" in sql.upper():
            # Find position to insert ORDER BY (before LIMIT if it exists)
            limit_match = re.search(r'LIMIT\s+\d+', sql, re.IGNORECASE)
            if limit_match:
                pos = limit_match.start()
                return f"{sql[:pos]}ORDER BY 1 {sql[pos:]}"
            else:
                semi_pos = sql.rfind(';')
                if semi_pos >= 0:
                    return f"{sql[:semi_pos]} ORDER BY 1{sql[semi_pos:]}"
                else:
                    return f"{sql} ORDER BY 1"
    
    return sql

def wrap_with_cte(sql):
    """Wrap the query with a CTE."""
    if random.random() > 0.25 or not sql.upper().startswith('SELECT'):
        return sql
        
    if not sql.upper().startswith('WITH '):
        cte_name = f"cte_{random_string(3)}"
        return f"WITH {cte_name} AS ({sql.rstrip(';')}) SELECT * FROM {cte_name};"
    
    return sql

def shuffle_joins(sql):
    """Shuffle the order of JOINs if possible."""
    if random.random() > 0.3:
        return sql
        
    # This is complex and can easily break queries
    # We'll do a simpler version that just changes JOIN types
    join_types = ['JOIN', 'INNER JOIN', 'LEFT JOIN', 'LEFT OUTER JOIN']
    
    result = sql
    for join_type in join_types:
        if join_type in sql.upper():
            new_type = random.choice(join_types)
            # Only replace exact join type with word boundaries
            result = re.sub(rf'\b{re.escape(join_type)}\b', new_type, result, flags=re.IGNORECASE)
            break
    
    return result

def add_case_expressions(sql):
    """Add harmless CASE expressions to the query."""
    if random.random() > 0.2 or not sql.upper().startswith('SELECT'):
        return sql
        
    # Find position after SELECT
    select_match = re.search(r'SELECT\b(?:\s+DISTINCT)?', sql, re.IGNORECASE)
    if select_match:
        pos = select_match.end()
        case_expr = random.choice([
            "CASE WHEN 1=1 THEN 1 ELSE 0 END AS always_true, ",
            "CASE WHEN random()>0.5 THEN 'yes' ELSE 'no' END AS random_choice, ",
            "CASE WHEN NULL IS NULL THEN 'valid' END AS validity_check, "
        ])
        return f"{sql[:pos]} {case_expr}{sql[pos:]}"
    
    return sql

def modify_grouping(sql):
    """Add or modify GROUP BY clause."""
    if random.random() > 0.2:
        return sql
        
    # Only add GROUP BY if we have aggregates
    has_aggregates = any(f in sql.upper() for f in ['COUNT(', 'SUM(', 'AVG(', 'MIN(', 'MAX('])
    
    if has_aggregates and not re.search(r'GROUP BY', sql, re.IGNORECASE):
        # Extract a column for GROUP BY
        from_match = re.search(r'FROM\s+(\w+)(?:\s+AS\s+\w+)?', sql, re.IGNORECASE)
        if from_match:
            table = from_match.group(1)
            
            # Find position to insert GROUP BY (before ORDER BY/LIMIT if they exist)
            insert_pos = len(sql)
            for clause in ['ORDER BY', 'LIMIT']:
                clause_match = re.search(rf'{clause}\b', sql, re.IGNORECASE)
                if clause_match and clause_match.start() < insert_pos:
                    insert_pos = clause_match.start()
            
            if insert_pos < len(sql):
                # Add GROUP BY with the table's first column as a placeholder
                return f"{sql[:insert_pos]}GROUP BY {table}.rowid {sql[insert_pos:]}"
    
    return sql

def mutate_input_values(sql: str) -> str:
    """
    Change literal input values in a SQL statement while preserving syntax.
    """
    if random.random() > 0.4:
        return sql
        
    modified_sql = sql
    
    # Find and replace numeric literals
    modified_sql = re.sub(r'(\s|^|\()(\d+)(\s|$|\)|,)', lambda m: f"{m.group(1)}{modify_number(m.group(2))}{m.group(3)}", modified_sql)
    
    # Find and replace string literals (in single quotes)
    modified_sql = re.sub(r"'([^']*)'", lambda m: f"'{modify_string(m.group(1))}'", modified_sql)
    
    # Find and replace date/time literals
    date_pattern = r"'(\d{4}-\d{2}-\d{2}(?:\s\d{2}:\d{2}:\d{2})?)'(?!\s*[+*/-])"
    modified_sql = re.sub(date_pattern, lambda m: f"'{modify_date(m.group(1))}'", modified_sql)
    
    # Find and replace NULL values
    if random.random() < 0.3 and "NULL" in modified_sql:
        modified_sql = re.sub(r'\bNULL\b(?!\s*IS)', random.choice(['NULL', "''", '0']), modified_sql)
    
    # Find and replace boolean literals
    if random.random() < 0.3:
        modified_sql = re.sub(r'\bTRUE\b', random.choice(['TRUE', '1', '(1=1)']), modified_sql, flags=re.IGNORECASE)
        modified_sql = re.sub(r'\bFALSE\b', random.choice(['FALSE', '0', '(1=0)']), modified_sql, flags=re.IGNORECASE)
    
    # Replace LIMIT values
    modified_sql = re.sub(r'\bLIMIT\s+(\d+)', lambda m: f"LIMIT {modify_limit(m.group(1))}", modified_sql, flags=re.IGNORECASE)
    
    # Replace parameters in WHERE clauses with boundary values
    if random.random() < 0.3 and "WHERE" in modified_sql.upper():
        where_clause = re.search(r'WHERE\s+(.+?)(?:GROUP BY|ORDER BY|LIMIT|;|$)', modified_sql, re.IGNORECASE | re.DOTALL)
        if where_clause:
            clause_text = where_clause.group(1)
            # Fixed condition pattern to properly match conditions without capturing keywords
            condition_pattern = r'(\w+)\s*([=<>!]+)\s*([^;()]+?)(?:\s+AND|\s+OR|\s+GROUP|\s+ORDER|\s+LIMIT|;|$)'
            matches = list(re.finditer(condition_pattern, clause_text))
            if matches:
                match = random.choice(matches)
                col, op, val = match.groups()
                new_val = generate_boundary_value(val.strip())
                new_condition = f"{col} {op} {new_val}"
                modified_sql = modified_sql.replace(match.group(0), new_condition + match.group(0)[match.end(3):])
    
    return modified_sql

def modify_number(number_str: str) -> str:
    """
    Modify a numeric literal while keeping it a valid number.
    """
    number = int(number_str)
    mutation_type = random.randint(0, 5)
    
    if mutation_type == 0:
        # Add or subtract a small amount
        return str(number + random.randint(-10, 10))
    elif mutation_type == 1:
        # Multiply or divide by small factor
        return str(int(number * random.choice([0.5, 2, 3, 0.1, 10])))
    elif mutation_type == 2:
        # Negate if not a date component or likely ID
        if number > 100 or number < 0:
            return str(-number)
        return number_str
    elif mutation_type == 3:
        # Replace with boundary values
        return random.choice(['0', '1', '-1', '999999', '-999999'])
    elif mutation_type == 4:
        # Replace with extreme value
        return str(random.randint(1000000, 9999999) * (1 if random.random() < 0.5 else -1))
    else:
        # Keep the same
        return number_str

def modify_string(string_value: str) -> str:
    """
    Modify a string literal while keeping it a valid string.
    """
    mutation_type = random.randint(0, 5)
    
    if mutation_type == 0:
        # Empty string
        return ""
    elif mutation_type == 1:
        # Add random characters to the end
        return string_value + random_string(random.randint(1, 5))
    elif mutation_type == 2:
        # Completely new random string
        return random_string(random.randint(1, 10))
    elif mutation_type == 3:
        # SQL special characters
        return random.choice(['%', '_', '%' + string_value + '%', '_' + string_value, string_value + '_'])
    elif mutation_type == 4:
        # Casing change
        return random.choice([string_value.upper(), string_value.lower(), string_value.capitalize()])
    else:
        # Keep the same
        return string_value
        
def modify_limit(limit_str: str) -> str:
    """
    Modify a LIMIT value in a way that's usually valid.
    """
    limit = int(limit_str)
    mutation_type = random.randint(0, 3)
    
    if mutation_type == 0:
        # Increase slightly
        return str(limit + random.randint(1, 5))
    elif mutation_type == 1:
        # Decrease slightly but keep positive
        return str(max(1, limit - random.randint(1, 3)))
    elif mutation_type == 2:
        # Much larger value
        return str(limit * random.randint(5, 20))
    else:
        # Fixed small values
        return random.choice(['1', '2', '5', '10', '100'])

def modify_date(date_str: str) -> str:
    """
    Modify a date literal while keeping it a valid date.
    """
    mutation_type = random.randint(0, 3)
    
    # Basic pattern checks
    is_datetime = len(date_str) > 10
    
    if mutation_type == 0:
        # Boundary dates
        return random.choice([
            '2000-01-01', '1970-01-01', '2038-01-19',
            '9999-12-31', '0000-00-00', 'now()'
        ])
    elif mutation_type == 1:
        # Slightly modify year
        year_pattern = r'(\d{4})-(\d{2})-(\d{2})'
        match = re.match(year_pattern, date_str)
        if match:
            year, month, day = match.groups()
            new_year = str(int(year) + random.randint(-5, 5))
            new_date = f"{new_year}-{month}-{day}"
            if is_datetime and len(date_str) > 16:
                new_date += date_str[10:]
            return new_date
    elif mutation_type == 2:
        # Slightly modify day
        if is_datetime:
            return date_str  # Don't modify datetime for this case
        year_pattern = r'(\d{4})-(\d{2})-(\d{2})'
        match = re.match(year_pattern, date_str)
        if match:
            year, month, day = match.groups()
            new_day = str(min(28, int(day) + random.randint(-5, 5))).zfill(2)
            return f"{year}-{month}-{new_day}"
    
    # If no mutation applied or failed, return original
    return date_str

def generate_boundary_value(value_str: str) -> str:
    """
    Generate boundary or edge case values based on the input type.
    """
    value_str = value_str.strip()
    
    # Check if it's a numeric value
    if re.match(r'^-?\d+(\.\d+)?$', value_str):
        return random.choice([
            '0', '1', '-1', 
            str(int(float(value_str)) + 1),
            str(int(float(value_str)) - 1),
            'NULL'
        ])
    
    # Check if it's a string value (quoted)
    elif re.match(r"^'.*'$", value_str) or re.match(r'^".*"$', value_str):
        quote = value_str[0]
        return random.choice([
            f"{quote}{quote}",  # Empty string
            f"{quote}%{quote}",  # Wildcard
            f"{quote}{quote} OR 1=1",  # SQL injection attempt (safe for testing)
            'NULL'
        ])
    
    # Otherwise return some common test values
    return random.choice(['NULL', '1', "'test'", '0'])

def is_valid_sql(sql):
    """
    Check if the SQL statement is likely valid.
    This is a basic check and won't catch all issues.
    """
    try:
        # Check for basic syntax errors
        if not sql.strip():
            return False
            
        # Check for basic query structure
        if sql.upper().startswith('SELECT'):
            if 'FROM' not in sql.upper() and '*' not in sql and 'SELECT 1' not in sql.upper():
                return False
                
        # Check for balanced parentheses
        if sql.count('(') != sql.count(')'):
            return False
            
        # Check for proper semicolon placement
        if ';' in sql and not sql.rstrip().endswith(';') and ';' != sql.rstrip()[-1]:
            return False
            
        # Check for common SQL syntax patterns
        if sql.upper().startswith('SELECT'):
            # SELECT without columns
            if re.match(r'SELECT\s+FROM', sql, re.IGNORECASE):
                return False
                
        # JOIN without ON or USING
        if re.search(r'\bJOIN\b.*?(?!\bON\b|\bUSING\b)(?:\bWHERE\b|\bGROUP\b|\bORDER\b|\bLIMIT\b|;|$)', sql, re.IGNORECASE | re.DOTALL):
            # Simple check for JOIN without ON, not perfect but catches obvious issues
            if not re.search(r'\bJOIN\b.*?(\bON\b|\bUSING\b)', sql, re.IGNORECASE | re.DOTALL):
                return False
        
        return True
    except Exception as e:
        # More specific exception handling
        # print(f"SQL validation error: {e}")
        return False

def random_string(length=5):
    """Generate a random string of specified length."""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))