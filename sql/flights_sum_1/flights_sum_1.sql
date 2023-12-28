select sum(dep_delay) from flights where year_date = 2000;
select sum(taxi_out) from flights where unique_carrier = '9E';
select sum(taxi_in) from flights where origin = 'MSP';
select sum(arr_delay) from flights where origin_state_abr = 'TX';
select sum(air_time) from flights where dest = 'BTV';
select sum(distance) from flights where dest_state_abr = 'MO';
select sum(distance) from flights where dep_delay > 500;
select sum(air_time) from flights where taxi_out > 100;
select sum(arr_delay) from flights where taxi_in < 3;
select sum(taxi_in) from flights where arr_delay < -20;
select sum(taxi_out) from flights where air_time > 400;
select sum(dep_delay) from flights where distance < 200;