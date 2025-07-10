import streamlit as st
import os
import pandas as pd
import json
import plotly.express as px

# Page config
st.set_page_config(page_title="CASTE-GUARD Dashboard", layout="wide")

st.title("🛡️ CASTE-GUARD - Hate & Intent Detection Dashboard")
st.caption("Tracking caste-based hate, discrimination & bias in real-time tweets.")

# Load JSON
try:
    with open("analyzed_tweets.json", "r", encoding="utf-8") as f:
        full_data = json.load(f)
        st.success("✅ analyzed_tweets.json loaded successfully!")

    # DEBUG preview
    st.subheader("🔍 Raw JSON Structure")
    st.json(full_data[:2] if isinstance(full_data, list) else full_data.get("data", [])[:2])

    # Flexible data structure support
    if isinstance(full_data, list):
        tweets_data = full_data
    elif "data" in full_data:
        tweets_data = full_data["data"]
    else:
        raise KeyError("Missing 'data' key in JSON")

except Exception as e:
    st.error("❌ Couldn't load analyzed_tweets.json")
    st.exception(e)
    st.stop()

# DataFrame conversion
df = pd.DataFrame(tweets_data)

# Check columns before casting
if "hate_score" not in df.columns:
    st.error("❗ 'hate_score' column not found in data!")
    st.stop()

df["hate_score"] = df["hate_score"].astype(float)
df["text"] = df["text"].astype(str)

if "intent" in df.columns:
    df["intent"] = df["intent"].astype(str)
else:
    df["intent"] = "unknown"

# Filters
st.sidebar.header("📊 Filters")
min_score = st.sidebar.slider("Minimum Hate Score", 0.0, 1.0, 0.5, 0.01)
intent_filter = st.sidebar.multiselect("Intent Filter", options=df["intent"].unique(), default=list(df["intent"].unique()))

filtered = df[(df["hate_score"] >= min_score) & (df["intent"].isin(intent_filter))]

st.success(f"🎯 Showing {len(filtered)} filtered tweets")

# Table view
st.dataframe(filtered[["text", "hate_score", "intent"]].reset_index(drop=True), use_container_width=True)

# Download
csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download Filtered Tweets", csv, "filtered_tweets.csv", "text/csv")

# 📊 Charts
st.subheader("📊 Hate Score Distribution")
fig = px.histogram(filtered, x="hate_score", nbins=20, title="Hate Score Frequency", color_discrete_sequence=["firebrick"])
st.plotly_chart(fig, use_container_width=True)

st.subheader("🧠 Intent Distribution")
intent_count = filtered["intent"].value_counts().reset_index()
intent_count.columns = ["intent", "count"]
fig2 = px.pie(intent_count, names="intent", values="count", title="Tweet Intent Pie Chart")
st.plotly_chart(fig2, use_container_width=True)
