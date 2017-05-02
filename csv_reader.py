import csv
import os

cd = os.path.dirname(os.path.abspath(__file__))     #Current Directory


# Generator for retrieving urls
def csv_url_reader(filename):
    with open(filename, "rb") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            try:
                yield row[0]
            except IndexError:
                continue


def csv_writer(url, accept=True):
    if accept:
        with open(os.path.join(cd, 'accepted.csv'), 'a') as accepted:
            writer = csv.writer(accepted)
            writer.writerow([url])
    else:
        with open(os.path.join(cd, 'rejected.csv'), 'a') as accepted:
            writer = csv.writer(accepted)
            writer.writerow([url])

if __name__ == '__main__':
    for i in csv_url_reader():
        print i
