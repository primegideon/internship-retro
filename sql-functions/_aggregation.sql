---1. Trip count and total revenue by hour of day
--- Use EXTRACT(HOUR...) and round the revenue to two decimal places for financial exactness.
---
SELECT
  EXTRACT(HOUR FROM trip_start_timestamp) AS hour_of_day,
  COUNT(unique_key) AS trip_count,
  ROUND(SUM(trip_total), 2) AS total_revenue
FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
WHERE EXTRACT(YEAR FROM trip_start_timestamp) = 2023
GROUP BY hour_of_day
ORDER BY hour_of_day;
---
---2. Trip count by day of week
---EXTRACT(DAYOFWEEK...) returns an integer where 1 is Sunday and 7 is Saturday.

SELECT
  EXTRACT(DAYOFWEEK FROM trip_start_timestamp) AS day_of_week_num,
  COUNT(unique_key) AS trip_count
FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
WHERE EXTRACT(YEAR FROM trip_start_timestamp) = 2023
GROUP BY day_of_week_num
ORDER BY day_of_week_num;

---4. Top 10 taxi companies by trip count and average fare
---group by the company, rank them by volume, and cap it at 10. also filter out null company names to keep the data audit clean.
SELECT
  company,
  COUNT(unique_key) AS trip_count,
  ROUND(AVG(fare), 2) AS avg_fare
FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
WHERE EXTRACT(YEAR FROM trip_start_timestamp) = 2023
  AND company IS NOT NULL
GROUP BY company
ORDER BY trip_count DESC
LIMIT 10;
