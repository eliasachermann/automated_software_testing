import subprocess
import glob
import os

SQLITE_BUILD_DIR = '/tmp/sqlite-autoconf-3260000'  # Update to the actual build directory

def clean_gcov_data():
    gcda_files = glob.glob('/tmp/sqlite-autoconf-3260000/*.gcda')
    for file in gcda_files:
        os.remove(file)

def get_coverage(iteration):
    """Run gcov ONLY on the database engine .gcda file."""
    gcda_file = os.path.join(SQLITE_BUILD_DIR, "sqlite3-sqlite3.gcda")
    
    if os.path.exists(gcda_file):
        # Run gcov and capture its output
        result = subprocess.run(
            ["gcov", gcda_file], 
            cwd=os.path.dirname(gcda_file), 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True  # Ensures the output is returned as a string
        )
        
        # Extract the relevant line (Lines executed:...)
        output_lines = result.stdout.splitlines()
        for line in output_lines:
            if "Lines executed:" in line:
                print(line + " after " + str(iteration) + " iterations")  # Print only the relevant line
                break

    else:
        print("Lines executed:0%")