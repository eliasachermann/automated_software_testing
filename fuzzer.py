from sql_generator import generate_query
from bug_detector import BugDetector
from bug_logger import BugLogger
from coverage import clean_gcov_data, get_coverage
from query_stats import SQLStatistics

def main():
    measure_coverage = True  # only works for 3.26.0
    test_path = "/usr/bin/sqlite3-3.26.0"
    # test_path = "/usr/bin/sqlite3-3.39.4"
    oracle_path = "/usr/bin/sqlite3-3.49.1"

    detector = BugDetector(test_path, oracle_path)
    stats = SQLStatistics()
    clean_gcov_data()
    tables_info = {}

    for i in range(500):
        query, tables_info = generate_query(tables_info)
        success = detector.detect_bug(query)
        stats.analyze_query(query, success)
        if i % 100 == 0 and measure_coverage:
            get_coverage(i)

    stats.save_statistics()
    
    #detector.close()  # forcibly close sqlite3 binary (flush .gcda)
    
if __name__ == "__main__":
    main()
