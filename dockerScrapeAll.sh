docker build -t latepig:latepig .
#docker run -it latepig:latepig
docker rm laterpig
docker run --name laterpig --entrypoint '/bin/bash' -it latepig:latepig -c "cd /home/jovyan; bash search_by_provinces.sh" #-c "cd /home/jovyan/;python3 src/lat_epig/parse.py tumulus"
docker cp laterpig:/home/jovyan/output "full_scrape_$(date --iso-8601)"
