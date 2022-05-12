import json
import csv

from APIservice import APIService


class Data:
    def __init__(self, id_tender=None, open_date=None, title=None, awarded_value=None, awarded_date=None,
                 suppliers=None,
                 offers_count=None):
        self.id = id_tender
        self.open_date = open_date
        self.title = title
        self.awarded_value = awarded_value
        self.awarded_date = awarded_date
        self.suppliers = suppliers
        self.offers_count = offers_count
        self.ddl_date = ''
        self.ended = False
        self.cpv = None

    def __str__(self):
        info = f"id {self.id}, data rozpoczęcia: {self.open_date},  {self.title}"
        if self.awarded_date:
            info += f" {self.awarded_date}, {self.awarded_value}, {self.suppliers}, {self.offers_count}, {self.ended}"
        return info

    def obj_to_json(self):
        dict = {
            "id": self.id,
            "title": self.title,
            "open_date": self.open_date,
            "awarded_value": self.awarded_value,
            "awarded_date": self.awarded_date,
            "suppliers": self.suppliers,
            "offers_count": self.offers_count,
            "ended": self.ended,
            "ddl_date": self.ddl_date,
            "cpv": self.cpv
        }
        try:
            return json.dumps(dict)
        except:
            raise Exception("Error with JSON")


class DataSet:
    def __init__(self, api: APIService, miasto):
        self.api = api
        self.miasto = miasto
        self.file = f'{miasto}1.json'
        self.dataSet = set()
        self.JsonSet = set()

    def make_dataset(self):
        data = self.api.get_data()
        while self.api.is_page_avaible():
            for datum in data:
                tmp_data = Data(datum['id'], datum['date'], datum['title'])
                try:
                    tmp_data.awarded_value = datum['awarded_value']
                    tmp_data.awarded_date = datum['awarded'][0]['date']
                    tmp_data.suppliers = datum['awarded'][0]['suppliers_name']
                    tmp_data.offers_count = datum['awarded'][0]['offers_count'][0]
                    tmp_data.ddl_date = datum['deadline_length_days']
                except:
                    pass
                if tmp_data.awarded_date:
                    tmp_data.ended = True
                self.dataSet.add(tmp_data)
            self.api.get_next_page()

    def open_CSV_from_scrapper(self):
        with open(f"CSVfromScrapper\{self.miasto}.csv", 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                if len(row) == 0:
                    continue
                for data in self.dataSet:
                    if data.id == row[0] and self.miasto == row[2].lower():
                        data.cpv = row[1]
                        self.JsonSet.add(data)

    def save_to_JSON(self):
        with open(f"{self.file}", 'w') as file:
            file.write('{ "data":[')
            for data in self.JsonSet:
                file.write(data.obj_to_json())
                file.write(',')
            file.write(']}')
