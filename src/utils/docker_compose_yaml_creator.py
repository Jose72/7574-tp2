import sys

DISPATCHER = "\
  dispatcher:\n\
    build:\n\
      context: ./\n\
      dockerfile: Dockerfile.dispatcher\n\
    volumes:\n\
        - ./:/7574-tp2\n\
    environment:\n\
        - PYTHONUNBUFFERED=1\n"

FILTER_INBOUND = "\
  filter_inbound_{}:\n\
    build:\n\
      context: ./\n\
      dockerfile: Dockerfile.filter_inbound\n\
    volumes:\n\
        - ./:/7574-tp2\n\
    environment:\n\
      - PYTHONUNBUFFERED=1\n"

FILTER_COLUMNS = "\
  filter_columns_{}:\n\
    build:\n\
      context: ./\n\
      dockerfile: Dockerfile.filter_columns\n\
    volumes:\n\
        - ./:/7574-tp2\n\
    environment:\n\
      - PYTHONUNBUFFERED=1\n"

TEXT_PROCESSING = "\
  text_processing_{}:\n\
    build:\n\
      context: ./\n\
      dockerfile: Dockerfile.text_processing\n\
    volumes:\n\
        - ./:/7574-tp2\n\
    environment:\n\
      - PYTHONUNBUFFERED=1\n"

AGGREGATOR_USERS = "\
  aggregator_users:\n\
    build:\n\
      context: ./\n\
      dockerfile: Dockerfile.aggregator_users\n\
    volumes:\n\
        - ./:/7574-tp2\n\
    environment:\n\
      - PYTHONUNBUFFERED=1\n"

AGGREGATOR_TOTAL = "\
  aggregator_total:\n\
    build:\n\
      context: ./\n\
      dockerfile: Dockerfile.aggregator_total\n\
    volumes:\n\
        - ./:/7574-tp2\n\
    environment:\n\
      - PYTHONUNBUFFERED=1\n"

HEADER = "\
version: '3'\n\
services:\n"


def main():

    n_filter_inbound = int(sys.argv[1])
    n_filter_columns = int(sys.argv[2])
    n_text_processor = int(sys.argv[3])
    with open("./docker-compose_dispatcher.yaml", 'w+') as f:
        f.write(HEADER)
        f.write(DISPATCHER)
        f.close()

    with open("./docker-compose.yaml", 'w+') as f:
        f.write(HEADER)
        #f.write(DISPATCHER)
        for i in range(0, n_filter_inbound):
            f.write(FILTER_INBOUND.format(i+1))
        for i in range(0, n_filter_columns):
            f.write(FILTER_COLUMNS.format(i+1))
        for i in range(0, n_text_processor):
            f.write(TEXT_PROCESSING.format(i+1))
        f.write(AGGREGATOR_USERS)
        f.write(AGGREGATOR_TOTAL)
        f.close()


if __name__ == "__main__":
    main()
