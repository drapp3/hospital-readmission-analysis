-- Encounter-level fact table for readmission analysis.
-- This mirrors the cleaned dataset produced by python/02_data_cleaning.py.

CREATE TABLE fact_encounters AS
SELECT
    encounter_id,
    patient_nbr,
    CASE WHEN race = '?' THEN 'Unknown' ELSE race END AS race,
    gender,
    age,
    admission_type_id,
    discharge_disposition_id,
    admission_source_id,
    time_in_hospital,
    CASE WHEN medical_specialty = '?' THEN 'Unknown' ELSE medical_specialty END AS medical_specialty,
    num_lab_procedures,
    num_procedures,
    num_medications,
    number_outpatient,
    number_emergency,
    number_inpatient,
    CASE WHEN diag_1 = '?' THEN 'Unknown' ELSE diag_1 END AS diag_1,
    CASE WHEN diag_2 = '?' THEN 'Unknown' ELSE diag_2 END AS diag_2,
    CASE WHEN diag_3 = '?' THEN 'Unknown' ELSE diag_3 END AS diag_3,
    number_diagnoses,
    change,
    diabetesMed,
    CASE WHEN readmitted = '<30' THEN 1 ELSE 0 END AS readmit_30
FROM raw_diabetic_encounters;

CREATE INDEX idx_fact_readmit_30 ON fact_encounters (readmit_30);
CREATE INDEX idx_fact_patient ON fact_encounters (patient_nbr);
