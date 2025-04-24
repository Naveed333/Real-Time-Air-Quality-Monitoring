import streamlit as st
import pandas as pd

data = pd.read_csv("data/predictions/today.csv")
st.title("Air Quality Dashboard")
st.map(data[["latitude", "longitude"]])
st.line_chart(data["predicted_aqi"])
