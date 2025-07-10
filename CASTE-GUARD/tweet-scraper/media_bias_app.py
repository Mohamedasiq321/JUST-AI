import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.set_page_config(page_title="CASTE-GUARD Dashboard", layout="wide")

st.title("🛡️ CASTE-GUARD - Hate, Bias & Media Watch Dashboard")
st.markdown("Tracking caste-based hate, discrimination & media bias in real-time tweets and news.")

# 🔄 SIDEBAR: Select Page
page = st.sidebar.radio("📂 Select Section", [
    "📄 Tweet Analysis",
    "📰 News Bias Detection",
    "⚖️ Fairness & Sentiment"
])

# ------------------- 📄 TWEET ANALYSIS -------------------
if page == "📄 Tweet Analysis":
    st.header("📄 Tweet Hate & Intent Analysis")
    try:
        with open("analyzed_tweets.json", "r", encoding="utf-8") as f:
            tweets_data = json.load(f)
        df = pd.DataFrame(tweets_data)
        df["hate_score"] = df["hate_score"].astype(float)
        df["intent"] = df["intent"].astype(str)

        st.sidebar.subheader("📊 Filters")
        min_score = st.sidebar.slider("Minimum Hate Score", 0.0, 1.0, 0.5, 0.01)
        intent_filter = st.sidebar.multiselect("Intent Filter", df["intent"].unique(), default=list(df["intent"].unique()))

        filtered = df[(df["hate_score"] >= min_score) & (df["intent"].isin(intent_filter))]
        st.success(f"🎯 Showing {len(filtered)} filtered tweets")

        st.dataframe(filtered[["text", "hate_score", "intent"]], use_container_width=True)

        if not filtered.empty:
            fig = px.pie(filtered, names="intent", title="🧠 Intent Breakdown")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("⚠️ No tweets matched the filter.")

    except Exception as e:
        st.error("❌ Couldn't load analyzed_tweets.json")
        st.exception(e)

# ------------------- 📰 NEWS BIAS DETECTION -------------------
elif page == "📰 News Bias Detection":
    st.header("📰 Caste-Based News Bias Detection")
    try:
        df = pd.read_csv("flagged_news_bias.csv")
        st.subheader("📄 News Bias Results")
        st.write("Detected Columns:", df.columns.tolist())
        st.success(f"✅ Found {len(df)} caste-biased news articles")

        if all(col in df.columns for col in ["title", "source", "bias_reason"]):
            st.dataframe(df[["title", "source", "bias_reason"]])
            fig = px.pie(df, names="bias_reason", title="📊 News Bias Categories")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Expected columns (title, source, bias_reason) not found.")

    except Exception as e:
        st.warning("⚠️ No biased news data found.")
        st.exception(e)

# ------------------- ⚖️ FAIRNESS & SENTIMENT -------------------
elif page == "⚖️ Fairness & Sentiment":
    st.header("⚖️ Tweet Fairness & Sentiment Breakdown")
    try:
        df = pd.read_csv("flagged_tweet_bias.csv")
        st.subheader("📄 Fairness Detection Results")
        st.write("Detected Columns:", df.columns.tolist())
        st.success(f"✅ Found {len(df)} biased caste-related tweets")

        if all(col in df.columns for col in ["text", "bias_flag", "fairness_score"]):
            st.dataframe(df[["text", "bias_flag", "fairness_score"]])
        else:
            st.warning("⚠️ Expected columns (text, bias_flag, fairness_score) not found.")

        if "sentiment" in df.columns:
            fig = px.pie(df, names="sentiment", title="🎭 Sentiment Breakdown")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ No sentiment data found to plot.")

    except Exception as e:
        st.warning("⚠️ No tweet fairness/sentiment data found.")
        st.exception(e)
