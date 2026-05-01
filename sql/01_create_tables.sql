-- Base table definitions for the UCI Diabetes 130-US Hospitals dataset.
-- The raw staging table keeps source columns as text where values may contain
-- category labels such as ">8", "None", or "?".

CREATE TABLE raw_diabetic_encounters (
    encounter_id BIGINT PRIMARY KEY,
    patient_nbr BIGINT NOT NULL,
    race TEXT,
    gender TEXT,
    age TEXT,
    weight TEXT,
    admission_type_id INTEGER,
    discharge_disposition_id INTEGER,
    admission_source_id INTEGER,
    time_in_hospital INTEGER,
    payer_code TEXT,
    medical_specialty TEXT,
    num_lab_procedures INTEGER,
    num_procedures INTEGER,
    num_medications INTEGER,
    number_outpatient INTEGER,
    number_emergency INTEGER,
    number_inpatient INTEGER,
    diag_1 TEXT,
    diag_2 TEXT,
    diag_3 TEXT,
    number_diagnoses INTEGER,
    max_glu_serum TEXT,
    A1Cresult TEXT,
    change TEXT,
    diabetesMed TEXT,
    readmitted TEXT
);

CREATE INDEX idx_raw_patient_nbr ON raw_diabetic_encounters (patient_nbr);
CREATE INDEX idx_raw_readmitted ON raw_diabetic_encounters (readmitted);
