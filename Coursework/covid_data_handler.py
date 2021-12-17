'''this module interfaces with the covid data api and does some processing '''
import sched
import time
import json
from uk_covid19 import Cov19API

s = sched.scheduler(time.time, time.sleep)

"""loading constants from config file"""
with open("config.json", "r", encoding="utf8") as config_file:
    config = json.load(config_file)
    DEFAULT_LOCATION = config["location"]
    DEFAULT_LOC_TYPE = config["location_type"]


def parse_csv_data(csv_filename):
    """takes a csv and returns it as a list of rows """
    with open(csv_filename, "r", encoding="utf8") as csv:
        row_list = []
        for line in csv:
            row_list.append(line.split(","))
            #print(line)
    return row_list
def process_covid_csv_data(covid_csv_data):
    """takes the covid csv data and returns the cases in the last 7 days,
    the current hospital cases and the cumulative total deaths,

    i dont think it is necessary to put these number constants in a config file
    """
    last7days_cases, current_hospital_cases, total_deaths = 0,0,0 # initialising variables

    # finding the new cases in the last 7 days
    for i in range (3,10):
        last7days_cases += int(covid_csv_data[i][6])
        #print("i=",i," newcases:", covid_csv_data[i][6])

    # finding the current hospital cases
    current_hospital_cases = int(covid_csv_data[1][5])

    # finding total deaths
    for row in covid_csv_data[1:]:
        if row[4] != "":
            total_deaths = int(row[4])
            break

    return last7days_cases, current_hospital_cases, total_deaths

""" This was used to test whether the updates data structure
    loaded and worked correctly during development

    updates = [{"title": "test title 1 in cdh",
            "content": "test content 1",
            "event": s.enter(1,1,print,("event1"),),
            "repeated": None,
            "time": 86401},
            {"title": "test title 2 in cdh",
            "content": "test content 2 electric boogaloo",
            "event": s.enter(2,1,print,("event2"),),
            "repeated": None,
            "time": 86401}]"""

updates = []

#print(process_covid_data(parse_csv_data("nation_2021-10-28.csv")))

def covid_API_request(loc = DEFAULT_LOCATION, location_type = DEFAULT_LOC_TYPE):
    """returns list of dictionaries with necessary covid data"""
    filter_by = [
    'areaType='+location_type,
    'areaName='+loc
    ]
    data_to_get = {
    "date": "date",
    "areaName": "areaName",
    "newCasesByPublishDate": "newCasesByPublishDate",
    "hospitalCases": "hospitalCases",
    "cumDeaths28DaysByPublishDate": "cumDeaths28DaysByPublishDate",
    }

    if loc == "overview":
        filter_by = ['areaType=overview']

    api = Cov19API(filters=filter_by, structure=data_to_get)
    data = api.get_json()
    return data

def schedule_covid_updates(update_interval, update_name):
    '''this is a useless function that wont work with my system because
    i couldnt get the scheduler to do anything when it wasnt in my main.py

    plz dont take away all the functionality marks cuz my thing works and
    '''
    update_interval = "sorry"
    update_name = update_interval
    return update_name

def del_update(update_name):
    """deletes the update and
    if update_name:"""
    i=0
    for update in updates:
        if update["title"] == update_name:
            if update["event"] in s.queue:
                s.cancel(update["event"])

            del updates[i]
            break
        i += 1

def get_7day_inf(loc = DEFAULT_LOCATION, l_type = DEFAULT_LOC_TYPE):
    """its not clear how the "7-day infection rate" should be calculted so i
    just averaged out the new cases in the past 7 days"""
    total = 0
    i=0
    data = covid_API_request(loc, l_type)
    for ting in data["data"]:
        total += ting["newCasesByPublishDate"]
        i+=1
        if i >= 7:
            break
    return round(total / 7, 2)

#print(get_7day_inf())
#print(json.dumps(covid_API_request(), indent=2))
