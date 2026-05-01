-- Example PostgreSQL load command.
-- Update the path to the local copy of diabetic_data.csv before running.

\copy raw_diabetic_encounters FROM 'data/raw/diabetic_data.csv' WITH (FORMAT csv, HEADER true);

SELECT
    COUNT(*) AS encounter_count,
    COUNT(DISTINCT patient_nbr) AS patient_count,
    ROUND(100.0 * AVG(CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END), 1) AS readmit_30_rate_pct
FROM raw_diabetic_encounters;
