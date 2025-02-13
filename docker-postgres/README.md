docker pull postgres:latest
sudo docker run -d \
  --name db-postgres \
  -e POSTGRES_USER= \
  -e POSTGRES_PASSWORD= \
  -e POSTGRES_DB= \
  -p 5432:5432 \
  postgres
