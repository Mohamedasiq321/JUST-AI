import streamlit as st

st.set_page_config(page_title="Tab Test", layout="wide")

st.title("🔍 Streamlit Tabs Test")

tab1, tab2, tab3 = st.tabs(["Tab 1: Tweets", "Tab 2: News", "Tab 3: Bias"])

with tab1:
    st.write("📄 This is the Tweet Analysis tab.")

with tab2:
    st.write("📰 This is the News Bias tab.")

with tab3:
    st.write("⚖️ This is the Fairness tab.")
