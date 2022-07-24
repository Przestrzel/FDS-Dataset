import os
import sys

from urllib.request import urlopen

from bs4 import BeautifulSoup


def init_links():
    main_links = list([])
    main_links.append('https://aleo.com/pl/firmy?phrase=LEMFAX+PHU+Joanna+Godlewska&showAuthorityPlate=true')
    return main_links


def check_validity(my_url):
    try:
        urlopen(my_url)
        print("Valid URL")
    except IOError:
        print("Invalid URL")
        sys.exit()


def get_nip(my_url):
    html = urlopen(my_url).read()
    soup = BeautifulSoup(html, features="html.parser")
    subpages_div = soup.find("div", {"class": "company_tax_identifier"})
    nip = subpages_div.find('strong')
    print(nip)


if __name__ == '__main__':
    print("Start processing...")
    links = init_links()

    for base_url in links:
        print(base_url)
        check_validity(base_url)
        get_nip(base_url)

    print("End processing...")

