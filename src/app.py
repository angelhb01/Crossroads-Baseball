import requests
from features import elo_ratings
import streamlit as st
from scrape import scrape_data

api_url = 'http://localhost:8000/predict' # Local

st.title("Crossroads Baseball Results")

st.header("Press the button to start scraping latest data")

# Initialize session state variables if they don't exist yet
if "df" not in st.session_state:
    st.session_state.df = None

# Clicking "Scrape" saves the data into memory and sets up the app
if st.button("Scrape"):
    st.session_state.df = scrape_data()

# Checks if we have data in memory. If we do, show the rest of the app
if st.session_state.df is not None:
    df = st.session_state.df # Use the saved dataframe

    st.subheader("Data Preview")
    st.write(df.head())

    st.subheader("Summary")
    st.write(df.describe())

    st.subheader("Filter Games")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Select column to filter by", columns)
    unique_values = df[selected_column].unique()
    selected_value = st.selectbox("Select value", unique_values)

    filtered_df = df[df[selected_column] == selected_value]
    st.write(filtered_df)

    st.subheader("Generate Elo Rankings")
    if st.button("Calculate Elo Rankings"):
        st.write("Calculating...")
        #res = requests.post(api_url, df)
        elo_df = elo_ratings(df)
        st.write("Calculated")
        st.write(df)

        st.subheader("Data Plot")
        st.line_chart(elo_df.set_index("date")["home_elo_pre"])