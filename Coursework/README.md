# Jamie's Epic Personalised Covid Data Dashboard

## Introduction
GitHub link: https://github.com/J-Packman/Covid-Dashboard-Assessment/tree/main/Coursework

The purpose of this project is to deliver a personalised covid data dashboard to present up-to-date 
covid data and news for a local and national area (Exeter and england respectively by default).
This is intended for individual personal use.

## Prerequisites & installation
I think all that is required is the UK covid api and flask.
### UK Covid API
Information regarding the API can be found here: https://pypi.org/project/uk-covid19/
For typical installation use ```pip install uk-covid19```
### Flask
Information about flask can be found here: https://pypi.org/project/Flask/
For typical installation use ```pip install Flask```
## Instructions for use
### Opening the dashboard
-  **Ensure all files are as you found them and run the main.py file**
-  **On the same machine, open a browser of your choice and navigate to:**
-  > http://127.0.0.1:5000/index
### Using the dashboard
- **Scheduling updates:** To schedule an update, Enter a name for the update in the text box then select a time by clicking on the clock icon, then choose which type of update and if you want it repeated by toggling the checkboxes and hit submit.
- By default **repeated updates** are set to repeat every 24hrs, to change this alter the ```repeat_update_time_secs``` value in the **config.json** (The value represents the seconds between each update)
- **Local and national location** can be changed by altering the values for ```location``` and ```nation``` in the **config.json** file
- To **filter what type of news** appears in the news feed, adjust the ```covid_terms``` value in the **config.json** file, it is filtered by each word delimited by a space " "
## Testing
I have handily put the testing files ```test_covid_data_handling.py``` and ```test_news_data_handling.py``` in with everything else (defo not because im lazy). **To run the tests,** simply run these files and if it doesn't give an assertion error then the test has passed.
## Developer notes
If you want to attempt to decipher the spaghetti I have included docstrings for each function and module, key thing is that most stuff is in the main.py file except for updates which are in the covid_data_handler.py file
## Details
### Authors
- Jamie Packer
### Acknowledgements
The covid-19 api provided by her majesty's government was very useful

