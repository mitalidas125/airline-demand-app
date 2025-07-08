import streamlit as st
import pandas as pd
import requests

# Page settings
st.set_page_config(page_title="✈️ Airline Demand Tracker", layout="centered")
st.title("✈️ Airline Market Demand Web App")

# API setup
API_KEY = "52e257e56c2db4773ac60ab96af78102"
url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&limit=100"

st.info("📡 Fetching flight data from AviationStack API...")

try:
    response = requests.get(url)
    data = response.json()

    if "data" in data and data["data"]:
        routes = [
            (f['departure']['airport'], f['arrival']['airport'])
            for f in data['data']
            if f['departure']['airport'] and f['arrival']['airport']
        ]

        if routes:
            df = pd.DataFrame(routes, columns=["From", "To"])
            top_routes = df.value_counts().head(5).reset_index(name='Count')

            st.success("✅ Top 5 Flight Routes Found")
            st.dataframe(top_routes)

            st.subheader("📊 Route Frequency Chart")
            st.bar_chart(top_routes["Count"])
        else:
            st.warning("⚠️ No routes found in the current API response.")
    else:
        st.error("❌ Invalid or empty data received from the API.")
except Exception as e:
    st.error(f"🚨 Error occurred while fetching data: {e}")

