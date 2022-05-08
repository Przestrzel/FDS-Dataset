from APIservice import APIService
from DataSet import DataSet

api = APIService("tenders", "Grudziądz")
dataSet = DataSet(api, "grudziadz")
dataSet.make_dataset()
