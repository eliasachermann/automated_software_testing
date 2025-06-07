from sqlglot import parse, parse_one
from sqlglot.errors import ParseError
import argparse
import subprocess
import sys
import tempfile
import os

def reduce_sql_query(sql_query: str, oracle: str, test_script: str) -> str:
    """Apply delta debugging to reduce the SQL query while preserving the bug."""
    
    # Parse the original query
    try:
        tree = parse_one(sql_query, dialect="sqlite", error_level="ignore")
    except Exception as e:
        print(f"Failed to parse query: {e}")
        return sql_query
    
    # First, verify the original query triggers the bug
    if not test_query(sql_query, test_script, oracle):
        print("Original query doesn't trigger the bug!")
        return sql_query
    
    def delta_debug_ast(node):
        """Recursively apply delta debugging to AST nodes."""
        if not hasattr(node, 'args') or not node.args:
            return node
        
        # Get all child nodes that can be removed
        removable_children = []
        for key, value in node.args.items():
            if value is not None:
                if isinstance(value, list) and len(value) > 1:
                    # For lists with multiple elements, try removing subsets
                    removable_children.append((key, value))
                elif not isinstance(value, (str, int, float, bool)):
                    # For single complex nodes, try removing them
                    removable_children.append((key, [value]))
        
        # Apply delta debugging: try removing half of the children at a time
        for key, children in removable_children:
            if len(children) <= 1:
                continue
                
            # Try removing the first half
            mid = len(children) // 2
            first_half = children[:mid]
            second_half = children[mid:]
            
            # Test removing first half
            modified_node = node.copy()
            if len(second_half) > 0:
                modified_node.args[key] = second_half
            else:
                modified_node.args[key] = None
            
            test_sql = modified_node.sql(dialect="sqlite")
            if test_query(test_sql, test_script, oracle):
                print(f"Successfully removed first half of {key}")
                node = modified_node
                continue
            
            # Test removing second half
            modified_node = node.copy()
            modified_node.args[key] = first_half
            
            test_sql = modified_node.sql(dialect="sqlite")
            if test_query(test_sql, test_script, oracle):
                print(f"Successfully removed second half of {key}")
                node = modified_node
                continue
        
        # Recursively process remaining children
        for key, value in node.args.items():
            if value is not None:
                if isinstance(value, list):
                    node.args[key] = [delta_debug_ast(child) for child in value 
                                    if hasattr(child, 'args')]
                elif hasattr(value, 'args'):
                    node.args[key] = delta_debug_ast(value)
        
        return node
    
    # Apply delta debugging to the AST
    reduced_tree = delta_debug_ast(tree)
    
    # Convert back to SQL string
    try:
        reduced_sql = reduced_tree.sql(dialect="sqlite")
        
        # Final verification
        if test_query(reduced_sql, test_script, oracle):
            return reduced_sql
        else:
            print("Warning: Reduced query doesn't trigger the bug, returning original")
            return sql_query
            
    except Exception as e:
        print(f"Error converting reduced AST to SQL: {e}")
        return sql_query


    

def test_query(sql_query: str, test_script: str, oracle: str) -> bool:
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as f:
            f.write(sql_query)
            query_file = f.name
        
        if test_script.endswith('.py'):
            print("Running test script as Python script")
            result = subprocess.run(['python3', test_script, '--query', query_file, '--oracle', oracle], 
                                  text=True, 
                                  timeout=30)
        else:
            result = subprocess.run([test_script, '--query', query_file, '--oracle', oracle], 
                                  text=True, 
                                  timeout=30)
        
        # Clean up temporary file
        os.unlink(query_file)
        
        # Return True if test script exits with code 0 (bug still present)
        return result.returncode == 0
        
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
    parser.add_argument("--oracle", required=True)
    
    args = parser.parse_args()

    try:
        with open(args.query, 'r') as f:
            sql_query = f.read().strip()
    except Exception as e:
        print(f"Error reading query file: {e}")
        sys.exit(1)

    try:
        with open(args.oracle, 'r') as f:
            oracle = f.read().strip()
    except Exception as e:
        print(f"Error reading oracle file: {e}")
        sys.exit(1)
    
    print(f"Original query length: {len(sql_query)} characters")
    reduced_query = reduce_sql_query(sql_query, oracle, args.test)
    print(f"Reduced query length: {len(reduced_query)} characters")

    print(reduced_query)