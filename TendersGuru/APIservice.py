import requests
import json
import sys


class APIService:
    __API_URL = 'https://tenders.guru/api/pl/'

    def __init__(self, data, parameter=None):
        self.__data = data
        self.__parameter = parameter
        self.__query = (self.__API_URL
                        + self.__data
                        + self.__query_params() # usually city
                        + 'per_page=100')
        self.__page = 1
        self.request = requests.get(self.__query)

    def __query_params(self):
        if self.__data == "tenders":
            return ("?q="
                    + str(self.__parameter)
                    + "&")
        elif self.__data == "notices":
            return ("error")

    def __check_next_page(self):
        try:
            meta = self.get_meta()
            self.__page = json.loads(meta).get('next_page')
        except json.JSONDecodeError:
            print("Please try later, the API isn't working")
            print("Error with loads metadata")
            sys.exit()

    def get_data(self):
        try:
            self.__data = json.dumps(self.request.json()['data'])
            return json.loads(self.__data)
        except json.JSONDecodeError:
            print("Please try later, the API isn't working")
            print("Error with loads data")
            sys.exit()

    def get_next_page(self):
        self.__check_next_page()
        self.request = requests.get(self.__query + "&page=" + str(self.__page))

    def get_meta(self):
        try:
            meta = json.dumps(self.request.json()['meta'])
            return meta
        except json.JSONDecodeError:
            print("Please try later, the API isn't working")
            print("Error with loads metadata")
            sys.exit()

    def get_query(self):
        return self.__query

    def is_page_avaible(self):
        if self.__page is not None:
            return True
        else:
            return False