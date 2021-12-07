
import datetime
from server.covid_data_handler import parse_csv_data, process_covid_csv_data
import unittest


class TestData(unittest.TestCase):
    def test_parse_csv_data(self):
        data = parse_csv_data("C:/Users/marke/Desktop/ECM1400/nation_2021-10-28.csv")
        assert len(data) == 639

    def test_process_covid_csv_data(self):
        last7days_cases, current_hospital_cases, total_deaths =
        process_covid_csv_data(parse_csv_data(mock_api_result))
        assert last7days_cases == 10661
        assert current_hospital_cases == 6027
        assert total_deaths is None


mock_api_result = {
    "data": [
        {'areaCode': 'E92000001',
         'areaName': 'England',
         'areaType': 'nation',
         'date': '2021-12-07',
         'cumDailyNsoDeathsByDeathDate': None,
         'hospitalCases': 6027,
         'newCasesBySpecimenDate': None},

        {'areaCode': 'E92000001',
         'areaName': 'England',
         'areaType': 'nation',
         'date': '2021-12-06',
         'cumDailyNsoDeathsByDeathDate': None,
         'hospitalCases': 5992,
         'newCasesBySpecimenDate': 10661}
    ]
}

mock_today = datetime.datetime.strptime("2021-12-07", "%Y-%m-%d").date()
