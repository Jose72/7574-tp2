import sys
import json

DISPATCHER = "\
  dispatcher:\n\
    build: .\n\
    command: python3 dispatcher_main.py ./config/dispatcher.json {}\n\
    image: 7574-tp2-dispatcher\n\
    volumes:\n\
        - ./config:/TP2/config\n\
    environment:\n\
        - PYTHONUNBUFFERED=1\n"

FILTER_INBOUND = "\
  filter_inbound_{}:\n\
    command: python3 main.py ./config/filter_inbound.json {} {}\n\
    image: 7574-tp2\n\
    volumes:\n\
        - ./config:/TP2/config\n\
    environment:\n\
        - PYTHONUNBUFFERED=1\n"

FILTER_COLUMNS = "\
  filter_columns_{}:\n\
    build: .\n\
    command: python3 main.py ./config/filter_columns.json {} {}\n\
    image: 7574-tp2\n\
    volumes:\n\
        - ./config:/TP2/config\n\
    environment:\n\
        - PYTHONUNBUFFERED=1\n"

TEXT_PROCESSING = "\
  text_processing_{}:\n\
    build: .\n\
    command: python3 main.py ./config/text_processing.json {} {} {}\n\
    image: 7574-tp2\n\
    volumes:\n\
        - ./config:/TP2/config\n\
    environment:\n\
        - PYTHONUNBUFFERED=1\n"

FILTER_USER = "\
  filter_user_{}:\n\
    build: .\n\
    command: python3 main.py ./config/filter_user.json {} {}\n\
    image: 7574-tp2\n\
    volumes:\n\
        - ./config:/TP2/config\n\
    environment:\n\
        - PYTHONUNBUFFERED=1\n"

FILTER_DATE = "\
  filter_date_{}:\n\
    build: .\n\
    command: python3 main.py ./config/filter_date.json {} {}\n\
    image: 7574-tp2\n\
    volumes:\n\
        - ./config:/TP2/config\n\
    environment:\n\
        - PYTHONUNBUFFERED=1\n"

AGGREGATOR_USERS = "\
  aggregator_users_{}:\n\
    build: .\n\
    command: python3 main.py ./config/aggregator_users.json {} {}\n\
    image: 7574-tp2\n\
    volumes:\n\
        - ./config:/TP2/config\n\
        - ./results:/TP2/results\n\
    environment:\n\
        - PYTHONUNBUFFERED=1\n"

AGGREGATOR_TOTAL = "\
  aggregator_total_{}:\n\
    build: .\n\
    command: python3 main.py ./config/aggregator_total.json {} {}\n\
    image: 7574-tp2\n\
    volumes:\n\
        - ./config:/TP2/config\n\
        - ./results:/TP2/results\n\
    environment:\n\
        - PYTHONUNBUFFERED=1\n"

SINK_USERS = "\
  sink_users:\n\
    build: .\n\
    command: python3 main.py ./config/sink_users.json {}\n\
    image: 7574-tp2\n\
    volumes:\n\
        - ./config:/TP2/config\n\
        - ./results:/TP2/results\n\
    environment:\n\
        - PYTHONUNBUFFERED=1\n"

SINK_TOTAL = "\
  sink_total:\n\
    build: .\n\
    command: python3 main.py ./config/sink_total.json {}\n\
    image: 7574-tp2\n\
    volumes:\n\
        - ./config:/TP2/config\n\
        - ./results:/TP2/results\n\
    environment:\n\
        - PYTHONUNBUFFERED=1\n"


HEADER = "\
version: '3'\n\
services:\n"


def main():

    n_filter_inbound = int(sys.argv[1])
    n_filter_columns = int(sys.argv[2])
    n_text_processor = int(sys.argv[3])
    n_filter_user = int(sys.argv[4])
    n_filter_date = int(sys.argv[5])
    n_aggregator_users = int(sys.argv[6])
    n_aggregator_total = int(sys.argv[7])
    with open("./docker-compose_dispatcher.yaml", 'w+') as f:
        f.write(HEADER)
        f.write(DISPATCHER.format(n_filter_inbound))
        f.close()

    with open("./docker-compose.yaml", 'w+') as f:

        f.write(HEADER)

        for i in range(0, n_filter_inbound):
            f.write(FILTER_INBOUND.format(i+1, 1, n_filter_columns))

        for i in range(0, n_filter_columns):
            f.write(FILTER_COLUMNS.format(i+1, n_filter_inbound, n_text_processor))

        for i in range(0, n_text_processor):
            f.write(TEXT_PROCESSING.format(i+1, n_filter_columns, n_filter_user, n_filter_date))

        for i in range(0, n_filter_user):
            f.write(FILTER_USER.format(i+1, n_text_processor, n_aggregator_total))

        for i in range(0, n_filter_date):
            f.write(FILTER_DATE.format(i+1, n_text_processor, n_aggregator_users))

        for i in range(0, n_aggregator_users):
            f.write(AGGREGATOR_USERS.format(i+1, n_filter_date, 1))

        for i in range(0, n_aggregator_total):
            f.write(AGGREGATOR_TOTAL.format(i+1, n_filter_user, 1))

        f.write(SINK_USERS.format(n_aggregator_users))
        f.write(SINK_TOTAL.format(n_aggregator_total))
        f.close()


if __name__ == "__main__":
    main()
