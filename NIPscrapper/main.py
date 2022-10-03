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
    phone_number = get_phone_number(phone_block_div)

    address_block_div = basic_data_section.find("div", {"class" : "address"})
    postal_code, city_name = None, None
    postal_code, city_name = get_postal_code_and_city_name(address_block_div)

    register_data_section = soup2.find("section", {"id" : "company-registry-data-section"})
    all_divs = register_data_section.find_all("div", {"class": "registry-details__row"})

    krs_number, legal_form, nip_number, owner_name, regon_number = None, None, None, None, None
    for single_div in all_divs:
        krs_number, legal_form, nip_number, owner_name, regon_number = get_company_official_details(krs_number, legal_form, nip_number, owner_name, regon_number, single_div)

    procuration_members, board_members_array, supervisory_board = [], [], []

    company_authorities_section = soup2.find("section", {"id": "company-authorities-section"})
    get_board_members(company_authorities_section, board_members_array)
    stock_company_divs = soup2.find_all("div", {"class":"flex flex-wrap w-full ng-star-inserted"})

    for stock_company_div in stock_company_divs:
        get_procuration_members(company_authorities_section, procuration_members, stock_company_div)
        get_supervisory_board(company_authorities_section, stock_company_div, supervisory_board)

    company = Company(company_name, nip_number, owner_name, city_name, postal_code, phone_number, krs_number, regon_number, legal_form, board_members_array, procuration_members, supervisory_board)
    return company


def get_company_official_details(krs_number, legal_form, nip_number, owner_name, regon_number, single_div):
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
    return krs_number, legal_form, nip_number, owner_name, regon_number


def get_supervisory_board(company_authorities_section, stock_company_div, supervisory_board):
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
    return


def get_procuration_members(company_authorities_section, procuration_members, stock_company_div):
    if "PROKURA" in stock_company_div.text:
        print("Prokura")
        new_member = ""
        board_members_names = company_authorities_section.find("div", {"class": "authority-name"})
        for member in board_members_names:
            if member.text != "" and not member.text.startswith(" "):
                new_member = member.text
            elif member.text.startswith(" "):
                new_member += member.text
                print(new_member)
                procuration_members.append(new_member)
                new_member = ""
    return

def get_board_members(company_authorities_section, board_members_array):
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
    return


def get_phone_number(phone_block_div):
    if phone_block_div is not None:
        phone_number = phone_block_div.find("span").text
        print("Phone number : " + phone_number)
    else:
        phone_number = None
    return phone_number


def get_postal_code_and_city_name(address_block_div):
    if address_block_div is not None:
        address = address_block_div.find("div", {"class":"address-data"}).text
        elements = address.split(" ")
        postal_code = elements[len(elements) - 2]
        city_name = elements[len(elements) - 1]
        print("Postal code : " + postal_code)
        print("City name : " + city_name)
        return postal_code, city_name
    else:
        return None, None


def check_auction_attender(attenders):
    companies = []
    if len(attenders) > 0:
        for offer_attender in attenders:
            hdr = {'User-Agent': 'Mozilla/5.0'}
            new_link = START_LINK + replace_polish_characters(offer_attender.name).replace(' ', '+') + END_LINK
            to_path = encode_decode_request_path(new_link)
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
                to_path = encode_decode_request_path(detail_page_link)
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

def check_single_auction_attender(attender_name):

    attender_name_string = str(attender_name)
    hdr = {'User-Agent': 'Mozilla/5.0'}
    new_link = START_LINK + replace_polish_characters(attender_name_string).replace(' ', '+') + END_LINK
    to_path = encode_decode_request_path(new_link)
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
        to_path = encode_decode_request_path(detail_page_link)
        req = Request(to_path, headers=hdr)

        exception = False

        try:
            urlopen(req).getcode()
        except Exception as e:
            print(e)
            exception = True

        if not exception:
            return open_detail_page(req)

    return None


def encode_decode_request_path(new_link):
    tmp = new_link.encode('utf-8')
    to_path = tmp.decode("utf-8")
    return to_path


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


def createComapniesListFromCity():
    city_names = ["Grudziądz", "Lubawa", "Mława", "Łomża"]
    fetched_comapnies_list = set()
    firstBoundary = 1
    secondBoundary = -1
    for city_name in city_names:
        if city_name == "Grudziądz":
            secondBoundary = 15
        elif city_name == "Lubawa":
            secondBoundary = 3
        elif city_name == "Mława":
            secondBoundary = 1
        elif city_name == "Łomża":
            secondBoundary = 15

        for iterator in range (firstBoundary, secondBoundary + 1):
            start = "D:\inzynierka_wakajki\scrapery\FDS-Dataset\BazaKonkurencyjnosciScrapper\data\\" + str(city_name)
            end = ".json"
            file_path = start + str(iterator) + end
            companies = Companies()
            with open(file_path, 'rb') as f:
                file_text = json.load(f)
                for singleAuction in file_text['auctions']:

                    dictInString = json.dumps(singleAuction)
                    # Parse JSON into an object with attributes corresponding to dict keys.
                    x = json.loads(dictInString, object_hook=lambda d: SimpleNamespace(**d))

                    for loser_company in x.offer_losers:
                        fetched_comapnies_list.add(loser_company.name)

                    for winning_company in x.offer_winners:
                        fetched_comapnies_list.add(winning_company.name)

    with open(f'OutputData/CompaniesList.txt', 'a') as f:
        for company_name in fetched_comapnies_list:
            f.write(company_name + '\n')

    return 1


if __name__ == '__main__':
    print("Start processing...")
    createComapniesListFromCity()

    print("Companies list is fetched")
    companies = Companies()
    with open(f'OutputData/CompaniesList.txt', 'rb') as f:
        companies_from_file = f.readlines()

        for company_name_from_file in companies_from_file:
            company_to_add = check_single_auction_attender(company_name_from_file)
            if company_to_add is not None:
                companies.add_company(company_to_add)

        with open(f'OutputData/Companies3.json', 'w', encoding='utf8') as f:
            json.dump(json.JSONDecoder().decode(companies.to_json()), f, ensure_ascii=False, indent=4)

    createComapniesListFromCity()
    print("End processing...")