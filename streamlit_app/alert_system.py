import streamlit as st


def send_alert(aqi):
    if aqi > 100:  # Example threshold
        st.warning("Unhealthy Air Quality!")
    elif aqi > 50:
        st.info("Moderate Air Quality")
    else:
        st.success("Good Air Quality")
