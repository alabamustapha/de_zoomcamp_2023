## Question 1. Knowing docker tags
```
--iidfile string
```

## Question 2. Understanding docker first run

```
3
```

```
Package    Version
---------- -------
pip        22.0.4
setuptools 58.1.0
wheel      0.38.4
```


## Question 3. Count records

```
20530
```

SELECT count(lpep_pickup_datetime) 
FROM green_trip_data 
WHERE 
    date_trunc('day', lpep_pickup_datetime) = '2019-01-15 00:00:00' AND 
    date_trunc('day', lpep_dropoff_datetime) = '2019-01-15 00:00:00'


## Question 4. Largest trip for each day

```
2019-01-15
```

`
SELECT lpep_pickup_datetime, trip_distance FROM green_trip_data ORDER BY trip_distance DESC LIMIT 1
`

## Question 5. The number of passengers

```
2 1282
3 254
```

`
SELECT 
COUNT(lpep_pickup_datetime), passenger_count 
FROM green_trip_data 
WHERE date_trunc('day', lpep_pickup_datetime) = '2019-01-01' 
GROUP BY passenger_count
`

## Question 6. Largest tip

```
Long Island City/Queens Plaza
```

`
SELECT zdo."Zone", gr."tip_amount"
FROM green_trip_data gr
JOIN zones zpu
ON gr."PULocationID" = zpu."LocationID"
JOIN zones zdo
ON gr."DOLocationID" = zdo."LocationID"
WHERE zpu."Zone" = 'Astoria'
ORDER BY gr."tip_amount" DESC
LIMIT 1
`
