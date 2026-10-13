import re
from datetime import date, timedelta
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "news.csv"
st.set_page_config(page_title="NewsPulse", page_icon="📰", layout="wide")
st.markdown("""<style>
.block-container{max-width:1400px;padding-top:1.5rem}
.hero{padding:2rem;border-radius:20px;background:linear-gradient(120deg,#10243a,#17557c,#1596a0);color:white}
.hero h1{color:white;font-size:3rem}.hero p{color:#e8f7ff;font-size:1.1rem}
div[data-testid="stMetric"]{background:#f3f8fb;padding:14px;border-radius:12px;border:1px solid #dfebf2}
</style>""", unsafe_allow_html=True)

def load_data():
    try:
        df = pd.read_csv(DATA)
    except Exception:
        df = pd.DataFrame(columns=["date","category","headline","text","source","url"])
    df.columns = [str(c).lower().strip().replace(" ","_") for c in df.columns]
    aliases={"title":"headline","content":"text","section":"category","published_date":"date","published":"date","link":"url"}
    df=df.rename(columns={c:aliases[c] for c in df.columns if c in aliases})
    if "headline" not in df and "text" in df: df["headline"]=df["text"]
    if "text" not in df and "headline" in df: df["text"]=df["headline"]
    defaults={"date":str(date.today()),"category":"Uncategorized","headline":"","text":"","source":"Unknown","url":""}
    for c,v in defaults.items():
        if c not in df: df[c]=v
    df["date"]=pd.to_datetime(df["date"],errors="coerce").dt.date
    for c in ["category","headline","text","source","url"]:
        df[c]=df[c].fillna("").astype(str)
    df=df[(df.headline.str.strip()!="")|(df.text.str.strip()!="")]
    return df.drop_duplicates(subset=["headline","text"]).reset_index(drop=True)

def score(text, method):
    text=str(text or "")
    if method=="VADER (NLTK)":
        try:
            from nltk.sentiment import SentimentIntensityAnalyzer
            try: sia=SentimentIntensityAnalyzer()
            except LookupError:
                import nltk
                nltk.download("vader_lexicon",quiet=True)
                sia=SentimentIntensityAnalyzer()
            s=float(sia.polarity_scores(text)["compound"])
            return ("Positive" if s>=.05 else "Negative" if s<=-.05 else "Neutral",s)
        except Exception: pass
    if method=="TextBlob":
        try:
            from textblob import TextBlob
            s=float(TextBlob(text).sentiment.polarity)
            return ("Positive" if s>.05 else "Negative" if s<-.05 else "Neutral",s)
        except Exception: pass
    pos=set("good great strong growth success improve improved profit profits record exceed positive win victory excellent rise rising boost".split())
    neg=set("bad poor weak decline loss losses negative crisis risk threat fall falling defeat fail failed warning debt inflation corruption violence disaster".split())
    words=re.findall(r"[a-z']+",text.lower()); raw=max(-1,min(1,(sum(w in pos for w in words)-sum(w in neg for w in words))/max(1,len(words)**.5)))
    return ("Positive" if raw>.08 else "Negative" if raw<-.08 else "Neutral",float(raw))

if "custom_df" not in st.session_state: st.session_state.custom_df=None
st.sidebar.title("📰 NewsPulse")
page=st.sidebar.radio("Navigate",["Home","Dashboard","Live Analyzer","Category Analysis","Weekly Reports","How It Works","Technologies","Model & Results","About & Team"])
method=st.sidebar.selectbox("Sentiment method",["VADER (NLTK)","TextBlob","Fallback lexicon"])
upload=st.sidebar.file_uploader("Upload news CSV",type=["csv"])
if upload:
    try: st.session_state.custom_df=pd.read_csv(upload)
    except Exception as e: st.sidebar.error(str(e))
raw=st.session_state.custom_df.copy() if st.session_state.custom_df is not None else load_data()
if not raw.empty:
    raw.columns=[str(c).lower().strip().replace(" ","_") for c in raw.columns]
    aliases={"title":"headline","content":"text","section":"category","published_date":"date","published":"date","link":"url"}
    raw=raw.rename(columns={c:aliases[c] for c in raw.columns if c in aliases})
    for c,v in {"date":str(date.today()),"category":"Uncategorized","headline":"","text":"","source":"Unknown","url":""}.items():
        if c not in raw: raw[c]=v
    raw["date"]=pd.to_datetime(raw["date"],errors="coerce").dt.date
    for c in ["category","headline","text","source","url"]: raw[c]=raw[c].fillna("").astype(str)
    labels=[]; scores=[]
    for t in (raw["headline"]+". "+raw["text"]).tolist():
        lab,sc=score(t,method); labels.append(lab); scores.append(sc)
    raw["sentiment"]=labels; raw["sentiment_score"]=scores
df=raw

if page=="Home":
    st.markdown('<div class="hero"><h1>NewsPulse</h1><p><b>Understand the news beyond the headlines.</b><br>News Sentiment Data Science Pipeline · Project 08</p><p>Analyze political, economic, and sports news; explore sentiment patterns; and create weekly summaries.</p></div>',unsafe_allow_html=True)
    st.write("")
    st.subheader("The problem")
    st.write("Media teams may receive more articles than they can manually review. NewsPulse demonstrates a repeatable pipeline to estimate language sentiment and summarize trends across categories.")
    a,b,c=st.columns(3); a.markdown("### 🧹 Process\nClean and organize news records."); b.markdown("### 🧠 Analyze\nEstimate positive, neutral, or negative sentiment."); c.markdown("### 📊 Explore\nCompare categories and create weekly reports.")
    st.subheader("Project features")
    st.markdown("- Multi-page project information\n- Interactive sentiment dashboard\n- Text sentiment analyzer\n- Category-wise comparisons\n- Weekly report download\n- CSV upload and export")
    st.info("Sentiment is a language estimate, not fact-checking or verified public opinion.")
elif page=="Dashboard":
    st.title("📊 Sentiment Dashboard")
    if df.empty: st.warning("No data loaded. Check data/news.csv or upload a CSV.")
    else:
        cats=sorted(df.category.unique().tolist()); selected=st.multiselect("Categories",cats,default=cats)
        view=df[df.category.isin(selected)].copy()
        valid=view.date.dropna()
        if not valid.empty:
            dr=st.date_input("Date range",(min(valid),max(valid)))
            if isinstance(dr,tuple) and len(dr)==2: view=view[view.date.notna()&(view.date>=dr[0])&(view.date<=dr[1])]
        total=len(view); counts=view.sentiment.value_counts()
        cols=st.columns(4)
        for col,label in zip(cols,["Articles","Positive","Neutral","Negative"]): col.metric(label,total if label=="Articles" else int(counts.get(label,0)))
        left,right=st.columns(2)
        with left:
            st.subheader("Sentiment distribution"); fig,ax=plt.subplots(); counts.reindex(["Positive","Neutral","Negative"],fill_value=0).plot(kind="bar",ax=ax); ax.set_ylabel("Articles"); st.pyplot(fig); plt.close(fig)
        with right:
            st.subheader("By category"); ct=pd.crosstab(view.category,view.sentiment).reindex(columns=["Positive","Neutral","Negative"],fill_value=0); fig,ax=plt.subplots(); ct.plot(kind="bar",stacked=True,ax=ax); ax.set_ylabel("Articles"); st.pyplot(fig); plt.close(fig)
        dated=view.dropna(subset=["date"]).copy()
        if not dated.empty:
            dated["week"]=pd.to_datetime(dated.date).dt.to_period("W").astype(str)
            st.subheader("Weekly trend"); st.line_chart(dated.groupby(["week","sentiment"]).size().unstack(fill_value=0))
        st.dataframe(view[["date","category","headline","source","sentiment","sentiment_score"]],use_container_width=True,hide_index=True)
        st.download_button("Download analyzed CSV",view.to_csv(index=False).encode(), "newspulse_analyzed.csv","text/csv")
elif page=="Live Analyzer":
    st.title("🔍 Live News Sentiment Analyzer")
    txt=st.text_area("Paste a headline or article paragraph",height=170,placeholder="The company reported record profits, but analysts warned about rising debt.")
    if st.button("Analyze sentiment",type="primary"):
        if not txt.strip(): st.warning("Enter text first.")
        else:
            lab,sc=score(txt,method); a,b,c=st.columns(3); a.metric("Predicted sentiment",lab); b.metric("Score",f"{sc:.3f}"); c.metric("Method",method)
            st.caption("The score is not necessarily a probability. Predictions estimate language polarity, not factual accuracy.")
elif page=="Category Analysis":
    st.title("🗂️ Category Analysis")
    if df.empty: st.warning("Load a dataset first.")
    else:
        ct=pd.crosstab(df.category,df.sentiment); st.dataframe(ct,use_container_width=True); st.bar_chart(ct)
        for cat,sub in df.groupby("category"):
            st.write(f"**{cat}:** {len(sub)} articles; most common predicted sentiment: **{sub.sentiment.value_counts().idxmax()}**.")
elif page=="Weekly Reports":
    st.title("📅 Weekly Summary Reports")
    if df.empty or df.date.dropna().empty: st.warning("A dataset with valid dates is required.")
    else:
        latest=max(df.date.dropna()); start=st.date_input("Week start date",latest-timedelta(days=6)); end=start+timedelta(days=6)
        view=df[df.date.notna()&(df.date>=start)&(df.date<=end)]; counts=view.sentiment.value_counts().reindex(["Positive","Neutral","Negative"],fill_value=0)
        report=f"# NewsPulse Weekly Report\\nPeriod: {start} to {end}\\nArticles: {len(view)}\\n\\n"+counts.to_string()+"\\n\\nCategory-wise counts:\\n"+pd.crosstab(view.category,view.sentiment).to_string()+"\\n\\nThese are sentiment estimates, not fact checks."
        st.text_area("Report preview",report,height=260); st.download_button("Download weekly report",report.encode(),"newspulse_weekly_report.txt","text/plain")
        st.dataframe(pd.crosstab(view.category,view.sentiment),use_container_width=True)
elif page=="How It Works":
    st.title("⚙️ How It Works")
    for title,body in [("1. Data input","Load the bundled dataset or upload a CSV."),("2. Cleaning","Normalize columns, parse dates, remove duplicates."),("3. Sentiment scoring","Use VADER, TextBlob, or the built-in fallback scorer."),("4. Aggregation","Group predictions by category and date with Pandas."),("5. Visualization","Display charts and trends."),("6. Reporting","Generate a downloadable weekly summary.")]:
        with st.expander(title,expanded=True): st.write(body)
    st.warning("The current version uses lexicon-based scoring; it does not train a supervised model or verify news claims.")
elif page=="Technologies":
    st.title("🧰 Technologies Used")
    for name,desc in [("Python","Main programming language."),("Pandas","Data cleaning and aggregation."),("NLTK / VADER","Lexicon-based sentiment scoring."),("TextBlob","Alternative text polarity scoring."),("Matplotlib","Charts."),("Streamlit","Interactive web application."),("CSV","Data input and export."),("GitHub","Source-code version control and collaboration.")]:
        st.subheader(name); st.write(desc); st.divider()
elif page=="Model & Results":
    st.title("🧪 Model & Results")
    st.write("The current version uses lexicon-based sentiment scoring, not a supervised trained model.")
    st.markdown("Evaluation requires labeled reference data and a comparison using accuracy, precision, recall, F1-score, and a confusion matrix.")
    if not df.empty: st.bar_chart(df.sentiment.value_counts())
    st.info("Prediction counts are not accuracy. Accuracy requires known correct labels.")
elif page=="About & Team":
    st.title("👥 About NewsPulse")
    st.write("A college-level Data Science project to explore sentiment patterns across political, economic, and sports news.")
    st.subheader("Objectives"); st.markdown("- Process news text\n- Estimate sentiment\n- Compare categories and dates\n- Visualize findings\n- Generate weekly summaries")
    st.subheader("Team"); st.write("Add your five team members and responsibilities before submission.")
    st.subheader("Limitations"); st.write("Sentiment tools may miss sarcasm and context. Results depend on the dataset and scoring method. Sentiment analysis is not fact-checking.")
st.sidebar.caption("NewsPulse · Student Data Science Project")
