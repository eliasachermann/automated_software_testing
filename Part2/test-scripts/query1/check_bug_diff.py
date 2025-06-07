#!/usr/bin/env python3
import os
import subprocess
import sys

def run_sqlite(sqlite_binary, db_path, query):
    try:
        result = subprocess.run(
            [sqlite_binary, db_path],
            input=query.encode(),
            capture_output=True,
            timeout=5
        )
        return result.stdout.decode(), result.stderr.decode(), result.returncode
    except Exception as e:
        return "", str(e), 1

# Step 1: Determine query location
test_case_location = os.environ.get('TEST_CASE_LOCATION')
if test_case_location:
    print(f"TEST_CASE_LOCATION is set to: {test_case_location}")
else:
    print("TEST_CASE_LOCATION environment variable is not set")
    base_path = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
    test_case_location = os.path.join(base_path, "test-scripts/query1/query.sql")

sqlite_v1 = "/usr/bin/sqlite3-3.26.0"
sqlite_v2 = "/usr/bin/sqlite3-3.39.4"

try:
    with open(test_case_location, "r") as f:
        sql_query = f.read()
except FileNotFoundError:
    print(f"Error: Query file not found at {test_case_location}", file=sys.stderr)
    sys.exit(1)

db_file = ":memory:"

out1, err1, code1 = run_sqlite(sqlite_v1, db_file, sql_query)
print("=== Running on sqlite_v1 ===")
print("STDOUT:", out1)
print("STDERR:", err1)
print("Exit code:", code1)


out2, err2, code2 = run_sqlite(sqlite_v2, db_file, sql_query)
print("\n=== Running on sqlite_v2 ===")
print("STDOUT:", out2)
print("STDERR:", err2)
print("Exit code:", code2)

bug_detected = False

error_keywords = [
    "syntax error",
    "no such table",
    "no such column",
    "no such function",
    "no such module",
    "already exists",
    "UNIQUE constraint failed",
    "NOT NULL constraint failed",
    "CHECK constraint failed",
    "FOREIGN KEY constraint failed",
    "database is locked",
    "values for", # ex: 3 values for 2 columns
    "incomplete input",
    "database disk image is malformed",
    "datatype mismatch",
    "integer overflow",
    "string or blob too big",
    "misuse of",
    "file is encrypted",
    "row value misused",
    "cannot start a transaction",
    "cannot start a transaction within a transaction",
    "cannot commit",
    "wrong number of arguments",
    "attempt to write a readonly database",
]

# both work
if(code1==0 and code2==0):
    if (out1 == out2):
        bug_detected = False
    # different output
    else:
        bug_detected = True
# 1 works and other doesn't
elif (code1 != code2):        
    bug_detected = True
# both don't work
else:
    def extract_errors(stderr, error_keywords):
        stderr_lower = stderr.lower()
        return [keyword for keyword in error_keywords if keyword in stderr_lower]

    errors_v1 = extract_errors(err1, error_keywords)
    errors_v2 = extract_errors(err2, error_keywords)

    # Bug still occurs (only in version 1)
    if errors_v1 and not errors_v2:
        bug_detected = True
    # Bug still occurs (only in version 2)
    elif not errors_v1 and errors_v2:
        bug_detected = True
    elif errors_v1 and errors_v2:
        # Both versions have the same error
        if set(errors_v1) == set(errors_v2):
            bug_detected = False
        # Bug still occurs (different errors)
        else:
            bug_detected = True
    # No bug in either version
    else:
        bug_detected = False




# Step 6: Exit accordingly
if bug_detected:
    print("still a bug")
    sys.exit(0)  # Bug still happens
else:
    print("bug gone")
    sys.exit(1)  # Bug is gone