To run for Linux:
sudo docker build -t sqlite-fuzz-env .
sudo docker run -it -v $(pwd):/app  sqlite-fuzz-env test-db

To run for Max:
docker build --platform linux/amd64 -t sqlite-fuzz-env .
docker run -it -v $(pwd):/app  sqlite-fuzz-env test-db

Optional flags are:
--iterations number_of_iterations --processes parallel_processes  --old-sqlite path_to_old_sqlite --new-sqlite 
Defaults are:
--iterations 10000 --processes 10  --old-sqlite path_to_old_sqlite --new-sqlite 