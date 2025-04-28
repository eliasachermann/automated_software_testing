To run:  
python3 fuzznew.py --iterations number_of_iterations --processes parallel_processes  --old-sqlite path_to_old_sqlite --new-sqlite path_to_new_sqlite
python3 fuzznew.py --iterations 5000 --processes 8  --old-sqlite /usr/bin/sqlite3-3.26.0 --new-sqlite /usr/bin/sqlite3-3.39.4

python3 fuzznew.py --iterations 5000 --processes 8  --old-sqlite /usr/bin/sqlite3-3.39.4 --new-sqlite /usr/bin/sqlite3-3.49.1

Docker

Build image from dockerfile:
docker build --platform linux/amd64 -t sqlite-fuzz-env .

Run Container:
docker run --platform linux/amd64 -it \
  -v $(pwd):/app \
  sqlite-fuzz-env