import csv
from uk_covid19 import Cov19API
import os
import logging

"""
This module handles calling covid data for the front end
"""

csv_path = os.environ['CSV_PATH']

cases_and_deaths = {
    "areaCode": "areaCode",
    "areaName": "areaName",
    "areaType": "areaType",
    "date": "date",
    "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",
    "hospitalCases": "hospitalCases",
    "newCasesBySpecimenDate": "newCasesBySpecimenDate"}


def parse_csv_data(csv_path):
    file = []

    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            file.append(row)
    return file


def process_covid_csv_data(covid_csv_data):
    hospital_cases = int(covid_csv_data[0]['hospitalCases'])

    cases = 0
    count = 0
    for i in covid_csv_data:
        num = i['newCasesBySpecimenDate']
        if num == '':
            pass
        elif count == 8:
            break
        else:
            cases += int(num)
            count += 1

    cumulative_cases = 0
    for i in covid_csv_data[1:]:
        value = i['cumDailyNsoDeathsByDeathDate']
        if value == '':
            pass
        else:
            if int(value) >= cumulative_cases:
                cumulative_cases = int(value)

    output = [hospital_cases, cases, cumulative_cases]
    return output


def covid_api_request(location=os.environ['LOCATION'], location_type=os.environ['LOCATION_TYPE']):
    try:
        location_filter = [f'areaType={location_type}', f'areaName={location}']

        api = Cov19API(filters=location_filter, structure=cases_and_deaths)
        api_data = api.get_json()
        return api_data['data']
    except:
        logging.error("API request couldn't be made")
        raise Exception


def process_covid_data():
    local_data = covid_api_request()
    national_data = covid_api_request(location=os.environ['NATION'], location_type=os.environ['NATION_TYPE'])

    count = 1
    local_cases = 0
    national_cases = 0
    while count < 9:
        local_cases += local_data[count]['newCasesBySpecimenDate']
        national_cases += national_data[count]['newCasesBySpecimenDate']
        count += 1

    total_death = 0
    for i in national_data:
        if i['cumDailyNsoDeathsByDeathDate'] is None:
            pass
        else:
            if i['cumDailyNsoDeathsByDeathDate'] > total_death:
                total_death = i['cumDailyNsoDeathsByDeathDate']

    local_rate = local_cases / 7
    national_rate = national_cases / 7
    h_cases = national_data[1]['hospitalCases']
    print(national_data)
    return [local_rate, national_rate, total_death, h_cases]
