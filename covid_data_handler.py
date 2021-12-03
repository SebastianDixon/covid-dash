import csv
import json
from uk_covid19 import Cov19API
import sched, time
import os

"""csv_path = os.environ['CSV_PATH']


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
"""


def covid_API_request(location=os.environ['LOCATION'], location_type=os.environ['LOCATION_TYPE']):
    location_filter = [f'areaType={location_type}', f'areaName={location}']

    cases_and_deaths = {
        "areaCode": "areaCode",
        "areaName": "areaName",
        "areaType": "areaType",
        "date": "date",
        "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",
        "hospitalCases": "hospitalCases",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate"}

    api = Cov19API(filters=location_filter, structure=cases_and_deaths)
    api_data = api.get_json()
    return api_data['data']


def process_covid_data():
    local_data = covid_API_request()
    national_data = covid_API_request(location=os.environ['LOCATION'],
                                      location_type=os.environ['LOCATION_TYPE'])

    count = 1
    local_cases = 0
    national_cases = 0
    while count < 9:
        local_cases += local_data[count]['newCasesBySpecimenDate']
        national_cases += national_data[count]['newCasesBySpecimenDate']
        count += 1

    total_death = 0
    for i in national_data:
        if i['cumDailyNsoDeathsByDeathDate'] == None:
            pass
        else:
            if i['cumDailyNsoDeathsByDeathDate'] > total_death:
                total_death = i['cumDailyNsoDeathsByDeathDate']

    local_rate = local_cases / 7
    national_rate = national_cases / 7
    h_cases = national_data[1]['hospitalCases']
    return [local_rate, national_rate, total_death, h_cases]


def schedule_covid_updates(update_interval, update_name):
    s = sched.scheduler(time.time, time.sleep)
    s.enter(update_interval, 1, process_covid_data())
    s.run()
