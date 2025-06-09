import os
import time
import subprocess
import csv
from sqlglot import Tokenizer

def count_tokens(sql_query):
    tokens = Tokenizer().tokenize(sql_query)
    return len(tokens)

BASE_DIR = os.getcwd()
REDUCER_IMAGE = "reduce-env"
TEST_CASES = [f"query{i}" for i in range(1, 21)]
CSV_PATH = os.path.join(BASE_DIR, "reduction_benchmark.csv")

# Prepare CSV file with headers
with open(CSV_PATH, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=[
        "Test Case", "Original Tokens", "Reduced Tokens", "Reduction (%)", "Time (s)"
    ])
    writer.writeheader()

# Iterate over test cases
for test in TEST_CASES:
    print(f"\n▶ Benchmarking {test}...")

    original_query_path = os.path.join(BASE_DIR, f"test-scripts/{test}/original_test.sql")
    reduced_query_path = os.path.join(BASE_DIR, f"query.sql")
    test_script_path = f"/app/queries/{test}/test-script.sh"

    try:
        with open(original_query_path, "r") as f:
            original_query = f.read()
            original_tokens = count_tokens(original_query)
    except FileNotFoundError:
        print(f"Skipping {test}: original query file not found.")
        continue

    try:
        start_time = time.perf_counter()
        subprocess.run([
            "sudo", "docker", "run", "--rm",
            "-v", f"{BASE_DIR}:/app",
            REDUCER_IMAGE, "reducer",
            "--query", f"/app/test-scripts/{test}/original_test.sql",
            "--test", test_script_path
        ], check=True)
        end_time = time.perf_counter()
        elapsed = round(end_time - start_time, 2)
    except subprocess.CalledProcessError as e:
        print(f"❌ Reducer failed for {test}, skipping. Exit code {e.returncode}")
        row = {
            "Test Case": test,
            "Original Tokens": original_tokens,
            "Reduced Tokens": "N/A",
            "Reduction (%)": "N/A",
            "Time (s)": "ERROR"
        }
        with open(CSV_PATH, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=row.keys())
            writer.writerow(row)
        continue

    try:
        with open(reduced_query_path, "r") as f:
            reduced_query = f.read()
            reduced_tokens = count_tokens(reduced_query)
    except FileNotFoundError:
        print(f"Skipping {test}: reduced file not found after reducer ran.")
        continue

    reduction_percent = round((1 - reduced_tokens / original_tokens) * 100, 2)

    row = {
        "Test Case": test,
        "Original Tokens": original_tokens,
        "Reduced Tokens": reduced_tokens,
        "Reduction (%)": reduction_percent,
        "Time (s)": elapsed
    }

    with open(CSV_PATH, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=row.keys())
        writer.writerow(row)