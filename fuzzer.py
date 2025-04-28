from sql_generator import generate_query
from bug_detector import BugDetector
from bug_logger import BugLogger
from coverage import clean_gcov_data, get_coverage

def main():
    measure_coverage = False
    test_path = "/usr/bin/sqlite3-3.26.0"
    # test_path = "/usr/bin/sqlite3-3.39.4"
    oracle_path = "/usr/bin/sqlite3-3.49.1"
    detector = BugDetector(test_path, oracle_path)
    clean_gcov_data()

    for i in range(1000):
        query = generate_query()
        detector.detect_bug(query)
        if i % 100 == 0 and measure_coverage:
            get_coverage(i)
        
    
    #detector.close()  # forcibly close sqlite3 binary (flush .gcda)
    
if __name__ == "__main__":
    main()
