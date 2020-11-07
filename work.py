import requests
import codecs

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
     }

url = 'https://rabota.by/search/vacancy?area=1002&fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post'
resp = requests.get(url, headers=headers)

h = codecs.open('work.html', 'w', 'utf-8')
h.write(str(resp.text))
h.close()