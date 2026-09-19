import requests
import streamlit as st
from features import elo_ratings
from scrape import scrape_data

api_url = 'http://localhost:8000/predict'

st.set_page_config(page_title='Crossroads Baseball Analytics', page_icon='⚾')
st.title('Crossroads Baseball Analytics')
st.caption('Web-scraped game data, Elo rankings, and ML-based win predictions.')

if 'df' not in st.session_state:
    st.session_state.df = None
if 'pred' not in st.session_state:
    st.session_state.pred = None

if st.button('Scrape latest data', use_container_width=True):
    st.write('This may take a moment while the latest games are collected.')
    st.session_state.df = scrape_data()
    st.session_state.pred = None

if st.session_state.df is not None:
    df = st.session_state.df

    st.subheader('Data preview')
    st.dataframe(df.head())

    st.subheader('Summary statistics')
    st.write(df.describe())

    st.subheader('Filter games')
    columns = df.columns.tolist()
    selected_column = st.selectbox('Select column to filter by', columns)
    selected_value = st.selectbox('Select value', df[selected_column].dropna().unique())
    filtered_df = df[df[selected_column] == selected_value]
    st.dataframe(filtered_df)

    elo_df = elo_ratings(df)
    st.header('Elo calculations')
    locations = ['home', 'away']
    selected_location = st.selectbox('Select location to filter by', locations)
    teams = elo_df[selected_location].unique()
    selected_team = st.selectbox('Select team to filter by', teams)

    st.subheader('Elo trend over time')
    st.line_chart(elo_df[elo_df[selected_location] == selected_team].set_index('date')['home_elo_pre'])

    st.header('Post-game Elo ratings')
    st.bar_chart(elo_df, x='home', y='home_elo_post')
    st.bar_chart(elo_df, x='away', y='away_elo_post')

    st.subheader('Make a prediction')
    away_teams = sorted(elo_df['away'].unique())
    home_teams = sorted(elo_df['home'].unique())

    away_team = st.selectbox('Away team', away_teams)
    home_team = st.selectbox('Home team', home_teams)
    away_elo_pre = st.number_input('Away Elo rating', min_value=0.0, value=1500.0)
    home_elo_pre = st.number_input('Home Elo rating', min_value=0.0, value=1450.0)
    elo_prob_away = st.number_input('Away win probability', min_value=0.0, max_value=1.0, value=0.40)
    elo_prob_home = st.number_input('Home win probability', min_value=0.0, max_value=1.0, value=0.60)

    if st.button('Predict winner', use_container_width=True):
        input_data = {
            'away_team': away_team,
            'home_team': home_team,
            'away_elo_pre': away_elo_pre,
            'home_elo_pre': home_elo_pre,
            'elo_prob_away': elo_prob_away,
            'elo_prob_home': elo_prob_home,
        }
        try:
            response = requests.post(api_url, json=input_data, timeout=30)
            if response.status_code == 200:
                st.session_state.pred = response.json()
            else:
                st.error(f'API error: {response.status_code} - {response.text}')
        except Exception as exc:
            st.error(f'Prediction request failed: {exc}')

    if st.session_state.pred is not None:
        prediction_val = st.session_state.pred.get('prediction')
        if prediction_val == 0:
            st.success('Home team is likely to lose.')
        else:
            st.success('Home team is likely to win.')