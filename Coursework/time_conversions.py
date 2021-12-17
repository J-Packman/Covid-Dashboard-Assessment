"""bunch of funcitons to get the time and convert between time formats"""

import time

def minutes_to_seconds( minutes: str ) -> int:
    """Converts minutes to seconds"""
    return int(minutes)*60

def hours_to_minutes( hours: str ) -> int:
    """Converts hours to minutes"""
    return int(hours)*60

def hhmm_to_seconds( hhmm: str ) -> int:
    """turns string hours:minutes to just int seconds"""
    if len(hhmm.split(':')) != 2:
        print('Incorrect format. Argument must be formatted as HH:MM')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
    minutes_to_seconds(hhmm.split(':')[1])

def current_time_hhmm():
    """converts current time to hours:minutes format"""
    return str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min)

def current_time_secs():
    """gets the current time in seconds"""
    return hhmm_to_seconds(current_time_hhmm())
