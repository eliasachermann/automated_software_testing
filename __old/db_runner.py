import tempfile
import subprocess
import os

class DatabaseRunner:
    def __init__(self, sqlite_binary_path):
        self.sqlite_binary_path = sqlite_binary_path
        self.tmpdb = tempfile.NamedTemporaryFile(delete=False)
        self.tmpdb.close()  # Close it so SQLite can open it

    def run_query(self, query):
        try:
            # Create the process and run SQLite
            process = subprocess.Popen(
                [self.sqlite_binary_path, self.tmpdb.name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,  # Work with strings, not bytes
                bufsize=1   # Line buffering
            )

            # Send query
            process.stdin.write(query + ";\n")
            process.stdin.flush()

            # Communicate with process and capture output
            stdout, stderr = process.communicate(timeout=5)  # Ensure it doesn't hang

            # Check for errors in the process exit status
            success = process.returncode == 0

            return success, stdout, stderr
        except Exception as e:
            return False, "", f"Exception: {str(e)}"

    def close(self):
        # Remove the temp database
        try:
            os.unlink(self.tmpdb.name)
        except Exception:
            pass
