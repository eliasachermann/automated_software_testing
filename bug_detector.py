from db_runner import DatabaseRunner
from bug_logger import BugLogger

class BugDetector:
    def __init__(self, buggy_sqlite_path, oracle_sqlite_path):
        """
        Initialize the bug detector with paths to buggy and oracle sqlite binaries.
        """
        self.buggy_runner = DatabaseRunner(buggy_sqlite_path)
        self.oracle_runner = DatabaseRunner(oracle_sqlite_path)
        self.logger = BugLogger()

    def is_bug(self, buggy_success, buggy_output, buggy_error,
                     oracle_success, oracle_output, oracle_error):
        
        # Case 1: Both succeed, but outputs differ → Bug
        if buggy_success and oracle_success:
            return buggy_output.strip() != oracle_output.strip()

        # Case 2: One succeeds, one fails → Bug
        if buggy_success != oracle_success:
            return True

        # Case 3: Both fail
        if not buggy_success and not oracle_success:
            # Check if error messages are different
            #return True
            return False

        # No bug detected
        return False

    def detect_bug(self, query):
        """
        Runs a query on both the buggy and oracle version and checks for discrepancies.

        :param query: The SQL query to test
        :return: (is_bug: bool, bug_info: dict)
        """
        buggy_success, buggy_output, buggy_error = self.buggy_runner.run_query(query)
        oracle_success, oracle_output, oracle_error = self.oracle_runner.run_query(query)

        if self.is_bug(buggy_success, buggy_output, buggy_error,
                       oracle_success, oracle_output, oracle_error):
            bug_info = {
                'query': query,
                'buggy_success': buggy_success,
                'buggy_output': buggy_output,
                'buggy_error': buggy_error,
                'oracle_success': oracle_success,
                'oracle_output': oracle_output,
                'oracle_error': oracle_error
            }
            self.logger.log_bug(bug_info)

        if oracle_success:
            return True
        return False

    def close(self):
        """
        Closes the database runners to ensure .gcda files are properly flushed.
        """
        self.buggy_runner.close()
        self.oracle_runner.close()
