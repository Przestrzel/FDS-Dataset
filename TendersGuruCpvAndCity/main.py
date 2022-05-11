import csv

from selenium import webdriver

import config_file
import constants
from selenium.webdriver.common.by import By

from time import sleep
from os import listdir

from ProcurementModel import ProcurementModel

driver = webdriver.Chrome(config_file.chrome_driver_path)


def get_filenames():
    filenames = []
    all_files = listdir(".\\csv")
    for file in all_files:
        filenames.append(file)
        print(file)
    return filenames


def read_data_from_csv(file_name):
    rows = []
    path = ".\\csv\\" + file_name
    print(file_name)
    with open(path) as f:
        lines = (line.rstrip() for line in f)  # All lines including the blank ones
        lines = (line for line in lines if line)  # Non-blank lines
        for row in lines:
            rows.append(row)
    return rows


def click_procurement_details(procurement_id):
    buttons_div = driver.find_element(by=By.CLASS_NAME, value="timeline")
    buttons_to_click = buttons_div.find_elements(by=By.CLASS_NAME, value="btn")

    contracting_city = ""
    cpv_code = ""
    for button_to_click in buttons_to_click:
        # button_to_click.click()
        # driver.execute_script("arguments[0].click();", button_to_click)
        webdriver.ActionChains(driver).move_to_element(button_to_click).click(button_to_click).perform()
        sleep(3)

        cpv_field = driver.find_elements(by=By.XPATH, value="//p[contains(text(), 'cpv_glowny_przedmiot')]")
        contracting_city_field = driver.find_elements(by=By.XPATH, value="//p[contains(text(), 'zamawiajacy_miejscowosc')]")

        if len(contracting_city_field) > 0:
            div_parent = contracting_city_field[0].find_element(by=By.XPATH, value='..')
            contracting_city_correct = div_parent.find_elements(by=By.TAG_NAME, value="p")
            contracting_city = contracting_city_correct[1].text

        if len(cpv_field) > 0:
            div_parent = cpv_field[0].find_element(by=By.XPATH, value='..')
            cpv_code_correct = div_parent.find_elements(by=By.TAG_NAME, value="p")
            cpv_code = cpv_code_correct[1].text

        new_procurement = ProcurementModel(procurement_id, cpv_code, contracting_city)
        return new_procurement


if __name__ == '__main__':
    file_names = get_filenames()
    procurements = []
    for file_name in file_names:
        procurements_ids = read_data_from_csv(file_name)
        procurements = []
        for procurement_id in procurements_ids:
            url = constants.BASE_TENDERS_GURU_PATH + procurement_id
            driver.get(url)
            new_procurement = click_procurement_details(procurement_id)
            procurements.append(new_procurement)
            print(new_procurement.id + " - " + new_procurement.cpv + " - " + new_procurement.city)
        with open("1grudziadz.csv", "w") as file:
            writer = csv.writer(file, delimiter=";")
            for line in procurements:
                writer.writerow([str(line.id), line.cpv, line.city])
        file.close()
    driver.close()

