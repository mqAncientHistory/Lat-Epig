docker build -t latepig:latepig .
docker run --publish 8888:8888 -it latepig:latepig
