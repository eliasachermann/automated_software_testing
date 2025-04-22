To run:  
python3 fuzznew.py --iterations number_of_iterations --processes parallel_processes  --old-sqlite path_to_old_sqlite --new-sqlite path_to_new_sqlite
python3 fuzznew.py --iterations 5000 --processes 8  --old-sqlite /usr/bin/sqlite3-3.26.0 --new-sqlite /usr/bin/sqlite3-3.39.4