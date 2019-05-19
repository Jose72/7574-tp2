

from datetime import datetime


def main():
    datef = 'Wed Oct 11 13:25:49 +0000 2017'
    datetime_object = datetime.strptime(datef, '%a %b %d %H:%M:%S %z %Y')
    date = datetime_object.strftime('%Y-%m-%d')
    print(date)

if __name__ == "__main__":
    main()
