To run for Linux:
sudo docker build -t reduce-env .
sudo docker run -it -v $(pwd):/app  reduce-env reducer --query <query-to-minimize> --test <an arbitrary-script>

To run for Mac:
docker build --platform linux/amd64 -t reduce-env .
docker run -it -v $(pwd):/app  reduce-env reducer --query <query-to-minimize> --test <an arbitrary-script>