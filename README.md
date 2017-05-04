# AsyncScrapper
Asynchronous Web Scraper (gevent + BeautifulSoup)

To run:
Goto AsynCrapper directory in terminal
>>python scraper_test.py input.csv

Add urls in input.csv or create a new csv file with urls and pass it as an argument

Output:
Url containing 'jquery.js' added in generated_csv/accepted.csv
If not, added in generated_csv/rejected.csv
