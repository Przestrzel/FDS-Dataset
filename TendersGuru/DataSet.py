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
        self.ended = False

    def __str__(self):
        info = f"id {self.id}, data rozpoczęcia: {self.open_date},  {self.title}"
        if self.awarded_date:
            info += f" {self.awarded_date}, {self.awarded_value}, {self.suppliers}, {self.offers_count}, {self.ended}"
        return info


class DataSet:
    def __init__(self, api: APIService):
        self.api = api

    def make_dataset(self):
        data = self.api.get_data()
        dataset= set()
        for datum in data:
            tmp_data = Data(datum['id'], datum['date'], datum['title'])
            try:
                tmp_data.awarded_value = datum['awarded_value']
                tmp_data.awarded_date = datum['awarded'][0]['date']
                tmp_data.suppliers = datum['awarded'][0]['suppliers_name']
                tmp_data.offers_count = datum['awarded'][0]['offers_count'][0]
            except:
                pass
            if tmp_data.awarded_date:
                tmp_data.ended = True
            dataset.add(tmp_data)
        for obj in dataset:
            print(obj)
