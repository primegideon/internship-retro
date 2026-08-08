---8. CTE: Trips classified as short/medium/long
--Common Table Expressions (CTEs) keep the logic separated. The top half categorizes the data, and the bottom half aggregates it.
WITH TripClassifications AS (
  SELECT
    CASE
      WHEN trip_miles <= 2 THEN 'Short'
      WHEN trip_miles > 2 AND trip_miles <= 10 THEN 'Medium'
      WHEN trip_miles > 10 THEN 'Long'
    END AS trip_class,
    trip_total,
    CASE 
      WHEN fare > 0 THEN (tips / fare) * 100 
      ELSE 0 
    END AS tip_rate_percent
  FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
  WHERE EXTRACT(YEAR FROM trip_start_timestamp) = 2023
    AND trip_miles IS NOT NULL
)
SELECT
  trip_class,
  COUNT(*) AS total_trips,
  ROUND(SUM(trip_total), 2) AS total_revenue,
  ROUND(AVG(tip_rate_percent), 2) AS avg_tip_rate_percent
FROM TripClassifications
WHERE trip_class IS NOT NULL
GROUP BY trip_class
ORDER BY total_revenue DESC;
