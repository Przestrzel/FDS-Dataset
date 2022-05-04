import os
import sys

import requests
from urllib.request import urlopen

from bs4 import BeautifulSoup

from SubpageModel import SubpageModel


def init_links():
    main_links = list([])
    # zamowienia publiczne
    main_links.append(SubpageModel('http://lubawa.bip-wm.pl/public/?id=161081', "zamPubliczne2020"))  # 2020
    main_links.append(SubpageModel('http://lubawa.bip-wm.pl/public/?id=151929', "zamPubliczne2019"))  # 2019
    main_links.append(SubpageModel('http://lubawa.bip-wm.pl/public/?id=142502', "zamPubliczne2018"))  # 2018
    main_links.append(SubpageModel('http://lubawa.bip-wm.pl/public/?id=136535', "zamPubliczne2017"))  # 2017
    main_links.append(SubpageModel('http://lubawa.bip-wm.pl/public/?id=129558', "zamPubliczne2016"))  # 2016
    # postepowania do 30 k euro
    main_links.append(SubpageModel('http://lubawa.bip-wm.pl/public/?id=163790', "postepowaniado30kEur2020"))  # 2020
    main_links.append(SubpageModel('http://lubawa.bip-wm.pl/public/?id=152697', "postepowaniado30kEur2019"))  # 2019
    main_links.append(SubpageModel('http://lubawa.bip-wm.pl/public/?id=142503', "postepowaniado30kEur2018"))  # 2018
    main_links.append(SubpageModel('http://lubawa.bip-wm.pl/public/?id=136619', "postepowaniado30kEur2017"))  # 2017
    main_links.append(SubpageModel('http://lubawa.bip-wm.pl/public/?id=136619', "postepowaniado30kEur2016"))  # 2016
    # postepowanie do 130 k pln
    main_links.append(SubpageModel('http://lubawa.bip-wm.pl/public/?id=172015', "postepowaniado130kPLN2021"))  # 2021
    return main_links


def check_validity(my_url):
    try:
        urlopen(my_url)
        print("Valid URL")
    except IOError:
        print("Invalid URL")
        sys.exit()


def get_subpages(subpage_url, main_category):
    html = urlopen(subpage_url).read()
    soup = BeautifulSoup(html)
    subpages_div = soup.find("div", {"class" : "td_content podkategoria"})
    procurements_links = list([])
    subpages_links = subpages_div.find_all("a")
    subpage_iterator = 0
    for subpage_link in subpages_links:
        if subpage_link.get('href').find("get_file") == -1:
            subpage_iterator += 1
            new_subpage_url = "http://lubawa.bip-wm.pl/public/" + subpage_link.get('href')
            print(new_subpage_url)
            procurements_links.append(new_subpage_url)
            check_validity(new_subpage_url)
            print(len(str(subpage_link.text)))
            max_length = 150
            if len(str(subpage_link.text)) > max_length:
                investition_name = str(subpage_link.text)[0:max_length]
            else:
                investition_name = str(subpage_link.text)
            if not os.path.isfile("./" + str(main_category) + "/" + investition_name.rstrip().replace("\"", "")):
                os.makedirs("./" + str(main_category) + "/" + investition_name.rstrip().replace("\"", ""), exist_ok=True)

            get_pdfs(new_subpage_url, investition_name.rstrip().replace("\"", ""), main_category) #zmiana
    print("All subpages founds")
    return procurements_links


def get_pdfs(my_url, subpage_title, main_category):
    html = urlopen(my_url).read()
    soup = BeautifulSoup(html)
    iterator = 0
    for link in soup.find_all("a"):
        if link.text.endswith('pdf') and link.get('href').startswith('http'):
            iterator += 1
            print("Downloading file: ", iterator)

            response = requests.get(link.get('href'))
            # os.makedirs("./" + str(main_category) + "/" + str(subpage_title), exist_ok=True)
            pdf = open("./" + str(main_category) + "/" + str(subpage_title) + "/" + link.text, 'wb')
            pdf.write(response.content)
            pdf.close()

            print("File ", iterator, " downloaded")

    print("All PDF files downloaded")


if __name__ == '__main__':
    print("Start processing...")
    links = init_links()
    number = 1

    for subpage in links:
        print("Web page number ", number)
        number += 1
        check_validity(subpage.url)
        os.makedirs("./" + str(subpage.title), exist_ok=True)
        get_subpages(subpage.url, subpage.title)

    print("End processing...")
