import json
from .data_model import Bid, PublicInstitution, Tender


CITIES = ('grudziadz', 'lomza', 'lubawa', 'mlawa')


for city in CITIES:
    dataset = []
    with open(f'Opentenders/datasets/{city}/{city}.json') as file:
        with open(f'Opentenders/{city}.json', 'w') as out_file:
            data = json.load(file)
            for info in data:
                dataset.append(Tender(
                    title=info['title'],
                    max_value=info['estimatedPrice']['netAmount'],
                    is_euFund=info['fundings']['isEuFund'],
                    state=info['lots']['status'],
                    end_value=info['lots']['status']['bids']['price']['netAmount'],
                    requirements_length=len(info['description']),
                    CPV=[info['cpvs']['code']],

                ))
        out_file.write()
