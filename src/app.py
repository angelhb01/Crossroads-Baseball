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
    st.write("This may take a while")
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

    if "elo_df" not in st.session_state:
        st.session_state.elo_df = None
    st.subheader("Generate Elo Rankings")
    if st.button("Calculate Elo Rankings"):
        st.write("Calculating...")
        st.session_state.elo_df = elo_ratings(df)
    if st.session_state.elo_df is not None:
        elo_df = st.session_state.elo_df
        st.write("Calculated")
        locations = ["home", "away"]
        selected_location = st.selectbox("Select location to filter by", locations)
        teams = elo_df[selected_location].unique()
        selected_team = st.selectbox("Select team to filter by", teams)

        st.subheader("Data Plot")
        st.line_chart(elo_df[elo_df[selected_location] == selected_team].set_index("date")["home_elo_pre"])

        st.header("Post Elo Ratings in Home Games")
        st.bar_chart(elo_df, x="home", y="home_elo_post")

        st.header("Post Elo Ratings in Away Games")
        st.bar_chart(elo_df, x="away", y="away_elo_post")

        # Next task: Continue with model prediction

        #res = requests.post(api_url, df)