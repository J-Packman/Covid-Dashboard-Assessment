'''basically just a bunch of functions to get the stuff i want from the news api'''
import json
import requests

"""loading constants from config file"""
with open("config.json", "r", encoding="utf8") as config_file:
    config = json.load(config_file)

    BASE_URL = config["news_api_base_url"]
    API_KEY = config["news_api_key"]
    COUNTRY = config["news_api_country"]
    COVID_TERMS = config["covid_terms"]

COMPLETE_URL = BASE_URL + "country=" + COUNTRY + "&apiKey=" + API_KEY

base_url = "https://newsapi.org/v2/top-headlines?"
api_key = "8e73baee0bfa481b9f52aaf687c3e878"
country = "gb"
complete_url = base_url + "country=" + country + "&apiKey=" + api_key

def news_API_request(covid_terms = "Covid COVID-19 coronavirus"):
    """returns latest news stories in the form of a list of dicts"""
    search_terms = covid_terms.split()
    response = requests.get(COMPLETE_URL).json()
    covid_stories = []

    for story in response["articles"]:
        for term in search_terms:
            if term in story["title"]:
                covid_stories.append(story)
                break
    # this print statement helped me test if i got the correct articles
    # print(json.dumps(covid_stories, indent=2))
    return covid_stories

def update_news(old_news):
    """takes the old news and returns a list of dicts with new news!"""
    new_news = news_API_request()
    for story in new_news:
        if story not in old_news:
            old_news.append(story)

    return old_news

def del_news(headline, news_in):
    """takes news, and a headline. if headline
    is in the news, that article gets deleted"""
    i=0
    for story in news_in:
        if story["title"] == headline:
            del news_in[i]
        i += 1
    return news_in


news_API_request()
