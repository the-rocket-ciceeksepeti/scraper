import requests
from bs4 import BeautifulSoup
import bleach
import json
from concurrent.futures import ThreadPoolExecutor


def get_image_ursl(url):
    try:
        page = BeautifulSoup(requests.get(url).content, features='html5lib').find_all(
            "div", attrs={"class": "complaint-img"})
        x =  list(map(lambda x: x[0]["href"], map(lambda x: x.find_all('a', href=True), page)))
        return x
    except:
        return "failedFF"


complaints_base_url = 'https://www.sikayetvar.com/cicek-sepeti'
base_url = 'https://www.sikayetvar.com'


max_page_number = 1777


content = BeautifulSoup(requests.get(
    complaints_base_url).content, features='html5lib')

complaints = map(lambda x: base_url+x.find_all('h2')[0].find_all('a', href=True)[0]['href'], filter(lambda x: len(x.find_all(
    'h2', attrs={'class': 'delete-message'})) == 0, content.find_all('article')))


results = []

for c in complaints:
    results += get_image_ursl(c)

for _ in range(1, 1+1):
   
    def get(i):
        
        to_req = complaints_base_url + "?page={}".format(i)

        content = BeautifulSoup(requests.get(
            to_req).content, features='html5lib')

        complaints = map(lambda x: base_url+x.find_all('h2')[0].find_all('a', href=True)[0]['href'], filter(lambda x: len(x.find_all(
            'h2', attrs={'class': 'delete-message'})) == 0, content.find_all('article')))

        for c in complaints:
            results.extend(get_image_ursl(c))
            if len(results) >= 1500:
                print(*results, sep="\n")
                exit(0)

    with ThreadPoolExecutor(max_workers=6) as exc:
        list(exc.map(get, range(1, max_page_number+1)))


print(*results, sep="\n")
