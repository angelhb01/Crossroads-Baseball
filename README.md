# Crossroads Baseball Analytics

A comprehensive baseball analytics platform that scrapes Crossroads League game data, applies Elo ranking systems, and uses machine learning to predict game outcomes.

## 📊 Project Overview

This project collects and analyzes thousands of college baseball games from the Crossroads League (2007-2025). It combines:
- **Web scraping** to gather game data
- **Elo rating system** to track team performance over time
- **Machine learning models** to predict game outcomes
- **Interactive dashboards** for visualization and exploration

## 🎯 Features

- **Game Data Scraping**: Automated collection of Crossroads League game results
- **Elo Ranking System**: Dynamic rating calculation based on game outcomes
- **Predictive Models**: ML models trained on historical game data (KFold cross-validation)
- **REST API**: FastAPI endpoint for real-time predictions
- **Interactive Dashboard**: Streamlit UI for data exploration and predictions
- **Rate Limiting**: Built-in rate limiting for API stability

## 🛠️ Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **Data Processing**: Pandas
- **Machine Learning**: Scikit-Learn
- **Web Scraping**: BeautifulSoup4, Requests
- **Rankings**: EloSports
- **Visualization**: Matplotlib
- **API Utilities**: SlowAPI (rate limiting)

## 📦 Project Structure

```
Crossroads-Baseball/
├── data/
│   ├── raw/                      # Raw scraped game data
│   └── clean/                    # Processed and cleaned data
├── models/
│   └── Kfold_CV/                # Cross-validated model artifacts
├── notebooks/
│   ├── 01_scrape_games.ipynb     # Data scraping pipeline
│   ├── 02_build_elo.ipynb        # Elo system implementation
│   └── 03_model_exploration.ipynb # ML model development
├── src/
│   ├── api.py                    # FastAPI prediction endpoint
│   ├── app.py                    # Streamlit dashboard
│   ├── scrape.py                 # Web scraping logic
│   ├── features.py               # Feature engineering & Elo calculations
│   └── predict.py                # Model predictions
├── Dockerfile                    # Container configuration
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/angelhb01/Crossroads-Baseball.git
   cd Crossroads-Baseball
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3.  **Activate environment with MacOS**
   ```bash
   venv/bin/activate
   ```

   **Activate environment with Windows**
   ```bash
   venv/Scripts/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Project

#### Interactive Dashboard (Streamlit)
```bash
cd src
streamlit run app.py
```
Then open your browser to `http://localhost:8501`

## 📝 Usage

### Making Predictions via API

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d "{
    \"home_team\": \"Team A\",
    \"away_team\": \"Team B\",
    \"features\": {...}
  }"
```

### Using the Streamlit Dashboard

1. Launch the app (see instructions above)
2. Click "Scrape" to fetch latest game data
3. View team rankings and performance metrics
4. Explore historical trends and predictions

## 📊 Data Sources

- Crossroads League college baseball games (2007-2025)
- Automated web scraping from league official sources

## 🔧 Development

### Workflow

1. **Data Collection** (`01_scrape_games.ipynb`): Scrapes game data and stores in `data/raw/`
2. **Processing** (`02_build_elo.ipynb`): Cleans data and calculates Elo ratings
3. **Modeling** (`03_model_exploration.ipynb`): Develops ML models with KFold validation
4. **Prediction**: Serves predictions via API or dashboard

### Model Details

- **Algorithm**: Trained on historical game outcomes
- **Validation**: K-Fold cross-validation
- **Features**: Team Elo ratings, head-to-head history, seasonal trends
- **Output**: Home team win probability

## 🐳 Docker

To run with Docker:
```bash
docker build -t crossroads-baseball .
docker run -p 8000:8000 -p 8501:8501 crossroads-baseball
```

## 📈 Metrics & Performance

The Elo rating system tracks team performance across all seasons. Ratings are updated after each game based on:
- Expected win probability
- Actual game outcome
- Rating differential between teams
