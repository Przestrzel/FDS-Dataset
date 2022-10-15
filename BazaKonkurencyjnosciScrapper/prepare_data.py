from os import listdir
from os.path import isfile, join
import config
import json
import re

all_auctions = []
all_companies_index = []
all_companies_offers = []
set_companies = set()

index_auction = 0
index_companies = 0
AUCTION_PER_FILE = 100

def return_id_company(name):
    for company in all_companies_index:
        if company['name'] == name:
            return company['id']


def get_files():
    onlyfiles = [f for f in listdir(config.path_to_data) if isfile(join(config.path_to_data, f)) and f.endswith(".json")]
    for file in onlyfiles:
        print(file)
        city = re.split(r'(\d+)', file)
        with open(join(config.path_to_data, file), encoding='utf-8') as f:
            data = json.load(f)
            data = data['auctions']
            prepare_data(data, city[0])


def prepare_data(auctions, city):
    for auction in auctions:
        all_auctions.append(auction)
        global index_auction
        auction.update({'id': index_auction})
        auction.update({'city': city})
        get_companies(auction)
        del auction['offer_winners']
        del auction['offer_losers']
        del auction['conditions']
        index_auction += 1
        
def get_companies(auction):
    for winner_company in auction['offer_winners']:
        if winner_company['name'] not in set_companies:
            set_companies.add(winner_company['name'])
            global index_companies
            all_companies_index.append({'id': index_companies, 'name': winner_company['name']})
            index_companies += 1
        all_companies_offers.append({'auction_id': index_auction, 'company_id': return_id_company(winner_company['name']), 'price': winner_company['price']})
    for offer_losers in auction['offer_losers']:
        if offer_losers['name'] not in set_companies:
            set_companies.add(offer_losers['name'])
            all_companies_index.append({'id': index_companies, 'name': offer_losers['name']})
            index_companies += 1
        all_companies_offers.append({'auction_id': index_auction, 'company_id': return_id_company(offer_losers['name']), 'price': offer_losers['price']})

def save_companies():
    auction_links_chunks = [all_auctions[x:x+AUCTION_PER_FILE] for x in range(0, len(all_auctions), AUCTION_PER_FILE)]
    for index, links_chunk in enumerate(auction_links_chunks):
        with open(f'data/new_data/auctions_{index}.json', 'w', encoding='utf-8') as f:
            json.dump(links_chunk, f, ensure_ascii=False, indent=4)
    all_companies_index_chunk = [all_companies_index[x:x+AUCTION_PER_FILE] for x in range(0, len(all_companies_index), AUCTION_PER_FILE)]
    for index, links_chunk in enumerate(all_companies_index_chunk):
        with open(f'data/new_data/companies{index}.json', 'w', encoding='utf-8') as f:
            json.dump(links_chunk, f, ensure_ascii=False, indent=4)
    all_companies_offers_chunk = [all_companies_offers[x:x+AUCTION_PER_FILE] for x in range(0, len(all_companies_offers), AUCTION_PER_FILE)]
    for index, links_chunk in enumerate(all_companies_offers_chunk):
        with open(f'data/new_data/companies_offers{index}.json', 'w', encoding='utf-8') as f:
            json.dump(links_chunk, f, ensure_ascii=False, indent=4)
    
    

get_files()
save_companies()
print(index_companies)
print(index_auction)