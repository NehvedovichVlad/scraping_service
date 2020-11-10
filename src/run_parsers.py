import codecs
import os, sys

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = "scraping_service.settings"

import django
django.setup()

from django.db import DatabaseError
from scraping.parsers import *

from scraping.models import Vacancy, City, Language

parsers = (
    (rabota_by,
     'https://rabota.by/search/vacancy?clusters=true&enable_snippets=true&text=Python&L_save_area=true&area=1002&from=cluster_area&showClusters=true'),
    (belmeta,
     'https://belmeta.com/%D0%B2%D0%B0%D0%BA%D0%B0%D0%BD%D1%81%D0%B8%D0%B8/Python/%D0%9C%D0%B8%D0%BD%D1%81%D0%BA'),
    (dev_by, 'https://jobs.dev.by/?filter[city_id][]=4429&filter[search]=python')
)

city = City.objects.filter(slug='minsk').first()
language = Language.objects.filter(slug='python').first()

jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass

# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()
