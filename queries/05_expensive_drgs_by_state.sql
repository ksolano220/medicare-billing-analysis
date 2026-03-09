-- Most expensive DRGs by state (average charges)
-- Useful for identifying geographic cost variation in specific procedures
-- Only includes DRGs with sufficient volume for reliable comparison

WITH ranked AS (
    SELECT
        provider_state,
        drg_code,
        drg_description,
        SUM(total_discharges)              AS total_discharges,
        ROUND(AVG(avg_covered_charges), 2) AS avg_charges,
        ROUND(AVG(avg_medicare_payments), 2) AS avg_medicare_payment,
        ROW_NUMBER() OVER (
            PARTITION BY provider_state
            ORDER BY AVG(avg_covered_charges) DESC
        ) AS rank_in_state
    FROM inpatient_charges
    GROUP BY provider_state, drg_code, drg_description
    HAVING total_discharges >= 50
)
SELECT
    provider_state,
    drg_code,
    drg_description,
    total_discharges,
    avg_charges,
    avg_medicare_payment
FROM ranked
WHERE rank_in_state <= 5
ORDER BY provider_state, rank_in_state;
