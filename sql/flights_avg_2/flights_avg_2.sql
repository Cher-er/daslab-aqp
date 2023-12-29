select avg(dep_delay) from flights where year_data = 2000;
select avg(taxi_out) from flights where unique_carrier = '9E';
select avg(taxi_in) from flights where origin = 'MSP';
select avg(arr_delay) from flights where origin_state_abr = 'TX';
select avg(air_time) from flights where dest = 'BTV';
select avg(distance) from flights where dest_state_abr = 'MO';