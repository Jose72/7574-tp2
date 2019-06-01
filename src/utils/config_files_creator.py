import sys
import json
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

FILTER_INBOUND_CONFIG = \
  {
    "processor_code": "filter",
    "fields": ["inbound"],
    "conditions": [True],
    "remove": True
  }

FILTER_COLUMNS_CONFIG = \
  {
    "processor_code": "filter",
    "fields": ["tweet_id", "response_tweet_id", "in_response_to_tweet_id"],
    "conditions": [],
    "remove": True
  }

TEXT_PROCESSOR_CONFIG = \
  {
    "processor_code": "text_processor",
    "field": "text",
    "new_field": "score",
    "remove": True
  }

FILTER_USER_CONFIG = \
  {
    "processor_code": "filter",
    "fields": ["author_id"],
    "conditions": [],
    "remove": True
  }

FILTER_DATE_CONFIG = \
  {
    "processor_code": "filter",
    "fields": ["created_at"],
    "conditions": [],
    "remove": True
  }

AGGREGATOR_USERS_CONFIG = \
  {
    "processor_code": "aggregator_users",
    "user_field": "author_id",
    "aggregate_field": "score"
  }

AGGREGATOR_TOTAL_CONFIG = \
  {
    "processor_code": "aggregator_total",
    "date_field": "created_at",
    "aggregate_field": "score"
  }

SINK_USERS_CONFIG = \
  {
    "processor_code": "sink_users",
    "user_field": "author_id",
    "aggregate_field": "negative_tweets"
  }

SINK_TOTAL_CONFIG = \
  {
    "processor_code": "sink_total",
    "date_field": "day",
    "aggregate_field_p": "positive_tweets",
    "aggregate_field_n": "negative_tweets"
  }


def create_config_file(file_name, in_host, in_queue, prod_n,
                       out_c, processor_c):

    with open("./config/{}.json".format(file_name), 'w+') as f:

        config = {}

        in_config = {"host_name_in": in_host, "in_q_name": in_queue, "in_r_key": in_queue, "producers": prod_n}

        config["in_config"] = in_config

        out_configs = []
        for oc in out_c:
            out_config = {"host_name_out": oc[0], "out_q_name": oc[1], "out_r_key": oc[1], "consumers": oc[2]}
            out_configs.append(out_config)

        config["out_config"] = out_configs

        config["processor_config"] = processor_c

        json.dump(config, f, indent=3, sort_keys=True)

        f.close()


def create_config_files(n_filter_inbound, n_filter_columns, n_text_processor, n_filter_user, n_filter_date,
                        n_aggregator_users, n_aggregator_total):
    host = "rabbitmq"

    create_config_file("filter_inbound", host, "full_tweets", 1, [["rabbitmq", "inbound_tweets", n_filter_columns]],
                       FILTER_INBOUND_CONFIG)

    create_config_file("filter_columns", host, "inbound_tweets", n_filter_inbound,
                       [["rabbitmq", "pre_analyze_tweets", n_text_processor]],
                       FILTER_COLUMNS_CONFIG)

    create_config_file("text_processing", host, "pre_analyze_tweets", n_filter_columns,
                       [["rabbitmq", "post_analyze_tweets_a1", n_filter_user],
                        ["rabbitmq", "post_analyze_tweets_a2", n_filter_date]],
                       TEXT_PROCESSOR_CONFIG)

    create_config_file("filter_user", host, "post_analyze_tweets_a2", n_text_processor,
                       [["rabbitmq", "post_analyze_tweets_a2_filtered", n_aggregator_total]],
                       FILTER_USER_CONFIG)

    create_config_file("filter_date", host, "post_analyze_tweets_a1", n_text_processor,
                       [["rabbitmq", "post_analyze_tweets_a1_filtered", n_aggregator_users]],
                       FILTER_DATE_CONFIG)

    create_config_file("aggregator_users", host, "post_analyze_tweets_a1_filtered", n_filter_date,
                       [["rabbitmq", "sink_tweets_a1", 1]],
                       AGGREGATOR_USERS_CONFIG)

    create_config_file("aggregator_total", host, "post_analyze_tweets_a2_filtered", n_filter_user,
                       [["rabbitmq", "sink_tweets_a2", 1]],
                       AGGREGATOR_TOTAL_CONFIG)

    create_config_file("sink_users", host, "sink_tweets_a1", n_aggregator_users,
                       [], SINK_USERS_CONFIG)

    create_config_file("sink_total", host, "sink_tweets_a2", n_aggregator_total,
                       [], SINK_TOTAL_CONFIG)


if __name__ == "__main__":
    n_filter_inbound = int(sys.argv[1])
    n_filter_columns = int(sys.argv[2])
    n_text_processor = int(sys.argv[3])
    n_filter_user = int(sys.argv[4])
    n_filter_date = int(sys.argv[5])
    n_aggregator_users = int(sys.argv[6])
    n_aggregator_total = int(sys.argv[7])
    create_config_files(n_filter_inbound, n_filter_columns, n_text_processor, n_filter_user, n_filter_date,
                        n_aggregator_users, n_aggregator_total)
