from app import app, calculate_daily_calories, get_client_summary


def test_calculate_daily_calories_fat_loss():
    assert calculate_daily_calories(70, "Fat Loss") == 1540


def test_calculate_daily_calories_muscle_gain():
    assert calculate_daily_calories(75, "Muscle Gain") == 2625


def test_calculate_daily_calories_invalid_program():
    try:
        calculate_daily_calories(60, "Unknown")
        assert False, "Expected ValueError for unsupported program"
    except ValueError:
        pass


def test_get_client_summary():
    summary = get_client_summary("Aisha", 29, 68, "Beginner")
    assert summary["name"] == "Aisha"
    assert summary["program"] == "Beginner"
    assert summary["calories_per_day"] == 1768


def test_home_endpoint():
    client = app.test_client()
    response = client.get("/", headers={"Accept": "text/html"})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["app"] == "BITS Pilani Student Fitness & Wellness API"
    assert "Fat Loss" in payload["programs"]
