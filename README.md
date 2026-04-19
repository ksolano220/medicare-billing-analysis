## Medicare Billing Analysis

### Problem
Hospital billing in the US varies dramatically by provider, region, and procedure. This project analyzes CMS Medicare inpatient claims data to identify billing patterns, cost outliers, and geographic disparities in healthcare pricing.

### Data Source
[CMS Medicare Inpatient Hospitals — by Provider and Service (FY2022)](https://data.cms.gov/provider-summary-by-type-of-service/medicare-inpatient-hospitals/medicare-inpatient-hospitals-by-provider-and-service)

- 145,000+ records across 3,000+ hospitals and 533 diagnosis groups (DRGs)
- Covers all 50 states + DC
- Fields include submitted charges, Medicare payments, and discharge volume

### Analysis

Six SQL queries explore different dimensions of the billing data:

| Query | Description |
|-------|-------------|
| `01_top_drgs_by_volume.sql` | Top 20 diagnosis groups by discharge volume nationally |
| `02_state_markup_analysis.sql` | Average charge-to-payment markup ratio by state |
| `03_cost_outlier_hospitals.sql` | Hospitals charging 3x+ the national average for the same procedures |
| `04_rural_vs_urban_billing.sql` | Billing pattern comparison across rural, suburban, and urban hospitals |
| `05_expensive_drgs_by_state.sql` | Top 5 most expensive procedures per state |
| `06_payment_gap_trends.sql` | DRGs with the widest gap between billed charges and Medicare payments |

### Key Findings
- **Markup ratios vary 3x across states.** Nevada hospitals charge 10x what Medicare pays on average, while Maryland charges under 2x. State-level reimbursement policy, not facility economics, appears to be the strongest driver of variance.
- **Cost outliers are concentrated.** Stanford Health Care bills up to 17x the national average for certain procedures. A small set of academic and specialty centers account for the bulk of extreme markups, which suggests negotiation leverage rather than cost recovery.
- **Rural hospitals charge less.** 4.1x markup vs 5.8x for urban, but serve fewer patients per facility. Rural pricing constraints are real but do not offset the volume disadvantage for a sustainable model.
- **Septicemia drives the most volume.** 550k discharges nationally, with a $57k average gap between charges and payments. Sepsis care is a structural loss leader for US hospitals.

### How to Run

```bash
pip install -r requirements.txt

# Download CMS data (~24 MB CSV)
python src/download_data.py

# Load into SQLite database
python src/load_db.py

# Run all queries and save results
python src/run_analysis.py
```

Results are saved as CSVs in `outputs/`.

### Tools Used
- Python, SQLite
- SQL (CTEs, window functions, aggregations)
- CMS Medicare public data
