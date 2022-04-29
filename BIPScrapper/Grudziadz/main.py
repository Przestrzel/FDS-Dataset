import os
import sys

import requests
from urllib.request import urlopen

from bs4 import BeautifulSoup


def init_links():
    main_links = list([])
    main_links.append('http://bip.grudziadz.pl/zamowienia/lista/1.dhtml')
    return main_links


def check_validity(my_url):
    try:
        urlopen(my_url)
        print("Valid URL")
    except IOError:
        print("Invalid URL")
        sys.exit()


def get_subpages(subpage_url):
    html = urlopen(subpage_url).read()
    soup = BeautifulSoup(html, features="html.parser")
    subpages_div = soup.find("table", {"id" : "lista_zamowien"})
    procurements_links = list([])
    subpages_links = subpages_div.find_all("a")
    subpage_iterator = 0
    for subpage_link in subpages_links:
            subpage_iterator += 1
            new_subpage_url = "http://bip.grudziadz.pl" + subpage_link.get('href')
            print(new_subpage_url)
            procurements_links.append(new_subpage_url)
            check_validity(new_subpage_url)

            get_pdfs(new_subpage_url, subpage_iterator)
    print("All subpages founds")
    return procurements_links


def get_pdfs(my_url, subpage_number):
    html = urlopen(my_url).read()
    soup = BeautifulSoup(html, features="html.parser")
    subpages_div = soup.find("table", {"class": "table table-bordered table-striped"})
    iterator = 0
    for link in subpages_div.find_all("a"):
        if link.text.endswith('pdf'):
            iterator += 1
            print("Downloading file: ", iterator)

            response = requests.get("http://bip.grudziadz.pl" + link.get('href'))
            os.makedirs("./" + str(subpage_number), exist_ok=True)
            pdf = open("./" + str(subpage_number) + "/" + link.text, 'wb')
            pdf.write(response.content)
            pdf.close()

            print("File ", iterator, " downloaded")

    print("All PDF files downloaded")


if __name__ == '__main__':
    print("Start processing...")
    links = init_links()
    number = 1

    for base_url in links:
        print("Web page number ", number)
        number += 1
        check_validity(base_url)
        get_subpages(base_url)

    print("End processing...")

