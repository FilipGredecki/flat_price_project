import requests
from bs4 import BeautifulSoup 
import random
import csv
import time
import os

HEADERS_LIST = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/90.0"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; rv:11.0) like Gecko"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/77.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Edge/90.0"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Chrome/80.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/88.0"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/89.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; rv:11.0) like Gecko"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/87.0"}
]

def collect_links(i):
    
    headers = random.choice(HEADERS_LIST)
    url = make_otodom_link(i)
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,features='lxml')
    links = soup.find_all('a', {'data-cy': 'listing-item-link'})

    return [link['href'] for link in links]
        



def make_otodom_link(i):
    return f'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/cala-polska?viewType=listing&limit=72&page={i}&by=LATEST&direction=DESC'

def saves_links_to_csv(links_list):
    with open("flat_links.csv",'a',encoding='utf-8') as file:
        writer = csv.writer(file,delimiter=';')
        writer.writerows([[f'https://www.otodom.pl{link.split('?')[0]}','False'] for link in links_list])

def save_headers_if_file_empty():
    if not os.path.exists("flat_links.csv") or os.path.getsize("flat_links.csv") == 0:
        with open("flat_links.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["link", "status"])


def make_and_update_checkpoint(page_number):
    with open("checkpoint", "w") as file:
        file.write(str(page_number))

def collecting_links_for_flats():
    save_headers_if_file_empty()
    if os.path.exists("checkpoint") or os.path.getsize("checkpoint") == 0:
        with open("checkpoint", "r") as file:
            last_saved_page = int(file.read())
    else: last_saved_page = 1
    links_list = []
    y = 0
    for i in range(last_saved_page,2401):
        print(i,'--start')
        x = time.time()
        links_list.extend(collect_links(i))
        if i % 50 == 0 :
            saves_links_to_csv(links_list)
            make_and_update_checkpoint(i+1)
            links_list = []
            print(f'pages from{i-49} - {i}')
            print(y,'--szacowany czas: ',int((2400-i)/50*y/60),'minutes')
            y=0
        y += time.time()-x
    if links_list:
        saves_links_to_csv(links_list)
        make_and_update_checkpoint(i+1)

collecting_links_for_flats()
