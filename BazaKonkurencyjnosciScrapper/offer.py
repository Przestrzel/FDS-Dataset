import json


class Offer:

    def __init__(self, name, price):
        self.name = Offer.extract_name(name)
        self.price = Offer.extract_price(price)

    @staticmethod
    def extract_name(name: str):
        name = name.replace("Nazwa podmiotu", "")
        name = name.replace("\n", "")
        return name

    @staticmethod
    def extract_price(price: str):
        price = price.replace("Cena", "")
        price = price.replace(",", ".")
        price = price.replace("\n", "")
        return price
