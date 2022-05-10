import config
import constants
import json
from offer import Offer
from auction import Auction, Auctions
from cpv import CPV
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

driver = webdriver.Chrome(config.chrome_driver_path)
sleep_time = 2


def setup_city_configuration():
    driver.execute_script("document.getElementsByClassName('cookies-container')[0].style.display='none'")
    driver.find_elements(by=By.XPATH, value="//button[@class='mdc-button mdc-button--outlined']")[0].click()
    sleep(sleep_time)
    announcement_status = driver.find_elements(by=By.XPATH, value="//input[@class='mdc-checkbox__native-control']")
    announcement_status[0].click()
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


def get_auction_offers(__link__):
    driver.get(__link__)
    sleep(sleep_time)
    offer_list = driver.find_elements(by=By.XPATH, value="//div[@class='offer__list']")
    offer_settlement = offer_list[0].find_elements(by=By.XPATH,
                                                   value="./child::p[@class='text mdc-typography--subtitle2']")
    if "żadnej oferty" in offer_settlement[0].text:
        return None, None
    offer_type_name = offer_list[0].find_elements(by=By.XPATH, value="./child::div[@class='offer-resolve__name']//h2")[0].text
    is_offer_multiple = True if "Rozstrzygnięcie części" in offer_type_name else False

    auction_winners = []
    auction_losers = []

    if is_offer_multiple:
        return None, None
    else:
        offer_win = offer_list[0].find_elements(by=By.XPATH, value="./child::div//div[@class='box__content']//div[@class='field-with-label ']")
        name = offer_win[0].text
        price = offer_win[2].text
        auction_winners.append(Offer(name, price))

        other_offers = offer_list[0].find_elements(by=By.XPATH, value="./child::section[@class='grid-custom ']//li[@class='box box--flexible  mdc-theme--background mdc-elevation--z3']")
        for other_offer in other_offers:
            off = other_offer.find_elements(by=By.XPATH, value="./child::div[@class='box__content']//div[@class='field-with-label ']")
            auction_losers.append(Offer(off[0].text, off[2].text))

        return auction_winners, auction_losers


def get_auction_cpv():
    order_box = driver.find_elements(by=By.XPATH, value="//div[@class='box__content']")[0]
    cpv_box = order_box.find_elements(by=By.XPATH, value="./child::div[@class='field-with-label ']")[2]
    cpv_codes = cpv_box.find_elements(by=By.XPATH, value="./child::p[@class='text mdc-typography--subtitle2']")
    cpv = []

    for code in cpv_codes:
        code_splitted = code.text.split()
        cpv.append(CPV(code_splitted[0], " ".join(code_splitted[1:])))

    return cpv


def get_auction_data(auction_link):
    driver.get(auction_link)
    sleep(sleep_time)
    auction_name = driver.find_elements(by=By.XPATH, value="//h1[@class='text text--main-title long-text mdc-typography--subtitle2']")[0].text
    date_row = driver.find_elements(by=By.XPATH,
                                    value="//section[@class='grid-custom grid-custom--flex-m grid-custom--full-width ']")
    date_container = date_row[0].find_elements(by=By.XPATH,
                                               value="./child::div[@class='field-with-label announcement--date']")
    date = date_container[1].find_element(by=By.XPATH, value="./child::p[@class='text mdc-typography--subtitle2']")
    auction_start_date = date.text
    if len(date.text) >= 10:
        auction_start_date = date.text[:10]

    auction_advertiser_container = driver.find_elements(by=By.XPATH,
                                                        value="//aside[@class='details-preview__part details-preview__part--aside']")
    auction_advertiser_name_container = auction_advertiser_container[0].find_elements(by=By.XPATH,
                                                                                      value="./child::div[@class='field-with-label ']")
    auction_advertiser_name = auction_advertiser_name_container[1].find_elements(by=By.XPATH,
                                                                                 value="./child::p[@class='text mdc-typography--subtitle2']")[
        0].text
    cpv = get_auction_cpv()
    auction_winner, auction_losers = get_auction_offers(auction_link + "?sekcja=oferty")
    if auction_winner is None:
        return None
    return Auction(auction_name, auction_advertiser_name, auction_start_date, auction_winner, auction_losers, cpv)


for city in config.cities_to_scrap:
    # url = constants.BASE_URL_QUERY + city
    # driver.get(url)
    # setup_city_configuration()

    # auctions_links = get_auctions_links()
    auctions = Auctions()

    for link in ["https://bazakonkurencyjnosci.funduszeeuropejskie.gov.pl/ogloszenia/11994"]:
        auction = get_auction_data(link)
        if auction is not None:
            auctions.add_auction(auction)

    with open(f'data/{city}.json', 'w') as f:
        json.dump(json.JSONDecoder().decode(auctions.to_json()), f, ensure_ascii=False, indent=4)

driver.close()
