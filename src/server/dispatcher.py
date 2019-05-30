import csv
import json
from time import sleep

class Dispatcher:

    @staticmethod
    def dispatch(file_path, fieldnames, pipe):
        with open(file_path, 'r+', encoding='utf-8') as f:

            reader = csv.DictReader(f,
                                    delimiter=',',
                                    quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL,
                                    fieldnames=fieldnames)

            header = next(reader)

            counter = 0

            for e in reader:
                print(json.dumps(e))
                pipe.send(e)
                counter += 1
                if counter == 100:
                    sleep(0.2)
                    counter = 0
            f.close()
