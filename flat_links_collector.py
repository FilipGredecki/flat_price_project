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
    if  os.path.exists("flat_links.csv") and os.path.getsize("flat_links.csv") == 0:
        with open("flat_links.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["link", "status"])
    elif not os.path.exists("flat_links.csv"):
        with open("flat_links.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["link", "status"])

def make_and_update_checkpoint(page_number):
    if not os.path.exists('checkpoint'):
        with open("checkpoint",'w',encoding='utf-8'):

def collecting_links_for_flats():
    save_headers_if_file_empty()
    links_list = []
    y = 0
    for i in range(1,2401):
        
        print(i,'--start')
        x = time.time()
        links_list.extend(collect_links(i))
        print(links_list[-1])
        if i % 10 == 0 :
            saves_links_to_csv(links_list)
            links_list = []
            print(f'pages from{i-49} - {i}')
            print(y,'--szacowany czas: ',(2400-i)/10*y/60)
            y=0
        y += time.time()-x

collecting_links_for_flats()
