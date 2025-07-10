import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.set_page_config(page_title="CASTE-GUARD Dashboard", layout="wide")

st.title("🛡️ CASTE-GUARD - Hate, Bias & Media Watch Dashboard")
st.markdown("Tracking caste-based hate, discrimination & bias in real-time tweets and news.")

# Tabs
tab1, tab2, tab3 = st.tabs(["📄 Tweet Analysis", "📰 News Bias Detection", "⚖️ Fairness & Sentiment"])

# Tab 1
with tab1:
    st.header("📄 Tweet Hate & Intent Analysis")
    try:
        with open("analyzed_tweets.json", "r", encoding="utf-8") as f:
            tweets_data = json.load(f)
        df = pd.DataFrame(tweets_data)
        df["hate_score"] = df["hate_score"].astype(float)
        df["intent"] = df["intent"].astype(str)

        min_score = st.slider("📊 Minimum Hate Score", 0.0, 1.0, 0.5, 0.01)
        intent_filter = st.multiselect("🧠 Intent Filter", df["intent"].unique(), default=list(df["intent"].unique()))

        filtered = df[(df["hate_score"] >= min_score) & (df["intent"].isin(intent_filter))]
        st.success(f"🎯 Showing {len(filtered)} filtered tweets")
        st.dataframe(filtered[["text", "hate_score", "intent"]])

        # Intent Pie Chart
        fig1 = px.pie(filtered, names="intent", title="🧠 Intent Breakdown")
        st.plotly_chart(fig1, use_container_width=True)

    except Exception as e:
        st.error("❌ Couldn't load analyzed_tweets.json")
        st.exception(e)

# Tab 2
with tab2:
    st.header("📰 Caste-Based News Bias Detection")
    try:
        bias_df = pd.read_csv("flagged_news_bias.csv")
        st.success(f"✅ Found {len(bias_df)} caste-biased news articles")
        st.dataframe(bias_df[["title", "source", "bias_reason"]], use_container_width=True)

        fig2 = px.pie(bias_df, names='bias_reason', title="📊 News Bias Categories")
        st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.warning("⚠️ No biased news data available.")
        st.exception(e)

# Tab 3
with tab3:
    st.header("⚖️ Fairness & Sentiment Breakdown")
    try:
        tweet_bias_df = pd.read_csv("flagged_tweet_bias.csv")
        st.success(f"✅ Found {len(tweet_bias_df)} biased caste-related tweets")
        st.dataframe(tweet_bias_df[["text", "bias_flag", "fairness_score"]], use_container_width=True)

        if "sentiment" in tweet_bias_df.columns:
            fig3 = px.pie(tweet_bias_df, names='sentiment', title="🎭 Sentiment Breakdown")
            st.plotly_chart(fig3, use_container_width=True)
    except Exception as e:
        st.warning("⚠️ No tweet fairness/sentiment data found.")
        st.exception(e)
