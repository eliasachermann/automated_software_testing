
import tempfile
import subprocess
import argparse


old_sqlite = "/usr/bin/sqlite3-3.26.0"
new_sqlite = "/usr/bin/sqlite3-3.39.4"

def test(sql: str, oracle: str) -> bool:

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
            
            crashed_old = result_old.returncode != 0
            crashed_new = result_new.returncode != 0


            # Add error handling to prevent UTF-8 decode errors
            out_old = result_old.stdout.decode(errors="replace")
            err_old = result_old.stderr.decode(errors="replace")
            out_new = result_new.stdout.decode(errors="replace")
            err_new = result_new.stderr.decode(errors="replace")

            print(f"Old SQLite output: {out_old}")
            print(f"New SQLite output: {out_new}")
            print(f"Old SQLite error: {err_old}")
            print(f"New SQLite error: {err_new}")

            if oracle == "DIFF":
                if out_old != out_new or err_old != err_new:
                    return True
                else:
                    return False
                
            elif oracle == "CRASH(3.26.0)":
                if crashed_old and not crashed_new:
                    return True
                else:
                    return False
                
            else:
                raise ValueError(f"Unknown oracle: {oracle}")
            

    except Exception as e:
        print(f"\n❗ Got exception: {e}") 



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--oracle", required=True)
    args = parser.parse_args()

    print(f"Testing query: {args.query} with oracle: {args.oracle}")

    try:
        with open(args.query, 'r') as f:
            sql_query = f.read().strip()
    except Exception as e:
        print(f"Error reading query file: {e}")
        exit(1)
    
    print(f"SQL Query: {sql_query}")
    test(sql_query, args.oracle)
