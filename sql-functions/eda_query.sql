 SELECT * FROM (
        SELECT
            trip_start_timestamp, fare, tips, trip_total,
            trip_seconds, trip_miles, pickup_community_area,
            company, payment_type,
            ROW_NUMBER() OVER(PARTITION BY payment_type ORDER BY RAND()) as row_num
        FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
        WHERE EXTRACT(YEAR FROM trip_start_timestamp) = 2023
    )
    WHERE row_num <= 50000
