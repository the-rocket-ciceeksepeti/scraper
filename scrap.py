import requests
from bs4 import BeautifulSoup
import bleach
import json
from concurrent.futures import ThreadPoolExecutor


def get_msg(url):
    page = BeautifulSoup(requests.get(url).content, features='html5lib').find_all(
        "div", attrs={"class": "description"})[0].find_all("p")[0]
    return bleach.clean(str(page), tags=[], strip=True)


complaints_base_url = 'https://www.sikayetvar.com/cicek-sepeti'
base_url = 'https://www.sikayetvar.com'


max_page_number = 1777


content = BeautifulSoup(requests.get(
    complaints_base_url).content, features='html5lib')

complaints = map(lambda x: base_url+x.find_all('h2')[0].find_all('a', href=True)[0]['href'], filter(lambda x: len(x.find_all(
    'h2', attrs={'class': 'delete-message'})) == 0, content.find_all('article')))


results = []

for c in complaints:
    results.append({"id": len(results), "text": get_msg(c)})


for _ in range(1, 1+1):

    def get(i):
        to_req = complaints_base_url + "?page={}".format(i)

        content = BeautifulSoup(requests.get(
            complaints_base_url).content, features='html5lib')

        complaints = map(lambda x: base_url+x.find_all('h2')[0].find_all('a', href=True)[0]['href'], filter(lambda x: len(x.find_all(
            'h2', attrs={'class': 'delete-message'})) == 0, content.find_all('article')))
        
        for c in complaints:
            results.append({"id": len(results), "text": get_msg(c)})

    with ThreadPoolExecutor(max_workers=6) as exc:
        list(exc.map(get, range(1, max_page_number+1)))

print(json.dumps(results))
