import argparse
import json
import multiprocessing as mp
import time
import tempfile
import subprocess
from sql_statement_generator import generate_test_case as gen_sql
import os
from coverage import get_coverage, clean_gcov_data
from sql_statement_mutator import mutate_sql_statement
import random


def check_muatation(out_old, err_old, out_new, err_new):
    if out_old != out_new:
        return True, "Output Mutation"
    if err_old != "" and err_new == "":
        return True, "Only one Error Mutation"
    return False, "No Difference"

def compare_results(out_old, err_old, out_new, err_new):
    # return True, "Test"
    if out_old != out_new:
        return True, "Output"
    if err_old != "" and err_new == "":
        return True, "Only one Error"
    if err_old or err_new:
        return True, "Error"
    return False, "No Difference"


def save_difference(
    sql, sql_old, sql_new, out_old, err_old, out_new, err_new, diff_type
):
    """Save a difference to a log file."""
    timestamp = time.time()
    formatted_timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime(timestamp))
    ms = int((timestamp - int(timestamp)) * 1000)
    timestamp = f"{formatted_timestamp}_{ms:03d}"
    pid = os.getpid()
    timestamp = f"{timestamp}_{pid}"
    log_dir = "fuzz_logs"

    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    filename = f"{log_dir}/diff_{diff_type}_{timestamp}.log"
    with open(filename, "w") as f:
        f.write(f"SQL:\n{sql}\n\n")
        f.write(f"--- v3.26.0 ---\nOUT:\n{out_old}\nERR:\n{err_old}\n\n")
        f.write(f"--- v3.49.1 ---\nOUT:\n{out_new}\nERR:\n{err_new}\n")

    return filename


def run_tests(old_sqlite, new_sqlite):
    sql = gen_sql()

    try:
        with (
            tempfile.NamedTemporaryFile() as tmpdb,
            tempfile.NamedTemporaryFile() as tmpdb2,
        ):
            # Run the old SQLite version
            cmd = [old_sqlite, tmpdb.name]
            result_old = subprocess.run(
                cmd, input=sql.encode(), capture_output=True, timeout=15
            )

            # Run the new SQLite version
            cmd = [new_sqlite, tmpdb2.name]
            result_new = subprocess.run(
                cmd, input=sql.encode(), capture_output=True, timeout=15
            )

            # Add error handling to prevent UTF-8 decode errors
            out_old = result_old.stdout.decode(errors="replace")
            err_old = result_old.stderr.decode(errors="replace")
            out_new = result_new.stdout.decode(errors="replace")
            err_new = result_new.stderr.decode(errors="replace")

            result, diff_type = compare_results(out_old, err_old, out_new, err_new)

            if result:
                filename = save_difference(
                    sql,
                    old_sqlite,
                    new_sqlite,
                    out_old,
                    err_old,
                    out_new,
                    err_new,
                    diff_type,
                )

                print(f"\n❗ Difference found! Type: {diff_type}, saved to {filename}")
                return {
                    "sql": sql,
                    "old": (out_old, err_old),
                    "new": (out_new, err_new),
                    "type": diff_type,
                    "file": filename,
                }

    except Exception as e:
        print("\n❗ Got exception")
        filename = save_difference(
            sql, old_sqlite, new_sqlite, e, "", "", "", "Exception"
        )
        print(f"❗ Exception: {e}")
        return {
            "sql": sql,
        }
    
    # if random.random() < 0.1:
    #     sql = mutate_sql_statement(sql)
    #     try:
    #         with (
    #             tempfile.NamedTemporaryFile() as tmpdb,
    #             tempfile.NamedTemporaryFile() as tmpdb2,
    #         ):
    #             # Run the old SQLite version
    #             cmd = [old_sqlite, tmpdb.name]
    #             result_old = subprocess.run(
    #                 cmd, input=sql.encode(), capture_output=True, timeout=5
    #             )

    #             # Run the new SQLite version
    #             cmd = [new_sqlite, tmpdb2.name]
    #             result_new = subprocess.run(
    #                 cmd, input=sql.encode(), capture_output=True, timeout=5
    #             )

    #             # Add error handling to prevent UTF-8 decode errors
    #             out_old = result_old.stdout.decode(errors="replace")
    #             err_old = result_old.stderr.decode(errors="replace")
    #             out_new = result_new.stdout.decode(errors="replace")
    #             err_new = result_new.stderr.decode(errors="replace")

    #             result, diff_type = check_muatation(out_old, err_old, out_new, err_new)

    #             if result:
    #                 filename = save_difference(
    #                     sql,
    #                     old_sqlite,
    #                     new_sqlite,
    #                     out_old,
    #                     err_old,
    #                     out_new,
    #                     err_new,
    #                     diff_type,
    #                 )

    #                 print(f"\n❗ Difference found! Type: {diff_type}, saved to {filename}")
    #                 return {
    #                     "sql": sql,
    #                     "old": (out_old, err_old),
    #                     "new": (out_new, err_new),
    #                     "type": diff_type,
    #                     "file": filename,
    #                 }

    #     except Exception as e:
    #         return


def run_parallel_tests(args):
    """Run tests in parallel."""
    print(f"Running {int(args.iterations)} tests using {args.processes} processes")
    print(f"Testing {args.old_sqlite} vs {args.new_sqlite}")

    start_time = time.time()

    with mp.Pool(processes=args.processes) as pool:
        results = pool.starmap(
            run_tests,
            [(args.old_sqlite, args.new_sqlite) for i in range(args.iterations)],
        )

    # Filter out None results
    differences = [r for r in results if r]

    end_time = time.time()
    duration = end_time - start_time

    print(f"\nCompleted {args.iterations} tests in {duration:.2f} seconds")
    print(f"Found {len(differences)} differences")
    return differences


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="SQLite Differential Fuzzer")
    parser.add_argument(
        "--iterations", type=int, default=10000, help="Number of test iterations"
    )
    parser.add_argument(
        "--processes", type=int, default=16, help="Number of parallel processes"
    )
    parser.add_argument(
        "--old-sqlite",
        default="/usr/bin/sqlite3-3.26.0",
        help="Path to old SQLite binary",
    )
    parser.add_argument(
        "--new-sqlite",
        default="/usr/bin/sqlite3-3.49.1",
        help="Path to new SQLite binary",
    )
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_args()

    clean_gcov_data()
    differences = run_parallel_tests(args)
    get_coverage(args.iterations)

    if not differences:
        print("No differences found!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        get_coverage(-1)
        print("\nFuzzing stopped by user")
