---6. Peak hour revenue ranking
---uses a subquery to first calculate the revenue per hour, and then the RANK() window function to order them from most to least profitable system-wide.
SELECT
  hour_of_day,
  total_revenue,
  RANK() OVER(ORDER BY total_revenue DESC) AS revenue_rank
FROM (
  SELECT
    EXTRACT(HOUR FROM trip_start_timestamp) AS hour_of_day,
    ROUND(SUM(trip_total), 2) AS total_revenue
  FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
  WHERE EXTRACT(YEAR FROM trip_start_timestamp) = 2023
  GROUP BY hour_of_day
)
ORDER BY revenue_rank;

---
