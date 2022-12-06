import os
import pytz
import requests
from datetime import datetime, timedelta, timezone

finals_2000A_table_url = 'https://maia.usno.navy.mil/ser7/finals2000A.daily'
leap_seconds_table_url = 'https://maia.usno.navy.mil/ser7/tai-utc.dat'

def date_single_month(year, month, day):
        if len(day) == 1:
            date = year + ' ' + month + ' ' + day
        else:
            date = year + ' '+ month + day
            
        return date

def date_double_month(year, month, day):
        if len(day) == 1:
            date = year + month + ' ' + day
        else:
            date = year + month + day
            
        return date  

def get_DUT1_dates(start_date, end_date):    
    """
    Parameters
    ----------
    start_date : datetime object
        start date of the time domain
        
    end_date : datetime object
        end date of the time domain
        
    Returns
    -------
    start_date : str
        start date of the time domain in format of DUT1 dates on associated website
        
    end_date : str
        end date of the time domain in format of DUT1 dates on associated website
    
    """
    
    start_year, start_month, start_day = f'{start_date.year}'[2:], f'{start_date.month}', f'{start_date.day}'
    end_year, end_month, end_day = f'{end_date.year}'[2:], f'{end_date.month}', f'{end_date.day}'
        
    
    if len(start_month) == 1:
        start_date = date_single_month(start_year, start_month, start_day)

    else:
        start_date = date_double_month(start_year, start_month, start_day)

    if len(end_month) == 1:
        end_date = date_single_month(end_year, end_month, end_day)

    else:
        end_date = date_double_month(end_year, end_month, end_day)

    return start_date, end_date

def retrieve_dut1_values(url, start_date, end_date):
    file_name = f'correction_table_UT1.dat'
    response = requests.get(url)
    
    DUT1 = [values[58:68] for values in response.text.split('\n')]
    dates = [values[:6] for values in response.text.split('\n')]
    
    DUT1_start_date, DUT1_end_date = get_DUT1_dates(start_date, end_date)
    
    date_range = dates[dates.index(DUT1_start_date):dates.index(DUT1_end_date) + 1]
    DUT1_range = DUT1[dates.index(DUT1_start_date):dates.index(DUT1_end_date) + 1]
    
    if not os.path.isfile(file_name): 
        with open(file_name, 'w') as f:
            f.write('\n'.join(DUT1_range))
        return DUT1_range, date_range, file_name
    else:
        raise Exception('file already exists')
        return


def time_domain_to_gps(url, time_domain):
    """
    For the implementation of this function, it has been assumed that the start and end date lie entirely within one 'period'
    of leap seconds, i.e. over the entire time_domain only one correction needs to be applied, and the time_domain does not 
    cross over a leap second date. For this implementation to be added, check whether one of the leap dates lie within the
    time domain chosen. As the last leap date was in 2017, and no new leap second will be introduced in december 2022, so 
    it will be assumed this is not necessary.
    """
    file_name = f'correction_table_GPS.dat'
    response = requests.get(url)
    
    leap_seconds = [values[38:48] for values in response.text.split('\n')]
    current_leap_second = float(leap_seconds[-2])
    GPS_time_domain = [(date + timedelta(seconds = current_leap_second)) for date in time_domain]
    
    if not os.path.isfile(file_name): 
        with open(file_name, 'w') as f:
            f.write('\n'.join(leap_seconds))
        f.close()
    
    return GPS_time_domain

