sudo docker build -f base-images/python-base.dockerfile -t rabbitmq-python-base:0.0.1 .
sudo docker build -f Dockerfile.tp2 -t 7574-tp2 .
sudo docker build -f Dockerfile.dispatcher -t 7574-tp2-dispatcher .
