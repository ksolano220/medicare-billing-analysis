-- Top 20 diagnosis groups by total discharge volume nationally
-- Shows which conditions drive the most inpatient hospital utilization

SELECT
    drg_code,
    drg_description,
    SUM(total_discharges)                       AS total_discharges,
    COUNT(DISTINCT provider_id)                  AS num_hospitals,
    ROUND(AVG(avg_covered_charges), 2)           AS avg_charges,
    ROUND(AVG(avg_medicare_payments), 2)         AS avg_medicare_payment,
    ROUND(AVG(avg_covered_charges) - AVG(avg_medicare_payments), 2) AS avg_charge_gap
FROM inpatient_charges
GROUP BY drg_code, drg_description
ORDER BY total_discharges DESC
LIMIT 20;
