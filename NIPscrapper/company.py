import json


class Company:

    def __init__(self, company_name, nip_number, owner_name, city_name, postal_code, phone_number, krs_number, regon_number, legal_form, board_members, procuration_members,supervisory_board):
        self.company_name = company_name
        self.nip_number = nip_number
        self.owner_name = owner_name
        self.city_name = city_name
        self.postal_code = postal_code
        self.phone_number = phone_number
        self.krs_number = krs_number
        self.regon_number = regon_number
        self.legal_form = legal_form
        self.board_members = board_members
        self.procuration_members = procuration_members
        self.supervisory_board = supervisory_board

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False)


class Companies:

    def __init__(self):
        self.companies = []

    def add_company(self, other: Company):
        self.companies.append(other)

    def add_companies(self, others: Company):
        for company in others:
            self.companies.append(company)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False)