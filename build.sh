sudo docker build -f Dockerfile.dispatcher -t 7574-tp2-dispatcher .
sudo docker build -f Dockerfile.filter_columns -t 7574-tp2-filter-columns .
sudo docker build -f Dockerfile.filter_inbound -t 7574-tp2-filter-inbound .
sudo docker build -f Dockerfile.text_processing -t 7574-tp2-text-processing .
sudo docker build -f Dockerfile.aggregator_users -t 7574-tp2-aggregator-users .
sudo docker build -f Dockerfile.aggregator_total -t 7574-tp2-aggregator-total .
