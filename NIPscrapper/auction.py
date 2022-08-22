import json
from tkinter import Label


class Auction:

    def __init__(self, auction_name, advertiser_name, start_date, end_date, offer_winners, offer_losers, cpv, is_price_criterium, status, conditions):
        self.auction_name = auction_name.replace("\\n", "")
        self.advertiser_name = advertiser_name.replace("\\n", "")
        self.start_date = start_date.replace("\\n", "")
        self.end_date = end_date.replace("\\n", "")
        self.is_price_criterium = is_price_criterium
        self.status = status.replace("Status ogłoszenia: ", "")
        self.conditions = conditions
        self.offer_winners = offer_winners
        self.offer_losers = offer_losers
        self.cpv = cpv

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False)


class Auctions:

    def __init__(self):
        self.auctions = []

    def add_auction(self, other: Auction):
        self.auctions.append(other)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False)