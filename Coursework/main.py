"""This is the main file with most of the stuff in

very sorry for the spaghetti code im sure i could have designed the whole thing a lot better
but it works i think
"""
import sched
import json
import time
from flask import Flask, render_template, request
import covid_data_handler as dh
import covid_news_handling as nh
import time_conversions as tc

s = sched.scheduler(time.time, time.sleep)

"""loading constants from config file"""
with open("config.json", "r", encoding="utf8") as config_file:
    config = json.load(config_file)
    LOCATION = config["location"]
    NATION = config["nation"]
    REPEAT_TIME = config["repeat_update_time_secs"]
    IMAGE_NAME = config["image_name"]


news = nh.news_API_request()
local_data = dh.covid_API_request()
UK_data = dh.covid_API_request("overview")
local_7day_inf = dh.get_7day_inf(LOCATION)
national_7day_inf = dh.get_7day_inf(NATION, "nation")

#print(news)

app = Flask(__name__)
@app.route("/index")
def main():
    """main function which interfaces with the flask app"""
    s.run(blocking=False)

    update_label = request.args.get("two")
    update_covid = request.args.get("covid-data")
    update_repeat = request.args.get("repeat")
    update_time = request.args.get("update")
    update_news = request.args.get("news")
    if update_covid:
        add_covid_update(update_time, update_label, update_repeat)
    if update_news:
        add_news_update(update_time, update_label,update_repeat)


    delete_update = request.args.get("update_item")
    if delete_update:
        dh.del_update(delete_update)

    delete_news = request.args.get("notif")
    if delete_news:
        news = nh.del_news(delete_news, get_news())

    return render_template("index.html",
        title = "Jamie's Covid Dashboard",
        location = LOCATION,
        nation_location = NATION,
        news_articles = get_news(),
        local_7day_infections = local_7day_inf,
        national_7day_infections = national_7day_inf,
        hospital_cases = "Hospital Cases : " +str(UK_data["data"][2]["hospitalCases"]),
        deaths_total = "Total deaths : " + str(UK_data["data"][0]["cumDeaths28DaysByPublishDate"]),
        updates = dh.updates,
        image = IMAGE_NAME
        )


def update_covid_data(update_name = None, repeated = None):
    """gets the most up to date covid data from the api and sticks them in necessary
    dictionaries and variables"""
    local_data = dh.covid_API_request(LOCATION)
    local_7day_inf = dh.get_7day_inf(LOCATION)
    national_7day_inf = dh.get_7day_inf(LOCATION, "nation")
    # scheduling a new event if the update is set to be repeated
    if repeated is not None:
        for update in dh.updates:
            if update["title"] == update_name:
                event = s.enter(REPEAT_TIME, 1,
                                update_news_data,
                                argument=(update_name , repeated ,))
                update["event"] = event
    else: # deleting the update if it is not due to repeat
        dh.del_update(update_name)

def add_covid_update(raw_time, update_name, repeated = None):
    """adds a new update to the update list in the form of a dictionary
    with the useful data, (title, event e.t.c)"""
    if raw_time:
        seconds_till_update = tc.hhmm_to_seconds(raw_time) - tc.current_time_secs()
    else:
        print("no time parameter entered, set to 04:20")
        raw_time = "04:20"

    description = "Covid data update scheduled for " + raw_time
    if repeated:
        description = description + " and repeated"
    event = s.enter(seconds_till_update, 1, update_covid_data, argument=(update_name , repeated))

    dh.updates.append({"title": update_name,
                    "content": description,
                    "event": event,
                    "repeated": repeated,
                    "time": tc.hhmm_to_seconds(raw_time)})

def add_news_update(raw_time, update_name,repeated = None):
    '''this function takes the parameters entered on the page,
     adds the blah blah blah'''
    seconds_till_update = tc.hhmm_to_seconds(raw_time) - tc.current_time_secs()
    description = "Covid news update scheduled for " + raw_time
    if repeated:
        description = description + " and repeated"
    event = s.enter(seconds_till_update, 1, update_news_data, argument=(update_name , repeated))
    dh.updates.append({"title": update_name, # note to jamie, remember that stupid  ^ comma
                    "content": description,
                    "event": event,
                    "repeated": repeated,
                    "time": tc.hhmm_to_seconds(raw_time) })

def update_news_data(update_name = None, repeated = None):
    """updates the news variable with most recent news from the api"""
    news = nh.update_news(get_news())

    if repeated is not None:
        for update in dh.updates:
            if update["title"] == update_name:
                event = s.enter(86400, 1, update_news_data, argument=(update_name , repeated ,))
                update["event"] = event
    else:
        dh.del_update(update_name)

def get_news():
    '''i dont really know why this works but it fixed an error which said news
     wasnt assigned even though its assigned at the very top of this file'''
    return news

if __name__ == "__main__":
    app.run(debug=(True))
