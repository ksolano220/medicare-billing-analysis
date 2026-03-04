-- Average hospital charge markup by state
-- Compares what hospitals bill vs what Medicare actually pays
-- Markup ratio = charges / payments — higher means bigger gap

SELECT
    provider_state,
    COUNT(DISTINCT provider_id)                          AS num_hospitals,
    SUM(total_discharges)                                AS total_discharges,
    ROUND(AVG(avg_covered_charges), 2)                   AS avg_charges,
    ROUND(AVG(avg_medicare_payments), 2)                 AS avg_medicare_payment,
    ROUND(AVG(avg_covered_charges) / NULLIF(AVG(avg_medicare_payments), 0), 2) AS markup_ratio
FROM inpatient_charges
GROUP BY provider_state
HAVING num_hospitals >= 5
ORDER BY markup_ratio DESC;
