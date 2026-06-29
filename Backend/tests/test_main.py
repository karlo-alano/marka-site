from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_calculate():
    payload = {
        "categories": [
            {
                "category": "Attendance",
                "weight": 10,
                "assessments": [
                    {"name": "Attendance", "earned_points": 18, "total_points": 20}
                ],
            },
            {
                "category": "Quizzes",
                "weight": 15,
                "assessments": [
                    {"name": "Quiz 1", "earned_points": 8, "total_points": 10},
                    {"name": "Quiz 2", "earned_points": 18, "total_points": 20},
                    {"name": "Long Exam", "earned_points": 42, "total_points": 50},
                ],
            },
            {
                "category": "Midterm",
                "weight": 20,
                "assessments": [
                    {"name": "Midterm Exam", "earned_points": 70, "total_points": 95}
                ],
            },
        ]
    }

    response = client.post("/calculate", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["subject_grade"] == 36.49

    assert data["breakdown"][0]["category"] == "Attendance"
    assert data["breakdown"][1]["category"] == "Quizzes"
    assert data["breakdown"][2]["category"] == "Midterm"

    assert data["breakdown"][0]["contribution"] == 9.0
    assert data["breakdown"][1]["contribution"] == 12.75
    assert data["breakdown"][2]["contribution"] == 14.74


def test_empty_assessments():
    payload = {"categories": [{"category": "Quizzes", "weight": 15, "assessments": []}]}

    response = client.post("/calculate", json=payload)

    assert response.status_code == 200
    assert response.json()["subject_grade"] == 0
