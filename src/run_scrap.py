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
from scraping.models import Vacancy, Error, Url

User = get_user_model()

"""parsers consists from function and key"""
parsers = (
    (dev_by, 'dev_by'),
    (belmeta, 'belmeta'),
    (rabota_by, 'rabota_by')
)

jobs, errors = [], []


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
        if pair in url_dct:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            tmp['url_data'] = url_dct[pair]
            urls.append(tmp)
    return urls


"""id language and city"""
settings = get_settings()
"""get url on id"""
url_list = get_urls(settings)

# city = City.objects.filter(slug='minsk').first()
# language = Language.objects.filter(slug='python').first()

for data in url_list:
    for func, key in parsers:
        url = data['url_data'][key]
        j, e = func(url, city=data['city'], language=data['language'])
        jobs += j
        errors += e

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    qs = Error.objets.filter(timestamp=dt.date.today())
    if qs.exsists():
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        er = Error(data=f'errors:{errors}').save()


# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()
