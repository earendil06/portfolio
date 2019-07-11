build : docker build -t portfolio .

dev : docker run -p 5000:5000 -v $PWD:/app portfolio

prod : docker run -p 5000:5000 portfolio


docker-compose pull

docker-compose up -d --force-recreate