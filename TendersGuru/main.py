from APIservice import APIService
from DataSet import DataSet

api = APIService("tenders", "Mława")
dataSet = DataSet(api)
dataSet.make_dataset()
