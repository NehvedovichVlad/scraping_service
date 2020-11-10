import requests
import codecs

from bs4 import BeautifulSoup as BS

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}


def rabota_by(url):
    jobs = []
    errors = []
    domain = 'https://rabota.by'
    url = 'https://rabota.by/search/vacancy?area=1002&fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', attrs={"class": "vacancy-serp"})
        if main_div:
            div_lst = main_div.find_all('div', attrs={"data-qa": "vacancy-serp__vacancy"})
            for div in div_lst:
                title = div.find('div', attrs={"class": "vacancy-serp-item__row_header"})
                href = title.a['href']
                company = div.find('a', attrs={"data-qa": "vacancy-serp__vacancy-employer"})
                adress = div.find('span', attrs={"data-qa": "vacancy-serp__vacancy-address"})
                content = div.find('div', attrs={"class": "g-user-content"})
                jobs.append({'title': title.text, 'url': href, 'description': content.text,
                             'company': company.text})
        else:
            errors.append({'url': url, 'title': "Div didn't exists"})
    else:
        errors.append({'url': url, 'title': "Page don't response"})

    return jobs, errors


def belmeta(url):
    jobs = []
    errors = []
    domain = 'https://belmeta.com'
    url = 'https://belmeta.com/%D0%B2%D0%B0%D0%BA%D0%B0%D0%BD%D1%81%D0%B8%D0%B8/Python/%D0%9C%D0%B8%D0%BD%D1%81%D0%BA'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        table = soup.find('div', attrs={"class": "jobs"})
        if table:
            div_lst = table.find_all('article', attrs={"class": "job no-logo"})
            for div in div_lst:
                title = div.find('h2', attrs={"class": "title"})
                href = title.a['href']
                company = div.find('div', attrs={"class": "job-data company"})
                adress = div.find('div', attrs={"class": "job-data region"})
                content = div.find('div', attrs={"class": "desc"})
                jobs.append(
                    {'title': title.text, 'url': domain + href, 'description': content.text, 'company': company.text})
        else:
            errors.append({'url': url, 'title': "Table didn't exists"})
    else:
        errors.append({'url': url, 'title': "Page don't response"})
    return jobs, errors


def dev_by(url):
    jobs = []
    errors = []
    domain = 'https://jobs.dev.by'
    #url = 'https://jobs.dev.by/?&filter[search]=python'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        list_body = soup.find('div', attrs={"class": "vacancies-list__scroll-block"})
        if list_body:
            div_lst = list_body.find_all('div', attrs={"class": "vacancies-list-item--marked"})
            for div in div_lst:
                title = div.find('div', attrs={"class": "vacancies-list-item__position"})
                href = title.a['href']
                company = div.a.text
                adress = "no adress"
                #получить все данные
                content = div.find_all('div', attrs={"class": "vacancies-list-item__technology-tag__name"})
                for i in content:
                    i.text
                if content:
                    jobs.append(
                        {'title': title.text, 'url': domain + href, 'description': content, 'company': company})
                else:
                    jobs.append(
                        {'title': title.text, 'url': domain + href, 'description': "no description", 'company': company})
        else:
            errors.append({'url': url, 'title': "List_body didn't exists"})
    else:
        errors.append({'url': url, 'title': "Page don't response"})
    return jobs, errors


if __name__ == '__main__':
    url = 'https://jobs.dev.by/?&filter[search]=python'
    jobs, errors = dev_by(url)
    h = codecs.open('work.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
