from __old.sql_generator import generate_query
from bug_detector import BugDetector
from bug_logger import BugLogger
from coverage import clean_gcov_data, get_coverage
from __old.query_stats import SQLStatistics
from time import sleep
from fuzzer import main as fuzz

def main():
    measure_coverage = True  # only works for 3.26.0
    # test_path = "/usr/bin/sqlite3-3.26.0"
    # # test_path = "/usr/bin/sqlite3-3.39.4"
    # oracle_path = "/usr/bin/sqlite3-3.49.1"

    # detector = BugDetector(test_path, oracle_path)
    # stats = SQLStatistics()
    # clean_gcov_data()

    fuzz()

    get_coverage(10000)

    # stats.save_statistics()
    
    #detector.close()  # forcibly close sqlite3 binary (flush .gcda)
    
if __name__ == "__main__":
    main()
