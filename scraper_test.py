import gevent
from gevent import monkey, pool
monkey.patch_all()
from timeit import timeit
from urllib2 import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup
from csv_reader import csv_url_reader, csv_writer

jobs = []
links = []
p = pool.Pool(10)


def get_links(url):
    try:
        page = urlopen(url, timeout=5)      # Raise URLError for timeout, indefinite wait problem
    except (URLError, HTTPError):
        print url, '-', "Invalid Url/ Unauthorized to scrape"
        return
    except Exception as e:
        from traceback import format_exc
        print url, '-', "Exception :", format_exc().splitlines()[-1]
        return
    else:
        if page.code == 200:
            soup = BeautifulSoup(page.read(), "lxml")
            sources = soup.findAll('script', {"src": True})
            for source in sources:
                print source['src']
                if 'dcmegamenu.1.2.js' in source['src']:
                    # csv_writer(url)     # add to accepted.csv
                    jobs.append(gevent.spawn(csv_writer, url))
                    return
            # csv_writer(url, accept=False)       # add to rejected.csv
            jobs.append(gevent.spawn(csv_writer, url, accept=False))
        return


def job(filename):
    # from sys import argv
    # try:
    # filename = argv[1]
    for link in csv_url_reader(filename):
        jobs.append(gevent.spawn(get_links, link))
    gevent.joinall(jobs)
    # if len(argv) > 2:
    #     raise IndexError
    # except IndexError:
    #     print 'provide csv file'


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


if __name__ == '__main__':
    from sys import argv
    filename = argv[1]
    wrapped = wrapper(job, filename)
    a = timeit(wrapped, number=1)
    print a
    # from sys import argv
    # try:
    #     filename = argv[1]
    #     for link in csv_url_reader(filename):
    #         jobs.append(gevent.spawn(get_links, link))
    #     gevent.joinall(jobs)
    #     if len(argv) > 2:
    #         raise IndexError
    # except IndexError:
    #     print 'provide csv file'

# def job(URLS):
#     for url in URLS:
#         jobs.append(p.spawn(get_links, url))
#     gevent.joinall(jobs)
#     return

# def wrapper(func, *args, **kwargs):
#     def wrapped():
#         return func(*args, **kwargs)
#     return wrapped

# urls.extend(a)
# wrapped = wrapper(job, urls)
# # job(urls)
# a = timeit.timeit(wrapped, number=1)
# print a
