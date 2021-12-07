"""
Test code for server.api.covid
"""

import datetime
from pytest_mock import MockerFixture

from server import covid_data_handler

__mock_data_point = {
    "date": "2020-07-28",
    "areaName": "test-area-name",
    "areaCode": "test-area-code",
    # new cases on the given date
    "newCasesByPublishDate": 1,
    # cumulative cases up until the given date
    "cumCasesByPublishDate": 2,
    # number of new deaths on the given date
    "newDeathsByDeathDate": 3,
    # cumulative number of deaths up until the given date
    "cumDeathsByDeathDate": 4,
}

__mock_api_result = {
    "data": [
        {
            "date": "2020-07-28",
            "areaName": "England",
            "areaCode": "E92000001",
            "newCasesByPublishDate": 547,
            "cumCasesByPublishDate": 259022,
            "newDeathsByDeathDate": None,
            "cumDeathsByDeathDate": None,
        },
        {
            "date": "2020-07-27",
            "areaName": "England",
            "areaCode": "E92000001",
            "newCasesByPublishDate": 616,
            "cumCasesByPublishDate": 258475,
            "newDeathsByDeathDate": 20,
            "cumDeathsByDeathDate": 41282,
        },
    ]
}

__mock_today = datetime.datetime.strptime("2020-07-28", "%Y-%m-%d").date()


def test_fetch_covid_data():
    result = covid_data_handler.process_covid_data()
    #    return [local_rate, national_rate, total_death, h_cases]

    assert result[0]
    assert result[1]
    assert result[2] == 547
    assert result[3] == 259022
