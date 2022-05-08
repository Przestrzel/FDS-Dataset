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
            "ddl_date": self.ddl_date
        }
        try:
            return json.dumps(dict)
        except:
            raise Exception("Error with JSON")




class DataSet:
    def __init__(self, api: APIService, miasto):
        self.api = api
        self.miasto = miasto
        self.file = f'{miasto}.json'

    def make_dataset(self):
        data = self.api.get_data()
        dataset =set()
        with open(self.file, 'w') as file:
            file.write('{ "data":[')
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
                    dataset.add(tmp_data)
                    file.write(tmp_data.obj_to_json())
                    file.write(',')
                self.api.get_next_page()
            file.write(']}')
        with open(f'CSV\{self.miasto}.csv', 'w') as file:
            writer = csv.writer(file, delimiter=',')
            for tmp in dataset:
                writer.writerow([tmp.id])