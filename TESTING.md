# Testing Plan

1. Run `python -m streamlit run app.py`.
2. Visit every navigation page.
3. Confirm sample records appear in Dashboard.
4. Change category/date filters and verify totals update.
5. Test positive, negative, and neutral text.
6. Switch sentiment methods.
7. Generate a weekly report for a week containing records.
8. Download the report and analyzed CSV.
9. Upload a compatible CSV.
10. Test missing dates, duplicate records, and unknown categories.

| Test | Expected result | Actual result | Status |
|---|---|---|---|
| App starts | Home page opens | Fill after testing | Pending |
| Filters | Metrics respond | Fill after testing | Pending |
| Analyzer | Displays a label | Fill after testing | Pending |
| Weekly report | Download available | Fill after testing | Pending |

Do not mark tests as passed until you have run them.
