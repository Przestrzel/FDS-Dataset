from APIservice import APIService


class Data:
    def __init__(self, id_tender=None, open_date=None, title=None, awarded_value=None, awarded_date=None,
                 suppliers=None,
                 offers_count=None):
        self.id = id
        self.open_date = open_date
        self.title = title
        self.awarded_value = awarded_value
        self.awarded_date = awarded_date
        self.suppliers = suppliers
        self.offers_count = offers_count


class DataSet:
    def __init__(self, api: APIService):
        self.api = api

    def make_dataset(self):
        data = self.api.get_data()
        for datum in data:
            tmp_data = Data(datum['id'], datum['date'], datum['title'], datum['awarded_value'])
            try:
                tmp_data.awarded_date = datum['awarded'][0]['date']
                tmp_data.suppliers = datum['awarded'][0]['suppliers_name']
                tmp_data.offers_count = datum['awarded'][0]['offers_count'][0]
            except:
                pass
            break
