from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_calculate_with_valid_data():
    payload = {
        "categories": [
            {
                "category": "Quizzes",
                "weight": 0.3,
                "assessments": [
                    {"name": "Quiz 1", "earned_points": 18, "total_points": 20}
                ],
            },
            {
                "category": "Exams",
                "weight": 0.7,
                "assessments": [
                    {"name": "Midterm", "earned_points": 85, "total_points": 100}
                ],
            },
        ]
    }

    response = client.post("/calculate", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["subject_grade"] == 86.5

    # Breakdown category verification
    assert data["breakdown"][0]["category"] == "Quizzes"
    assert data["breakdown"][1]["category"] == "Exams"

    # Percentage scores per category (grade * 100)
    assert data["breakdown"][0]["percentage"] == 90.0
    assert data["breakdown"][1]["percentage"] == 85.0

    # Individual rounded contributions to the total decimal score
    assert data["breakdown"][0]["contribution"] == 27.0
    assert data["breakdown"][1]["contribution"] == 59.5


def test_empty_assessments():
    payload = {
        "categories": [{"category": "Quizzes", "weight": 0.15, "assessments": []}]
    }

    response = client.post("/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["subject_grade"] == 0.0
    assert data["breakdown"][0]["percentage"] == 0.0
    assert data["breakdown"][0]["contribution"] == 0.0
