# Chicago Taxi Ride-and-Share Data Dictionary

This dataset was used to build machine learning models predicting exact fares and tipping behavior.

| Feature | Description | Data Type |
| :--- | :--- | :--- |
| **trip_miles** | Total distance of the taxi ride in miles. | Numeric (Float) |
| **trip_seconds** | Total duration of the taxi ride in seconds. | Numeric (Integer) |
| **trip_hour** | The specific hour of the day the trip started (0-23). | Numeric (Integer) |
| **trip_day** | The day of the week the trip occurred. | Categorical / Numeric |
| **payment_type** | The method of payment used by the rider (e.g., Cash, Credit Card). | Categorical |
| **fare** | The base continuous dollar amount of the trip cost. *(Target for Regression)* | Numeric (Float) |
| **tips** | The exact dollar amount of the tip left. | Numeric (Float) |
| **tip_given** | Binary classification target indicating if a tip was left (1 = Yes, 0 = No). *(Target for Classification)* | Binary (Integer) |