docker build -t latepig:latepig .
docker run --publish 8888:8888 --publish 8866:8866 -it latepig:latepig
