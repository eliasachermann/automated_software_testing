#!/usr/bin/env python3

import os
import sys
import subprocess
import glob
from pathlib import Path

def process_query(query_dir):
    """Process a single query directory."""
    query_name = os.path.basename(query_dir)
    print(f"Processing query: {query_name}")
    print("=" * 50)
    
    # Look for specific files
    sql_file = os.path.join(query_dir, "original_test.sql")
    oracle_file = os.path.join(query_dir, "oracle.txt")
    test_script = "tester.py"  # Use tester.py as specified
    
    # Check if SQL file exists
    if not os.path.exists(sql_file):
        print(f"Warning: original_test.sql not found in {query_dir}")
        return False
    
    # Check if oracle file exists (optional check)
    if not os.path.exists(oracle_file):
        print(f"Warning: oracle.txt not found in {query_dir}")
        # Continue anyway since oracle might be optional
    
    print(f"SQL file: {sql_file}")
    print(f"Test script: {test_script}")
    print(f"Oracle file: {oracle_file}")
    print()
    
    # Run reducer
    print("Running reducer...")
    try:
        result = subprocess.run([
            sys.executable, "reducer.py",
            "--query", sql_file,
            "--test", test_script,
            "--oracle", oracle_file
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"SUCCESS: Query {query_name} reduced successfully")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"FAILED: Query {query_name} reduction failed")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT: Query {query_name} reduction timed out")
        return False
    except Exception as e:
        print(f"ERROR: Exception while processing {query_name}: {e}")
        return False
    finally:
        print()
        print("=" * 70)
        print()

def main():
    base_dir = Path(__file__).parent
    queries_dir = base_dir / "queries"
    
    if not queries_dir.exists():
        print(f"Error: Queries directory '{queries_dir}' not found")
        sys.exit(1)
    
    print("Starting batch reduction process...")
    print(f"Queries directory: {queries_dir}")
    print()
    
    # Statistics
    total_queries = 0
    successful_reductions = 0
    failed_reductions = 0
    
    # Process each query directory
    for query_dir in sorted(queries_dir.iterdir()):
        if query_dir.is_dir():
            total_queries += 1
            if process_query(query_dir):
                successful_reductions += 1
            else:
                failed_reductions += 1
    
    # Print summary
    print("SUMMARY")
    print("=" * 20)
    print(f"Total queries processed: {total_queries}")
    print(f"Successful reductions: {successful_reductions}")
    print(f"Failed reductions: {failed_reductions}")
    
    if total_queries == 0:
        print(f"No query directories found in {queries_dir}")
        sys.exit(1)

if __name__ == "__main__":
    main()