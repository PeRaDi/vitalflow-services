sudo docker build -t nginx-cdn .
sudo docker run -d -p 80:80 --name nginx-cdn nginx-cdn
docker container stop nginx-cdn
sudo docker container rm nginx-cdn