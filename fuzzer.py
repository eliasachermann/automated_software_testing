from sql_generator import generate_query
from bug_detector import BugDetector
from bug_logger import BugLogger
from coverage import clean_gcov_data, collect_coverage, calculate_coverage

def main():
    test_path = "/tmp/sqlite-autoconf-3260000/sqlite3"
    # test_path = "/usr/bin/sqlite3-3.39.4"
    oracle_path = "/tmp/sqlite-autoconf-3490100/sqlite3"

    clean_gcov_data()
    
    detector = BugDetector(test_path, oracle_path)
    logger = BugLogger()
    
    for i in range(100):
        detector.close()  # forcibly close sqlite3 binary (flush .gcda)
        collect_coverage()
        coverage = calculate_coverage()
        print(f"[+] {i+1} queries generated - Current coverage: {coverage:.2f}%")

        # Recreate detector (new sqlite3 process)
        detector = BugDetector(test_path, oracle_path)

if __name__ == "__main__":
    main()
