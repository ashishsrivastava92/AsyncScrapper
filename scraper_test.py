from gevent import monkey, pool, spawn, joinall, sleep
monkey.patch_all()

# from timeit import timeit
# from socket import timeout
from urllib2 import urlopen, HTTPError, URLError
from httplib import BadStatusLine
from bs4 import BeautifulSoup
from csv_utils import csv_url_reader, csv_writer


class Scraper:
    def __init__(self, file_name):
        self.filename = file_name
        self.jobs = []
        self.pool = pool.Pool(20)

    def get_links(self, url):
        try:
            page = urlopen(url, timeout=5)
        except (URLError, HTTPError):
            # self.jobs.append(spawn(csv_writer, url, accept=False))     # Can add to rejected list if wanted
            print url, '-', "Url Error/ Unauthorized to scrape"
            return
        # except timeout:
        #     print url, ':', "Url TimeOut"
        except ValueError:
            print url, ':', "Invalid Url Type"
        except BadStatusLine:
            print url, '-', "Requires User Agent data"
        except Exception, e:
            from traceback import format_exc
            print url, '-', "Exception :", format_exc().splitlines()[-1]
            return
        else:
            if page.code == 200:
                soup = BeautifulSoup(page.read(), "lxml")
                sources = soup.findAll('script', {"src": True})
                for source in sources:
                    if 'jquery.js' in source['src']:
                        self.jobs.append(spawn(csv_writer, url))
                        return
                self.jobs.append(spawn(csv_writer, url, accept=False))       # add to rejected.csv
            return

    def job(self):
        # TODO: Implement bloom filter in csv_url_reader() for million records, If duplicate url don't create greenlet
        # For 100 entries hash map won't provide much improvement

        for link in csv_url_reader(self.filename):
            self.pool.spawn(self.get_links, link)
            # if p1.full():
            #     sleep(.2)
        self.pool.join(timeout=10)      # url request in pool
        joinall(self.jobs)      # Csv writer with gevent spawn


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


if __name__ == '__main__':
    from sys import argv
    try:
        filename = argv[1]
        scraper = Scraper(filename)
        # wrapped = wrapper(scraper.job)
        # timing = timeit(wrapped, number=1)
        # print timing
        scraper.job()
        if len(argv) > 2:
            raise IndexError
    except IndexError:
        print 'provide csv file'
    except Exception, e:
        print "Something went wrong... try again"
