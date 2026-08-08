--- Purpose: Initial Data Validation for 2023-01
SELECT 
trip_start_timestamp,
    fare,
    tips,
    trip_total,
    trip_seconds,
    pickup_community_area
FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
WHERE EXTRACT(YEAR FROM trip_start_timestamp) = 2023 
  AND EXTRACT(MONTH FROM trip_start_timestamp) = 1
LIMIT 1000;
