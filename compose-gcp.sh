# gcp method
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo docker build -t myapp .
sudo docker run -p 80:8000 myapp
