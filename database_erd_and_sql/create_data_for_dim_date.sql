INSERT INTO dim_date
SELECT 
    TO_CHAR(date, 'YYYYMMDD')::INT AS date_key,
    date AS full_date,
    EXTRACT(ISODOW FROM date) AS day_of_week,  -- Monday=1 to Sunday=7
    TO_CHAR(date, 'Day') AS day_name,
    EXTRACT(DAY FROM date) AS day_of_month,
    EXTRACT(DOY FROM date) AS day_of_year,
    EXTRACT(WEEK FROM date) AS week_of_year,
    EXTRACT(MONTH FROM date) AS month_number,
    TO_CHAR(date, 'Month') AS month_name,
    EXTRACT(QUARTER FROM date) AS quarter_number,
    'Q' || EXTRACT(QUARTER FROM date) AS quarter_name,
    EXTRACT(YEAR FROM date) AS year,
    CASE WHEN EXTRACT(ISODOW FROM date) IN (6, 7) THEN TRUE ELSE FALSE END AS is_weekend,
    FALSE AS is_holiday,  -- Default to false, can update holidays separately
    NULL AS holiday_name  -- Can be updated later
FROM 
    generate_series(
        '2016-01-01'::date, 
        '2025-12-31'::date, 
        '1 day'::interval
    ) AS date;