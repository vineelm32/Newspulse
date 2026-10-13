# Methodology

1. **Data input:** read bundled or uploaded CSV data.
2. **Cleaning:** normalize columns, map aliases, remove empty text and duplicates, parse dates.
3. **Sentiment scoring:** VADER (NLTK), TextBlob, or a simple fallback lexicon.
4. **Aggregation:** use Pandas to group predictions by category and date.
5. **Visualization:** use Matplotlib and Streamlit charts.
6. **Weekly reporting:** summarize a selected seven-day period and allow download.
7. **Evaluation:** valid evaluation needs labeled reference data and accuracy, precision, recall, F1-score, and a confusion matrix. This version does not perform supervised training or claim validated accuracy.
