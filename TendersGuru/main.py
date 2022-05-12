from APIservice import APIService
from DataSet import DataSet
import csv

api = APIService("tenders", "Lubawa")
dataSet = DataSet(api, "lubawa")
dataSet.make_dataset()
dataSet.open_CSV_from_scrapper()
dataSet.save_to_JSON()