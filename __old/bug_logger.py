import os

class BugLogger:
    def __init__(self, base_dir="bugs"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.counter = 0

    def log_bug(self, bug_info):
        """
        Save the bug information into a structured directory.
        :param bug_info: Dictionary with query, outputs and errors
        """
        self.counter += 1
        bug_dir = os.path.join(self.base_dir, f"bug_{self.counter:03d}")
        os.makedirs(bug_dir, exist_ok=True)

        # Save the original SQL query
        with open(os.path.join(bug_dir, "original_test.sql"), "w") as f:
            f.write(bug_info['query'])

        # Save outputs from both buggy and oracle versions into a single file
        combined_output_path = os.path.join(bug_dir, "outputs.txt")
        with open(combined_output_path, "w") as f:
            f.write("=== Buggy Version ===\n")
            f.write(f"Success: {bug_info['buggy_success']}\n")
            f.write("Output:\n")
            f.write(bug_info['buggy_output'])
            if bug_info['buggy_error']:
                f.write("\nError:\n")
                f.write(bug_info['buggy_error'])

            f.write("\n\n=== Oracle Version (3.49.1) ===\n")
            f.write(f"Success: {bug_info['oracle_success']}\n")
            f.write("Output:\n")
            f.write(bug_info['oracle_output'])
            if bug_info['oracle_error']:
                f.write("\nError:\n")
                f.write(bug_info['oracle_error'])

        print(f"[!] Bug saved to {bug_dir}")
