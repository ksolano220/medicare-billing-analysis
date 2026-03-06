-- Billing patterns: rural vs urban hospitals
-- Uses RUCA (Rural-Urban Commuting Area) codes to classify
-- RUCA 1-3 = urban/metro, 4-6 = suburban, 7-10 = rural

SELECT
    CASE
        WHEN CAST(provider_ruca AS REAL) BETWEEN 1 AND 3 THEN 'Urban/Metro'
        WHEN CAST(provider_ruca AS REAL) BETWEEN 4 AND 6 THEN 'Suburban'
        WHEN CAST(provider_ruca AS REAL) >= 7              THEN 'Rural'
        ELSE 'Unknown'
    END AS location_type,
    COUNT(DISTINCT provider_id)                  AS num_hospitals,
    SUM(total_discharges)                        AS total_discharges,
    ROUND(AVG(avg_covered_charges), 2)           AS avg_charges,
    ROUND(AVG(avg_total_payments), 2)            AS avg_total_payment,
    ROUND(AVG(avg_medicare_payments), 2)         AS avg_medicare_payment,
    ROUND(AVG(avg_covered_charges) / NULLIF(AVG(avg_medicare_payments), 0), 2) AS markup_ratio,
    ROUND(AVG(total_discharges), 1)              AS avg_discharges_per_record
FROM inpatient_charges
WHERE provider_ruca IS NOT NULL
GROUP BY location_type
ORDER BY location_type;
