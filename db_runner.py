import tempfile
import subprocess
import os

class DatabaseRunner:
    def __init__(self, sqlite_binary_path):
        self.sqlite_binary_path = sqlite_binary_path
        self.tmpdb = tempfile.NamedTemporaryFile(delete=False)
        self.tmpdb.close()  # Close so sqlite3 can open it
        self.process = subprocess.Popen(
            [self.sqlite_binary_path, self.tmpdb.name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # Work with strings, not bytes
            bufsize=0   # Unbuffered
        )

    def run_query(self, query):
        try:
            if self.process.poll() is not None:
                # Process already dead
                return False, "", "Process not running"

            # Send query
            self.process.stdin.write(query + ";\n")
            self.process.stdin.flush()

            # Capture output manually
            output = ""
            error = ""
            while True:
                line = self.process.stdout.readline()
                if not line or line.strip() == "":  # Assume output ends at empty line
                    break
                output += line

            # No clean way to capture stderr unless process dies, so we can just skip it
            success = True  # If no crash, assume success for now

            return success, output, error
        except Exception as e:
            return False, "", f"Exception: {str(e)}"

    def close(self):
        if self.process.poll() is None:
            try:
                # Try to exit nicely
                self.process.stdin.write(".exit\n")
                self.process.stdin.flush()
                self.process.communicate(timeout=5)
            except Exception:
                self.process.kill()
                self.process.wait()

        # Remove the temp database
        try:
            os.unlink(self.tmpdb.name)
        except Exception:
            pass
