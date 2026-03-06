-- Hospitals charging significantly above the national average for common procedures
-- Flags potential billing outliers by comparing each hospital's charges
-- to the average for the same DRG

WITH drg_avg AS (
    SELECT
        drg_code,
        AVG(avg_covered_charges)   AS national_avg_charge,
        AVG(avg_medicare_payments) AS national_avg_payment
    FROM inpatient_charges
    GROUP BY drg_code
    HAVING COUNT(*) >= 20
)
SELECT
    ic.provider_name,
    ic.provider_city,
    ic.provider_state,
    ic.drg_code,
    ic.drg_description,
    ic.total_discharges,
    ROUND(ic.avg_covered_charges, 2)            AS hospital_charge,
    ROUND(da.national_avg_charge, 2)            AS national_avg_charge,
    ROUND(ic.avg_covered_charges / NULLIF(da.national_avg_charge, 0), 2) AS charge_multiple,
    ROUND(ic.avg_medicare_payments, 2)          AS hospital_medicare_pmt
FROM inpatient_charges ic
JOIN drg_avg da ON ic.drg_code = da.drg_code
WHERE ic.avg_covered_charges > da.national_avg_charge * 3
  AND ic.total_discharges >= 10
ORDER BY charge_multiple DESC
LIMIT 50;
