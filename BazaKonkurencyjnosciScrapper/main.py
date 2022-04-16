import config
import constants
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

driver = webdriver.Chrome(config.chrome_driver_path)


def setup_city_configuration():
    driver.execute_script("document.getElementsByClassName('cookies-container')[0].style.display='none'")
    driver.find_elements(by=By.XPATH, value="//button[@class='mdc-button mdc-button--outlined']")[0].click()
    sleep(0.5)
    announcement_status = driver.find_elements(by=By.XPATH, value="//input[@class='mdc-checkbox__native-control']")
    announcement_status[0].click()
    announcement_status[1].click()
    announcement_status[3].click()
    driver.execute_script(
        "document.getElementsByClassName('mdc-dialog__surface')[0].scrollTo(0, document.body.scrollHeight);")
    driver.find_element(by=By.ID, value="zastosuj_kryteria_wyszukiwania_button_id").click()
    sleep(0.5)


def get_links_at_site():
    selenium_links = driver.find_elements(By.XPATH, value="//a[@class='link-text']")
    links = []
    for link in selenium_links:
        normal_link = link.get_attribute("href")
        links.append(normal_link)

    return links


def get_auctions_links():
    __auctions_links__ = get_links_at_site()
    while driver.find_elements(by=By.XPATH, value="//button[@class='mdc-button mdc-button--outlined']")[2].is_enabled():
        driver.find_elements(by=By.XPATH, value="//button[@class='mdc-button mdc-button--outlined']")[2].click()
        sleep(0.5)
        __auctions_links__ = __auctions_links__ + get_links_at_site()

    return __auctions_links__


for city in config.cities_to_scrap:
    url = constants.BASE_URL_QUERY + city
    driver.get(url)
    setup_city_configuration()

    auctions_links = get_auctions_links()
    print(auctions_links)

# driver.close()
