import json


CITIES = ('grudziadz', 'lomza', 'lubawa', 'mlawa')


for city in CITIES:
    dataset = []
    with open(f'Opentenders/datasets/{city}/{city}.json') as file:
        data = json.load(file)
        for info in data:
            for bids in info['lots']:
                try:
                    for bidders in bids['bids']:
                        if not bidders['isWinning']:
                            print('sth')
                except Exception:
                    pass

