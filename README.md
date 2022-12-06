The table_retrieval.py script retrieves the table necessary to convert the UTC time domains to UT1 and GPS time domains. In order to use the code, call the
retrieve_dut1_values(url, start_date, end_date) to retrieve the DUT1 time correction tables. Here the url is the url of the correction table and the start and end date 
specify the time domain in UTC. The code returns a list of the DUT1 values for every day in the given range. The time_domain_to_gps(url, time_domain) retrieves the GPS 
correction tables, where the url is the url of the correction table and the time domain is given in UTC. The code returns the current leap second as a str. 

A working example:

```
finals_2000A_table_url = 'https://maia.usno.navy.mil/ser7/finals2000A.daily'
leap_seconds_table_url = 'https://maia.usno.navy.mil/ser7/tai-utc.dat'

start_time = '2022-12-01T00:00:00'
end_time = '2022-12-04T00:00:00'

start_date = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
end_date = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')
delta_t_minutes = int((end_date - start_date).total_seconds() / 60)

time_domain = [start_date + int(time_step) * timedelta(minutes=i) for i in
               range(int(delta_t_minutes / int(time_step)))]
               
DUT1_range = retrieve_dut1_values(finals_2000A_table_url, start_date, end_date)
GPS_leap_second = time_domain_to_gps(leap_seconds_table_url, time_domain)
```




