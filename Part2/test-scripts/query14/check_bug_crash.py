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
    test_case_location = os.path.join(base_path, "test-scripts/query6/query.sql")

sqlite_v1 = "/usr/bin/sqlite3-3.26.0"
sqlite_v2 = "/usr/bin/sqlite3-3.39.4"

try:
    with open(test_case_location, "r") as f:
        sql_query = f.read()
except FileNotFoundError:
    print(f"Error: Query file not found at {test_case_location}", file=sys.stderr)
    sys.exit(1)

db_file = ":memory:"
bug_detected = False

out1, err1, code1 = run_sqlite(sqlite_v1, db_file, sql_query)
print("=== Running on 3.26.0 ===")
print("STDOUT:", out1)
print("STDERR:", err1)
print("Exit code:", code1)
if (code1 == 1 and "database disk image is malformed" in err1):
    bug_detected = True

if bug_detected:
    print("still a bug")
    sys.exit(0)  # Bug still happens
else:
    print("bug gone")
    sys.exit(1)  # Bug is gone