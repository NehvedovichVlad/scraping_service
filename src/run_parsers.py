import codecs

from scraping.parsers import *

parsers = (
    (rabota_by, 'https://rabota.by/search/vacancy?area=1002&fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post'),
    (belmeta, 'https://belmeta.com/%D0%B2%D0%B0%D0%BA%D0%B0%D0%BD%D1%81%D0%B8%D0%B8/Python/%D0%9C%D0%B8%D0%BD%D1%81%D0%BA'),
    (dev_by, 'https://jobs.dev.by/?&filter[search]=python')
)

jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()
