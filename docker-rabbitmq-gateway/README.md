sudo docker build -t rabbitmq-gateway .
sudo docker run -d -p 5672:5672 15672:15672 --env-file .env --name rabbitmq-gateway rabbitmq-gateway
docker container stop rabbitmq-gateway
sudo docker container rm rabbitmq-gateway
docker exec -it rabbitmq-gateway bash
ls -lh /var/log/