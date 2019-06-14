
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.processing.aggregator import UserAggregator, TotalAggregator, NegativeTweetValidator
from src.processing.filter import Filter
from src.processing.analyzer import TextProcessor
from src.processing.sink import TotalSink, UserSink
from src.processing.processor import Processor


class ProcessorFactory:

    @staticmethod
    def create(config_info, out_pipes):
        p_code = config_info["processor_code"]
        if p_code == "filter":
            return Filter(out_pipes, config_info['fields'], config_info['conditions'], config_info['remove'])
        elif p_code == "text_processor":
            return TextProcessor(out_pipes, config_info['field'], config_info['new_field'], config_info['remove'])
        elif p_code == "aggregator_users":
            return UserAggregator(out_pipes, config_info['user_field'], config_info['aggregate_field'],
                                  NegativeTweetValidator)
        elif p_code == "aggregator_total":
            return TotalAggregator(out_pipes, config_info['date_field'], config_info['aggregate_field'])
        elif p_code == "sink_users":
            return UserSink(out_pipes, config_info['user_field'], config_info['aggregate_field'])
        elif p_code == "sink_total":
            return TotalSink(out_pipes, config_info['date_field'], config_info['aggregate_field_p'],
                             config_info['aggregate_field_n'])
        return Processor(out_pipes)
