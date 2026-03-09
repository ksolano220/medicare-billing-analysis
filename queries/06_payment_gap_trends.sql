-- Payment gap analysis: where Medicare pays the least relative to charges
-- Highlights DRGs where the gap between billed and paid is widest
-- This gap often indicates areas of billing inefficiency or inflated charges

SELECT
    drg_code,
    drg_description,
    SUM(total_discharges)                                AS total_discharges,
    ROUND(AVG(avg_covered_charges), 2)                   AS avg_charges,
    ROUND(AVG(avg_medicare_payments), 2)                 AS avg_medicare_payment,
    ROUND(AVG(avg_covered_charges) - AVG(avg_medicare_payments), 2) AS payment_gap,
    ROUND(
        (AVG(avg_covered_charges) - AVG(avg_medicare_payments))
        / NULLIF(AVG(avg_covered_charges), 0) * 100,
        1
    ) AS gap_pct
FROM inpatient_charges
GROUP BY drg_code, drg_description
HAVING total_discharges >= 100
ORDER BY payment_gap DESC
LIMIT 25;
