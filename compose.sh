# install docker, depends on your machine, this example is for ubuntu
# usage:
# git clone <this repo>
# cd <this repo>
# chmod +x compose.sh
# ./compose.sh (or sudo ./compose.sh)
sudo snap install docker
# start docker
sudo systemctl start docker
# build docker image
sudo docker build -t myapp .
# run docker image
sudo docker run -p 80:8000 myapp
