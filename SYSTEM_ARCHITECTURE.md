# System Architecture

```text
CSV / user text → Input normalization → Cleaning → Sentiment scorer
        → Predicted label and score → Pandas aggregation
        → Dashboard / category analysis / weekly report / CSV export
```

Components: Streamlit UI, Pandas processing, sentiment-scoring functions, Matplotlib charts, and CSV data.

Current boundaries: single Streamlit application; no separate API server or database. Automated live RSS ingestion and supervised model training are not implemented.
