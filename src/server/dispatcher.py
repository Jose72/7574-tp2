import csv


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

            for e in reader:
                #print(json.dumps(e))
                pipe.send(e)

            f.close()
