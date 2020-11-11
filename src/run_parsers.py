import os
import sys

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = "scraping_service.settings"

import django

django.setup()

from django.db import DatabaseError
from scraping.parsers import *
from scraping.models import Vacancy, City, Language, Error, Url

User = get_user_model()

parsers = (
    (rabota_by,
     'https://rabota.by/search/vacancy?clusters=true&enable_snippets=true&text=Python&L_save_area=true&area=1002&from=cluster_area&showClusters=true'),
    (belmeta,
     'https://belmeta.com/%D0%B2%D0%B0%D0%BA%D0%B0%D0%BD%D1%81%D0%B8%D0%B8/Python/%D0%9C%D0%B8%D0%BD%D1%81%D0%BA'),
    (dev_by, 'https://jobs.dev.by/?filter[city_id][]=4429&filter[search]=python')
)


def get_settings():
    """Get set id language and city for our users"""
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst


def get_urls(_settings):
    """get url for each language with city"""
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = pair[pair]
        urls.append(tmp)
    return urls

q = get_settings()
u = get_urls(q)

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
if errors:
    er = Error(data=errors).save()

# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()
