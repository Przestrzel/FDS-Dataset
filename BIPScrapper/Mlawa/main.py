import os
import sys

import requests
from urllib.request import urlopen

from bs4 import BeautifulSoup


def init_links():
    main_links = list([])
    base = 'https://bip.mlawa.pl/zamowienia-publiczne?view_expired=1&page='
    for i in range(10):
        main_links.append(base + str(i))
    return main_links


def check_validity(my_url):
    try:
        urlopen(my_url)
        print("Valid URL")
    except IOError:
        print("Invalid URL")
        sys.exit()


def get_subpages(subpage_url, file_num):
    html = urlopen(subpage_url).read()
    soup = BeautifulSoup(html, features="html.parser")
    subpages_div = soup.find("table", {"class": "public-procurements-list"})
    procurements_links = list([])
    subpages_links = subpages_div.find_all("a")
    subpage_iterator = 0
    for subpage_link in subpages_links:
        if 'mailto' not in subpage_link.get('href'):
            subpage_iterator += 1
            file_num +=1
            new_subpage_url = "https://bip.mlawa.pl" + subpage_link.get('href')
            print(new_subpage_url)
            procurements_links.append(new_subpage_url)
            get_pdfs(new_subpage_url, file_num)
    print("All subpages founds")
    return file_num


def get_pdfs(my_url, subpage_number):
    html = urlopen(my_url).read()
    soup = BeautifulSoup(html, features="html.parser")
    subpages = []
    offer = soup.find("div", {"class": "field field--name-field-attachments-offer field--type-file field--label-above"})
    if offer is not None:
        print ('offer')
        subpages.append(offer)
    winner = soup.find("div", {"class": "field field--name-field-attachments-winner field--type-file field--label-above"})
    if winner is not None:
        print('winner')
        subpages.append(winner)
    cancel = soup.find("div", {"class": "field field--name-field-attachments-cancel field--type-file field--label-above"})
    if cancel is not None:
        print('cancel')
        subpages.append(cancel)
    iterator = 0
    for divs in subpages:
        for link in divs.find_all("a"):
            if link.get('href').endswith('pdf'):
                iterator += 1
                print(link.get('href'))
                response = requests.get(link.get('href'))
                os.makedirs("./" + str(subpage_number), exist_ok=True)
                pdf = open("./" + str(subpage_number) + "/" + link.text, 'wb')
                pdf.write(response.content)
                pdf.close()

                print("File ", iterator, " downloaded")
    if iterator == 0:
        print('not Found')
    else:
        print("All PDF files downloaded")


if __name__ == '__main__':
    print("Start processing...")
    links = init_links()
    number = 1
    file_num = 0
    for base_url in links:
        print("Web page number ", number)
        number += 1
        check_validity(base_url)
        file_num = get_subpages(base_url, file_num)
    print("End processing...")

