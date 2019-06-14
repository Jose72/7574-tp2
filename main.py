import json
from time import sleep
import uuid
import sys
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.middleware.tpipe import TPipe
from src.processing.factory import ProcessorFactory


def main():
    consumer_tag = uuid.uuid1().hex

    with open(sys.argv[1], 'r+') as c_file:
        config_info = json.load(c_file)
        c_file.close()

        processor = ProcessorFactory.create(config_info["processor_config"])

        p = TPipe(config_info["in_config"], config_info["out_config"], processor, consumer_tag)
        p.run()


if __name__ == "__main__":
    main()
