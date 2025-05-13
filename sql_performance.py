from sql_statement_generator import generate_test_case as gen_sql
import time
from query_stats import SQLStatistics
import tempfile
import subprocess
import sys
import os


def measure_performance():
    start_time = time.time()

    for _ in range(10000):
        sql = gen_sql()

    endtime = time.time()
    duration = endtime - start_time
    print(f"Time taken to generate 10000 SQL statements: {duration:.2f} seconds")

def get_statistics():
    stats = SQLStatistics()
    for _ in range(10000):
        sql = gen_sql()
        try: 
            with(tempfile.NamedTemporaryFile() as tmpdb):
                cmd = ["/usr/bin/sqlite3-3.26.0", tmpdb.name]
                result_old = subprocess.run(
                    cmd, input=sql.encode(), capture_output=True, timeout=10
                )
                err_old = result_old.stderr.decode(errors="replace")
                if(err_old != ""):
                    stats.analyze_query(sql, False)
                else:
                    stats.analyze_query(sql, True)
        except Exception as e:
            print("\n❗ Got exception")
            stats.analyze_query(sql, False)

    stats.print_statistics()
    stats.save_statistics()

#make main
if __name__ == "__main__":
    # measure_performance()
    get_statistics()
