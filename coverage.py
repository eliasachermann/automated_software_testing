import subprocess
import glob
import os

SQLITE_BUILD_DIR = '/tmp/sqlite-autoconf-3260000'  # Update to the actual build directory

def clean_gcov_data():
    # Ensure you're removing previous .gcda files here.
    gcda_files = glob.glob('/path/to/gcov/*.gcda')
    for file in gcda_files:
        os.remove(file)

def collect_coverage():
    """Run gcov ONLY on the database engine .gcda file."""
    gcda_file = os.path.join(SQLITE_BUILD_DIR, "sqlite3-sqlite3.gcda")
    if os.path.exists(gcda_file):
        subprocess.run(["gcov", gcda_file], cwd=os.path.dirname(gcda_file)) # stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))


def calculate_coverage():
    """Calculate code coverage ONLY from sqlite3.c related .gcov file."""
    gcov_file = os.path.join(SQLITE_BUILD_DIR, "sqlite3.c.gcov")
    total = 0
    covered = 0
    if not os.path.exists(gcov_file):
        print("file not found")
        return 0.0

    with open(gcov_file, 'r') as f:
        for line in f:
            if line.startswith('    -:'):
                continue  # No code on this line
            if line.startswith('#####'):
                total += 1  # Code line, not executed
            elif ':' in line:
                covered += 1
                total += 1
    print(covered)
    print(total)
    if total == 0:
        return 0.0
    return (covered / total) * 100
