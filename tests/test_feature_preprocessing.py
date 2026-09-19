"""
Ensures that preprocessing runs correctly
"""

from src.features import preprocess


def test_preprocess_generates_model_features_from_team_name_fields():
    payload = {
        "away_team": "Team B",
        "home_team": "Team A",
        "away_elo_pre": 1500.0,
        "home_elo_pre": 1400.0,
        "elo_prob_away": 0.45,
        "elo_prob_home": 0.55,
    }

    result = preprocess(payload)

    assert "away_encode" in result
    assert "home_encode" in result
    assert "away_elo_pre" in result
    assert "home_elo_pre" in result
    assert "elo_prob_away" in result
    assert "elo_prob_home" in result
    assert result["away_encode"] == 1
    assert result["home_encode"] == 0
