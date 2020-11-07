import requests
import codecs

from bs4 import BeautifulSoup as BS
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
     }

domain = 'https://rabota.by'
url = 'https://rabota.by/search/vacancy?area=1002&fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post'
resp = requests.get(url, headers=headers)
jobs=[]
if resp.status_code == 200:
    soup = BS(resp.content, 'html.parser')
    main_div = soup.find('div', attrs={"class": "vacancy-serp"})
    div_lst = main_div.find_all('div', attrs={"data-qa": "vacancy-serp__vacancy"})
    for div in div_lst:
        title = div.find('div', attrs={"class": "vacancy-serp-item__row_header"})
        href = title.a['href']
        company = div.find('a', attrs={"data-qa": "vacancy-serp__vacancy-employer"})
        address = div.find('span', attrs={"data-qa": "vacancy-serp__vacancy-address"})
        content = div.find('div', attrs={"class": "g-user-content"})
        jobs.append({'title': title.text, 'url': href, 'description': content.text,
                     'company': company.text})


h = codecs.open('work.text', 'w', 'utf-8')
h.write(str(jobs))
h.close()