import constants
import json
import pprint
from offer import Offer
from auction import Auction, Auctions
from cpv import CPV
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from os import listdir
from os.path import isfile, join
from difflib import SequenceMatcher
from selenium import webdriver
import config

driver = webdriver.Chrome(config.path)


cities_to_scrap = [ "Gdansk"]

sleep_time = 2

EU_words = ["unii", "europejskiej", "unię", "europejską",  "europ", "unia", "unią"]




def setup_city_configuration():
    sleep(2*sleep_time)
    driver.execute_script("document.getElementsByClassName('cookies-container')[0].style.display='none'")
    driver.find_elements(by=By.XPATH, value="//button[@class='mdc-button mdc-button--outlined']")[0].click()
    sleep(2*sleep_time)
    announcement_status = driver.find_elements(by=By.XPATH, value="//input[@class='mdc-checkbox__native-control']")
    announcement_status[0].click()
    announcement_status[1].click()
    announcement_status[3].click()
    driver.execute_script(
        "document.getElementsByClassName('mdc-dialog__surface')[0].scrollTo(0, document.body.scrollHeight);")
    driver.find_element(by=By.ID, value="zastosuj_kryteria_wyszukiwania_button_id").click()
    sleep(sleep_time)


def get_links_at_site():
    selenium_links = driver.find_elements(By.XPATH, value="//a[@class='link-text']")
    links = []
    for __link__ in selenium_links:
        anchor = __link__.get_attribute("href")
        if not ("kopia" in __link__.find_element(By.TAG_NAME, value="span").text.lower()):
            links.append(anchor)

    return links


def get_auctions_links():
    __auctions_links__ = get_links_at_site()
    while driver.find_elements(by=By.XPATH, value="//button[@class='mdc-button mdc-button--outlined']")[2].is_enabled():
        driver.find_elements(by=By.XPATH, value="//button[@class='mdc-button mdc-button--outlined']")[2].click()
        sleep(sleep_time)
        __auctions_links__ = __auctions_links__ + get_links_at_site()

    return __auctions_links__



def get_list(offers) -> list:
    list_offer = list()
    for offer in offers:
        if "Odrzucona" in offer.text:
            is_rejected = True
        else: 
            is_rejected = False
        offer_data = offer.find_elements(by=By.XPATH, value="./child::div[@class='field-with-label ']")
        #offer to każda pojedyncza oferta
        name = offer_data[0].text
        price = offer_data[2].text
        list_offer.append(Offer(name, price, is_rejected))   
    return list_offer


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def data_from_EU(description):
    description = description.lower().split()
    for word in EU_words:
        if word in description:
            return True
        for word_descriptin in description:
            if similar(word, word_descriptin) > 0.8:
                return True
    return False


def get_offers_losers(offers) -> list:
    offers_data = offers.find_elements(by=By.XPATH, value=".//div[@class='box__content']")
    #offers_data to wszystkie oferty ktore przyszly
    return get_list(offers_data)

def get_offers_settled(offers):
    offers_data_win = offers.find_elements(by=By.XPATH, value=".//div//div[@class='box__content']")
    try:
        offers_data_lose = offers.find_elements(by=By.XPATH, value=".//section//div[@class='box__content']")
        offers_data_lose_list = get_list(offers_data_lose)
    except Exception:
        offers_data_lose_list = None
    offers_data_win_list =  get_list(offers_data_win)
    return offers_data_win_list, offers_data_lose_list
    

def get_auction_offers(__link__):
    driver.get(__link__)
    sleep(sleep_time)
    offer_list = driver.find_elements(by=By.XPATH, value="//div[@class='offer__list']")
    if len(offer_list) == 0:
        print("No offers")
        return None, None
    offer_winners = list()
    offer_losers = list()
    for offer in offer_list:
        if "żadnej oferty" in offer.text:
            offer_losers = get_offers_losers(offer)
        elif "wybrana oferta" in offer.text or "wybrane oferty" in offer.text:
            offer_winners, offer_losers  = get_offers_settled(offer)
    return offer_winners, offer_losers


def get_auction_cpv():
    order_box = driver.find_elements(by=By.XPATH, value="//div[@class='box__content']")[0]
    cpv_box = order_box.find_elements(by=By.XPATH, value="./child::div[@class='field-with-label ']")[2]
    cpv_codes = cpv_box.find_elements(by=By.XPATH, value="./child::p[@class='text mdc-typography--subtitle2']")
    cpv = []

    if len(cpv_codes) == 0:
        cpv_codes = cpv_box.find_elements(by=By.XPATH, value="//div[contains(string(), 'Kody CPV')]/p[2]")
    

    for code in cpv_codes:
        code_splitted = code.text.split()
        cpv.append(CPV(code_splitted[0], " ".join(code_splitted[1:])))

    return cpv


def get_auction_conditions():
    announcement = driver.find_elements(by=By.XPATH, value="//li[@class='announcement__part']")[0]
    condition_box = announcement.find_elements(by=By.XPATH, value="./child::ul//li[@class='box box--long-content  mdc-theme--background mdc-elevation--z3']//div[@class='box__content']//div[@class='separate-content']")
    conditions = []
    for condition_element in condition_box:
        condition_description = condition_element.find_elements(by=By.XPATH, value="./child::div[@class='field-with-label ']")[1]
        text = condition_description.find_elements(by=By.XPATH, value="./child::p[@class='text long-text mdc-typography--subtitle2']")[0].text
        conditions.append(text.replace("\\n", ""))

    return conditions


def get_price_criterium():
    criteria = driver.find_elements(by=By.XPATH, value="//li[@class='box  mdc-theme--background mdc-elevation--z3']")[0]
    box_criteria = criteria.find_elements(by=By.XPATH, value="./child::div[@class='box__content']")[0]
    is_price_text = box_criteria.find_elements(by=By.XPATH, value="./child::p[@class='text mdc-typography--subtitle2']")[0].text
    return is_price_text == "TAK"


def get_auction_data(auction_link):
    driver.get(auction_link)
    sleep(5*sleep_time)
    auction_name = driver.find_elements(by=By.XPATH, value="//h1[@class='text text--main-title long-text mdc-typography--subtitle2']")[0].text
    auction_status = driver.find_elements(by=By.XPATH, value="//h2[@class='text mdc-typography--subtitle2']")[0].text
    date_row = driver.find_elements(by=By.XPATH,
                                    value="//section[@class='grid-custom grid-custom--flex-m grid-custom--full-width ']")
    date_container = date_row[0].find_elements(by=By.XPATH,
                                               value="./child::div[@class='field-with-label announcement--date']")
    end_date = date_container[0].find_element(by=By.XPATH, value="./child::p[@class='text mdc-typography--subtitle2']")
    start_date = date_container[1].find_element(by=By.XPATH, value="./child::p[@class='text mdc-typography--subtitle2']")
    auction_end_date = end_date.text
    auction_start_date = start_date.text
    auction_EU = data_from_EU(auction_name)
    if not auction_EU:
        description_box = driver.find_elements(By.XPATH, '//div[@class="box__content"]//p[contains(string(), "Opis")]')
        for description in description_box:
            description_text = description.find_element(By.XPATH, '..').text
            auction_EU = data_from_EU(description_text)
            if auction_EU:
                break 
    if len(auction_start_date) >= 10:
        auction_start_date = start_date.text[:10]

    if len(auction_end_date) >= 10:
        auction_end_date = end_date.text[:10]

    auction_advertiser_container = driver.find_elements(by=By.XPATH,
                                                        value="//aside[@class='details-preview__part details-preview__part--aside']")
    auction_advertiser_name_container = auction_advertiser_container[0].find_elements(by=By.XPATH,
                                                                                      value="./child::div[@class='field-with-label ']")
    auction_advertiser_name = auction_advertiser_name_container[1].find_elements(by=By.XPATH,
                                                                                 value="./child::p[@class='text mdc-typography--subtitle2']")[
        0].text
    cpv = get_auction_cpv()
    conditions = get_auction_conditions()
    is_price_criterium = get_price_criterium()
    auction_winner, auction_losers = get_auction_offers(auction_link + "?sekcja=oferty")
    if auction_winner is None:
        auction_winner = []
    if auction_losers is None:
        auction_losers = []
    return Auction(auction_name,
                   auction_advertiser_name,
                   auction_start_date,
                   auction_end_date,
                   auction_winner,
                   auction_losers,
                   cpv,
                   is_price_criterium,
                   auction_status,
                   conditions, 
                   auction_EU)


def get_last_done_chunk(city_name):
    onlyfiles = [f for f in listdir(config.path_to_data) if isfile(join(config.path_to_data, f))]
    last_file = onlyfiles[-1]
    try:
        last_file_index = last_file.split(city_name, 1)[1].split('.json', 1)[0]
    except Exception:
        last_file_index = 0
    return last_file_index


for city in cities_to_scrap:
    last_saved_file = get_last_done_chunk(city)
    url = constants.BASE_URL_QUERY + city
    driver.get(url)
    setup_city_configuration()
    auctions_links = get_auctions_links()
    auctions = Auctions()
    auction_links_chunks = [auctions_links[x:x+100] for x in range(0, len(auctions_links), 100)]

    for index, links_chunk in enumerate(auction_links_chunks):
        if index <= int(last_saved_file):
            continue
        print(index)
        for link in links_chunk:
            auction = get_auction_data(link)
            if auction is not None:
                auctions.add_auction(auction)
        with open(f'data/{city}{index}.json', 'w', encoding='utf-8') as f:
            json.dump(json.JSONDecoder().decode(auctions.to_json()), f, ensure_ascii=False, indent=4)

driver.close()
