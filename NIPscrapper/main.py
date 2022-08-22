import json
from types import SimpleNamespace

from urllib.request import urlopen, Request

from bs4 import BeautifulSoup

from NIPscrapper.company import Company, Companies

START_LINK = 'https://aleo.com/pl/firmy?phrase='
END_LINK = '&showAuthorityPlate=true'


def check_validity(my_url):
    try:
        urlopen(my_url)
        print("Valid URL")
    # except IOError as e:
    #     print(e)
    #     print("Invalid URL")
    except:
        pass
        #sys.exit()


def get_field_by_name(raw_text, name):
    if name in raw_text:
        result = raw_text[len(name):]
        return result
    return None


def check_existing_result(my_url):
    tmp_html = urlopen(my_url)
    if tmp_html.getcode() != 404:
        html = tmp_html.read()
        soup = BeautifulSoup(html, features="html.parser")
        table = soup.find("div", {"class": "bg-white shadow-custom ng-star-inserted"})
        if table is None:
            print("Table not exist")
            return False
        print("Table exist")
        return True
    return False


def open_detail_page(my_url):
    html2 = urlopen(my_url).read()
    soup2 = BeautifulSoup(html2, features="html.parser")
    basic_data_section = soup2.find("section", {"id": "company-info-section"})
    company_name_div = basic_data_section.find("span", {"class": "text-company-name font-semibold lg:company-name lg:font-normal"})
    company_name = company_name_div.text
    print("Company name : " + company_name)

    phone_block_div = basic_data_section.find("div", {"class" : "phone "})
    if phone_block_div is not None:
        phone_number = phone_block_div.find("span").text
        print("Phone number : " + phone_number)
    else:
        phone_number = None

    register_data_section = soup2.find("section", {"id" : "company-registry-data-section"})
    all_divs = register_data_section.find_all("div", {"class": "registry-details__row"})

    nip_number = None
    owner_name = None
    krs_number = None
    regon_number = None
    legal_form = None
    for single_div in all_divs:
        if nip_number is None and get_field_by_name(single_div.text, "NIP ") is not None:
            nip_number = get_field_by_name(single_div.text, "NIP ")
            print("Nip number : " + nip_number)
        if owner_name is None and get_field_by_name(single_div.text, "Przedsiębiorca ") is not None:
            owner_name = get_field_by_name(single_div.text, "Przedsiębiorca ")
            print("Owner name : " + owner_name)
        if krs_number is None and get_field_by_name(single_div.text, "KRS ") is not None:
            krs_number = get_field_by_name(single_div.text, "KRS ")
            print("KRS number : " + krs_number)
        if regon_number is None and get_field_by_name(single_div.text, "REGON ") is not None:
            regon_number = get_field_by_name(single_div.text, "REGON ")
            print("REGON number : " + regon_number)
        if legal_form is None and get_field_by_name(single_div.text, "Forma prawna ") is not None:
            legal_form = get_field_by_name(single_div.text, "Forma prawna ")
            print("Legal form : " + legal_form)

    procuration_members = []
    board_members_array = []
    supervisory_board = []

    company_authorities_section = soup2.find("section", {"id": "company-authorities-section"})
    if company_authorities_section is not None:
        board_members = company_authorities_section.find("div", {"class": "board-members"})

        if board_members is not None:
            print("Czlonkowie zarzadu")
            board_members_names = board_members.find("div", {"class": "authority-name"})
            for member in board_members_names:
                if member.text != "" and not member.text.startswith(" "):
                    new_member = member.text
                elif member.text.startswith(" "):
                    new_member += member.text
                    print(new_member)
                    board_members_array.append(new_member)
                    new_member = ""

    stock_company_divs = soup2.find_all("div", {"class":"flex flex-wrap w-full ng-star-inserted"})
    for stock_company_div in stock_company_divs:

        if "PROKURA" in stock_company_div.text:
            print("Prokura")
            board_members_names = company_authorities_section.find("div", {"class": "authority-name"})
            for member in board_members_names:
                if member.text != "" and not member.text.startswith(" "):
                    new_member = member.text
                elif member.text.startswith(" "):
                    new_member += member.text
                    print(new_member)
                    procuration_members.append(new_member)
                    new_member = ""

        if " RADA NADZORCZA " in stock_company_div.text:
            print("Rada nadzorcza")
            board_members_names = company_authorities_section.find("div", {"class": "authority-name ng-star-inserted"})
            new_member = ""
            for member in board_members_names:
                if member.text != "" and not member.text.startswith(" "):
                    new_member = member.text
                elif member.text.startswith(" "):
                    new_member += member.text
                    print(new_member)
                    supervisory_board.append(new_member)
                    new_member = ""
    company = Company(company_name, nip_number, owner_name, phone_number, krs_number, regon_number, legal_form, board_members_array, procuration_members, supervisory_board)
    return company


def check_auction_attender(attenders):
    companies = []
    if len(attenders) > 0:
        for offer_attender in attenders:
            hdr = {'User-Agent': 'Mozilla/5.0'}
            new_link = START_LINK + replace_polish_characters(offer_attender.name).replace(' ', '+') + END_LINK
            tmp = new_link.encode('utf-8')
            to_path = tmp.decode("utf-8")
            req = Request(to_path, headers=hdr)
            print(new_link)

            check_validity(req)

            results_exist = check_existing_result(req)
            if results_exist:
                html = urlopen(req).read()
                soup = BeautifulSoup(html, features="html.parser")
                table = soup.find("div", {"class": "bg-white shadow-custom ng-star-inserted"})
                header = table.find("div", {"class": "catalog-row-container"})
                new_link = header.find('a', href=True)

                link_start = "https://aleo.com/pl/"
                detail_page_link = link_start + new_link['href']
                hdr = {'User-Agent': 'Mozilla/5.0'}
                tmp = detail_page_link.encode('utf-8')
                to_path = tmp.decode("utf-8")

                req = Request(to_path, headers=hdr)

                exception = False

                try:
                    urlopen(req).getcode()
                except Exception as e:
                    print(e)
                    exception = True

                if not exception :
                    company = open_detail_page(req)
                    companies.append(company)
    return companies


def replace_polish_characters(base_text):
    return_text = base_text.replace("ą", "a")\
        .replace("ę", "e")\
        .replace("ó", "o")\
        .replace("ł", "l")\
        .replace("ś", "s")\
        .replace("ć", "c")\
        .replace("ż", "z")\
        .replace("ź", "z")\
        .replace("ń", "n")\
        .replace("Ą", "A")\
        .replace("Ę", "E")\
        .replace("Ó", "O")\
        .replace("Ł", "L")\
        .replace("Ś", "S")\
        .replace("Ć", "C")\
        .replace("Ż", "Z")\
        .replace("Ź", "Z")\
        .replace("Ń", "N")\
        .replace("“", '"')\
        .replace("”", '"')\
        .replace("„", '"')

    return return_text


if __name__ == '__main__':
    print("Start processing...")
    # tmp = "https://aleo.com/pl/firmy?phrase=Platfroma+Filtrowentylacyjna+Sp+z.o.o.&showAuthorityPlate=true"
    #
    # hdr = {'User-Agent': 'Mozilla/5.0'}
    # req = Request(tmp, headers=hdr)
    #
    # html = urlopen(req).read()
    # soup = BeautifulSoup(html, features="html.parser")
    # table = soup.find("div", {"class": "bg-white shadow-custom ng-star-inserted"})
    # header = table.find("div", {"class": "catalog-row-container"})
    # new_link = header.find('a', href=True)
    #
    # link_start = "https://aleo.com/pl/"
    # detail_page_link = link_start + new_link['href']
    # hdr = {'User-Agent': 'Mozilla/5.0'}
    # tmp = detail_page_link.encode('utf-8')
    # to_path = tmp.decode("utf-8")
    #
    # req = Request(to_path, headers=hdr)
    # print("Before 404 check")
    # try:
    #     urlopen(req).getcode()
    # except Exception as e:
    #     code = 404
    # print("After 404 check")
    # company = open_detail_page(req)
    # companies.append(company)

    for iterator in range(7, 16): #nie jest brany pod uwage na razie ten json bez indexu liczbowego
        start = "D:\inzynierka_wakajki\scrapery\FDS-Dataset\BazaKonkurencyjnosciScrapper\data\Łomża"
        end = ".json"
        file_path = start + str(iterator) + end
        companies = Companies()
        with open(file_path, 'rb') as f:
            file_text = json.load(f)
            for singleAuction in file_text['auctions']:
                dictInString = json.dumps(singleAuction)
                # Parse JSON into an object with attributes corresponding to dict keys.
                x = json.loads(dictInString, object_hook=lambda d: SimpleNamespace(**d))
                losers_companies = check_auction_attender(x.offer_losers)
                winning_companies = check_auction_attender(x.offer_winners)
                companies.add_companies(losers_companies)
                companies.add_companies(winning_companies)

        with open(f'OutputData/Łomża' + str(iterator) + '.json', 'w') as f:
            json.dump(json.JSONDecoder().decode(companies.to_json()), f, ensure_ascii=False, indent=4)

    print("End processing...")