# 📰 NewsPulse — News Sentiment Data Science Pipeline

> **Understand the news beyond the headlines.** A college-level Data Science project for exploring sentiment patterns across political, economic, and sports news.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458)
![NLP](https://img.shields.io/badge/NLP-Sentiment%20Analysis-16a085)
![Streamlit](https://img.shields.io/badge/Interface-Streamlit-ff4b4b)

## Project overview
NewsPulse processes news text and estimates whether its language expresses **positive, neutral, or negative sentiment**. It summarizes results by category and date, visualizes patterns, and creates weekly reports.

## Problem statement
A media analytics company wants to understand sentiment trends across political, economic, and sports news. Manually reviewing every article is slow; NewsPulse demonstrates a repeatable pipeline for processing news text and summarizing sentiment.

## Objectives
- Treat news articles as structured data.
- Clean and normalize news records.
- Apply sentiment scoring to headlines and article text.
- Compare political, economic, and sports news.
- Visualize distributions and trends.
- Generate downloadable weekly summaries.
- Explain methods and limitations transparently.

## Features
- Multi-page project website and technical explanations.
- Interactive dashboard with category/date filters.
- Live text sentiment analyzer.
- Category-wise comparisons.
- Weekly report generation and download.
- CSV upload and export.
- VADER (NLTK), TextBlob, and fallback scoring options.

## Technologies
| Technology | Role |
|---|---|
| Python | Main programming language |
| Pandas | Data cleaning, filtering, grouping, and summaries |
| NLTK / VADER | Lexicon-based sentiment scoring option |
| TextBlob | Alternative polarity-based scoring |
| Matplotlib | Visualizations |
| Streamlit | Interactive web application |
| CSV | Data input/output |
| Git / GitHub | Version control and collaboration |

## Workflow
```text
News dataset / uploaded CSV
          |
          v
Data validation and cleaning
          |
          v
Headline + article text
          |
          v
Sentiment scoring (selected method)
          |
          v
Positive / Neutral / Negative label
          |
          v
Aggregation by category and date
          |
          v
Charts, filters, and weekly report
```

## Repository structure
```text
NewsPulse/
├── app.py
├── requirements.txt
├── README.md
├── data/news.csv
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── METHODOLOGY.md
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── TESTING.md
│   ├── RESULTS.md
│   └── VIVA_QUESTIONS.md
└── assets/screenshots/
```

## Run locally
Install dependencies:
```bash
python -m pip install -r requirements.txt
```
Run:
```bash
python -m streamlit run app.py
```

## Dataset format
The bundled CSV is demonstration data. Compatible fields are `date`, `category`, `headline`, `text`, and optional `source`, `url`. Common aliases such as `title`, `content`, `section`, `published_date`, and `link` are supported.

## Evaluation and limitations
Dashboard counts and percentages summarize predictions; they are **not accuracy measurements**. Proper evaluation requires a labeled reference dataset and metrics such as accuracy, precision, recall, F1-score, and a confusion matrix. This version does not train a supervised model and does not claim validated accuracy.

Sentiment estimates do not establish whether a news claim is true or measure public opinion. Sarcasm, context, and domain-specific language may affect results.

## Live news collection
Automated live RSS collection is a future enhancement and is **not implemented in the current code**. The current app analyzes bundled data or a CSV uploaded by the user.

## Future enhancements
- Add permitted RSS feed collection with source attribution.
- Evaluate scoring methods on a labeled dataset.
- Improve contextual NLP and mixed-sentiment handling.
- Automate scheduled reports.
- Add more automated tests.

## Team
Add the five team members' names and responsibilities before submission.

## Documentation
- [Project Overview](docs/PROJECT_OVERVIEW.md)
- [Methodology](docs/METHODOLOGY.md)
- [System Architecture](docs/SYSTEM_ARCHITECTURE.md)
- [Testing Plan](docs/TESTING.md)
- [Results and Limitations](docs/RESULTS.md)
- [Viva Questions](docs/VIVA_QUESTIONS.md)
