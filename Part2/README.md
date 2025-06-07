To run for Linux:
sudo docker build -t reduce-env .
sudo docker run -it -v $(pwd):/app  reduce-env reducer

To run for Mac:
docker build --platform linux/amd64 -t reduce-env .
docker run -it -v $(pwd):/app  reduce-env reducer