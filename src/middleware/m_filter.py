import json
import uuid
import sys
from multiprocessing import Queue
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.middleware.pipe import Pipe
from src.processing.filter import Filter
from src.server.receiver import Receiver
from src.server.sender import Sender
from src.middleware.pipe_2 import TPipe


class MFilter(TPipe):

        def __init__(self, config_info, c_id):

                in_pipe = Pipe(config_info['host_name'], config_info['in_q_name'], config_info['in_r_key'],
                               sys.argv[2], c_id)
                out_pipe = Pipe(config_info['host_name'], config_info['out_q_name'], config_info['out_r_key'],
                                sys.argv[3])
                f_filter = Filter(config_info['fields'], config_info['conditions'], config_info['remove'])

                super().__init__(in_pipe, [out_pipe], f_filter)



