import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
from time import sleep
from streamlit import cache_data

# URL to be scraped
initial_url = "https://crossroadsleague.com/sports/bsb/2006-07/schedule?jsRendering=true"

headers = {
    "User-Agent": "Chrome/120.0.0.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://crossroadsleague.com/"
}

@cache_data(ttl=3600) # Store data in a cache for 1 hour
def scrape_data():
    page = requests.get(initial_url, headers=headers).text
    soup = BeautifulSoup(page, 'html.parser')
    sleep(5)

    column_headers = ['date', 'away', 'home', 'away_score', 'home_score']
    df = pd.DataFrame(columns=column_headers)

    urls = [option.get('value') for option in soup.find('select', id='season-selector').find_all('option')]

    for url in urls:
        page = requests.get("https://crossroadsleague.com" + url, headers=headers).text
    
        soup = BeautifulSoup(page, 'html.parser')
        sleep(5)
        print("Season Result: ", soup.find('div', class_='page-content-header').text.strip().split(' ')[0])
        season = soup.find('div', class_='page-content-header').text.strip().split(' ')[0]
    
        start_year = None
        end_year = None
    
        if '-' in season:
            start_year = int(re.split(r'-', season)[0])
        else:
            end_year = int(season)

        # Finding the score results
        results = soup.find_all('div', class_='result')
    
        for result in results:

            # Date
            day = result.find_parent('div', class_='section-event-date').get('data-date')
            month = result.find_parent('div', class_='section-event-month').get('class')[1]

            month_num = datetime.strptime(month, "%B").month

            if month_num >= 8 and start_year:
                year = start_year
            elif month_num >= 8 and end_year:
                year = end_year - 1
            
            if month_num < 8 and start_year:
                year = start_year + 1
            elif month_num < 8 and end_year:
                year = end_year

            date_str = f"{month} {day} {year}"
            date = datetime.strptime(date_str, "%B %a. %d %Y")
        
            # Team Name
            team_name = result.find_all('span', class_='team-name')[0].text.strip()
        
            # Opponent Name
            opponent_name = result.find_all('span', class_='team-name')[1].text.strip()

            # Scores
            team_score = result.find_all('div', class_='flex-shrink-1')[0].text.strip()
            opponent_score = result.find_all('div', class_='flex-shrink-1')[1].text.strip()
        
            df.loc[len(df)] = [date, team_name, opponent_name, team_score, opponent_score]

    # Clean scraped data
    # change datatype of scores from object to numbers
    df = df.astype({
        'away_score': int,
        'home_score': int
    })
    # standardize text data
    df['away'] = df['away'].str.lower()
    df['home'] = df['home'].str.lower()
    same_team = {
        'grace' : 'grace (in)',
        'goshen' : 'goshen (in)',
        'huntington' : 'huntington (in)',
        'indiana wesleyan' : 'indiana wesleyan (in)',
        'marian' : 'marian (in)',
        'mount vernon nazarene' : 'mount vernon nazarene (oh)',
        'saint francis (ind.)' : 'saint francis (in)',
        'spring arbor' : 'spring arbor (in)',
        'taylor' : 'taylor (in)',
        'aquinas' : 'aquinas (mi)',
        'faulkner' : 'faulkner (al)',
        'bryan' : 'bryan (tn)',
        'union' : 'union (ky)'
    }
    df['away'] = df['away'].replace(same_team)
    df['home'] = df['home'].replace(same_team)

    return df.sort_values(by="date", ascending=True)