-- Feature engineering used by the readmission model.
-- These fields mirror python/03_feature_engineering.py and support the
-- dashboard risk-tier summaries.

CREATE TABLE readmission_features AS
SELECT
    *,
    number_outpatient + number_emergency + number_inpatient AS prior_visits_total,
    CASE WHEN number_inpatient >= 2 THEN 1 ELSE 0 END AS high_utilizer,
    CASE WHEN time_in_hospital >= 7 THEN 1 ELSE 0 END AS long_stay,
    CASE WHEN num_medications >= 15 THEN 1 ELSE 0 END AS many_meds,
    CASE WHEN change = 'Ch' THEN 1 ELSE 0 END AS med_changed
FROM fact_encounters;

SELECT
    CASE
        WHEN high_utilizer = 1 THEN 'High utilizer'
        WHEN long_stay = 1 THEN 'Long stay'
        WHEN many_meds = 1 THEN 'Medication complexity'
        ELSE 'Lower risk indicators'
    END AS risk_signal,
    COUNT(*) AS encounters,
    ROUND(100.0 * AVG(readmit_30), 1) AS readmit_30_rate_pct
FROM readmission_features
GROUP BY risk_signal
ORDER BY readmit_30_rate_pct DESC;
