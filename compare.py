
import tempfile
import subprocess


old_sqlite = "/usr/bin/sqlite3-3.26.0"
new_sqlite = "/usr/bin/sqlite3-3.49.1"

sql = """CREATE TABLE t_hmgX (c_jx413v9W TEXT PRIMARY KEY, UNIQUE (c_jx413v9W), FOREIGN KEY (c_jx413v9W) REFERENCES t_Xu5JM(c_tnNum));
ALTER TABLE t_hmgX RENAME COLUMN c_jx413v9W TO c_FIJwkt;"""

try:
    with (
        tempfile.NamedTemporaryFile() as tmpdb,
        tempfile.NamedTemporaryFile() as tmpdb2,
    ):
        # Run the old SQLite version
        cmd = [old_sqlite, tmpdb.name]
        result_old = subprocess.run(
            cmd, input=sql.encode(), capture_output=True, timeout=5
        )

        # Run the new SQLite version
        cmd = [new_sqlite, tmpdb2.name]
        result_new = subprocess.run(
            cmd, input=sql.encode(), capture_output=True, timeout=5
        )


        # Add error handling to prevent UTF-8 decode errors
        out_old = result_old.stdout.decode(errors="replace")
        err_old = result_old.stderr.decode(errors="replace")
        out_new = result_new.stdout.decode(errors="replace")
        err_new = result_new.stderr.decode(errors="replace")

        if(err_old or err_new):
            print("Got error:")
            print("Err_old:")
            print(err_old)
            print("Err_new:")
            print(err_new)

        if(out_old != out_new):
            print("Out_old:")
            print(out_old)
            print("")
            print("Out_new:")
            print(out_new)
            print("")
        else:
            print("No difference found")

except Exception as e:
    print(f"\n❗ Got exception: {e}") 