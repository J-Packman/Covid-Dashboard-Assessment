from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_API_request
from covid_data_handler import schedule_covid_updates

def test_parse_csv_data():
    """tests the parse csv function, if it doesnt throw an assertion error
    then it works"""
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639

def test_process_covid_csv_data():
    """tests the process csv function, if it doesnt throw an assertion error
    then it works"""
    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data ( parse_csv_data (
            'nation_2021-10-28.csv' ) )
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544

def test_covid_API_request():
    """tests the covid api request function, if it doesnt throw an
    assertion error then it works"""
    data = covid_API_request()
    assert isinstance(data, dict)

def test_schedule_covid_updates():
    """tests the schedule covid updates function, if it doesnt throw an assertion error
    then it works"""
    schedule_covid_updates(update_interval=10, update_name='update test')

# running each test
test_covid_API_request()
test_parse_csv_data()
test_process_covid_csv_data()
