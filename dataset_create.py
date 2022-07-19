import json
from .data_model import Bid, PublicInstitution, Tender


CITIES = ('grudziadz', 'lomza', 'lubawa', 'mlawa')


def open_files():
    for city in CITIES:
        with open(f'Opentenders/datasets/{city}/{city}.json') as file:
            data_bid, data_public_institution, data_tender = data_loading(file)


def data_loading(file) -> (set(Bid), set(PublicInstitution), set(Tender)):
    dataset_bid = set()
    dataset_tender = set()
    dataset_public_institution = set()
    data = json.load(file)
    for info in data:
        dataset_tender.add(Tender(
            title=info['title'],
            max_value=info['estimatedPrice']['netAmount'],
            is_euFund=info['fundings']['isEuFund'],
            state=info['lots']['status'],
            end_value=info['lots']['status']['bids']['price']['netAmount'],
            requirements_length=len(info['description']),
            CPV=[info['cpvs']['code']],
            procedure_type=info['procedureType'],
        ))
        dataset_public_institution.add(PublicInstitution(
         name = info['buyers']['name'],
         type = info['buyers']['buyer_type'],
        ))
