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

    elo_df = elo_ratings(df)
    st.header("Elo Calculations")
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
    if "pred" not in st.session_state:
        st.session_state.pred = None
    st.subheader("Make a Prediction")
    away_teams = elo_df["away"].unique()
    home_teams = elo_df["home"].unique()

    # Away team name
    away_team = st.selectbox("Select away team to filter by", away_teams)
    # Home team name
    home_team = st.selectbox("Select home team to filter by", home_teams)
    # Elo rating for the away team
    away_elo_pre = st.number_input("Enter an elo rating for the away team", min_value=0.0, value=1500.0)
    # Elo rating for the home team
    home_elo_pre = st.number_input("Enter an elo rating for the home team", min_value=0.0, value=1300.0)
    # Elo probability for the away team
    elo_prob_away = st.number_input("Enter a probability for the away team to win", min_value=0.0, max_value=1.0, value=0.40)
    # Elo probability for the home team
    elo_prob_home = st.number_input("Enter a probability for the home team to win", min_value=0.0, max_value=1.0, value=0.50)

    if st.button("Predict"):
        st.write("Calculating")
        input_data = {
            "away_team": away_team,
            "home_team": home_team,
            "away_elo_pre": away_elo_pre,
            "home_elo_pre": home_elo_pre,
            "elo_prob_away": elo_prob_away,
            "elo_prob_home": elo_prob_home,
        }
        try:
            response = requests.post(api_url, json=input_data)
            if response.status_code == 200:
                st.session_state.pred = response.json()
            else:
                st.write(f"API Error: {response.status_code}")
        except Exception as e:
            st.write("An error has occurred")
            print(f"An error when sending a post request: {e}")
    if st.session_state.pred is not None:
        prediction_val = st.session_state.pred.get("prediction")

        if prediction_val == 0:
            st.write("Home team is likely to lose")
        else:
            st.write("Home team is likely to win")