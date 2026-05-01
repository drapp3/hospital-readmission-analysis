-- Dimension-style extracts used for analysis and dashboard filters.

CREATE TABLE dim_patients AS
SELECT
    patient_nbr,
    MAX(age) AS age_group,
    MAX(gender) AS gender,
    MAX(CASE WHEN race = '?' THEN 'Unknown' ELSE race END) AS race,
    COUNT(*) AS encounter_count
FROM raw_diabetic_encounters
GROUP BY patient_nbr;

CREATE TABLE dim_diagnoses AS
SELECT DISTINCT
    diag_1,
    diag_2,
    diag_3,
    CASE
        WHEN diag_1 BETWEEN '390' AND '459' OR diag_1 = '785' THEN 'Circulatory'
        WHEN diag_1 BETWEEN '460' AND '519' OR diag_1 = '786' THEN 'Respiratory'
        WHEN diag_1 BETWEEN '520' AND '579' OR diag_1 = '787' THEN 'Digestive'
        WHEN diag_1 LIKE '250%' THEN 'Diabetes'
        ELSE 'Other'
    END AS primary_diagnosis_group
FROM raw_diabetic_encounters;

CREATE INDEX idx_dim_patients_patient ON dim_patients (patient_nbr);
