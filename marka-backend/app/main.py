from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Assessment(BaseModel):
    name: str
    earned_points: float
    total_points: float


class GradeCategory(BaseModel):
    category: str
    weight: float
    assessments: list[Assessment]


class Subject(BaseModel):
    categories: list[GradeCategory]


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/calculate")
def calculate(subject: Subject):
    weighted_average = 0.0
    breakdown = []

    for category in subject.categories:
        grade = get_activity_grade(category.assessments)

        contribution = grade * category.weight
        weighted_average += contribution

        breakdown.append(
            {
                "category": category.category,
                "percentage": round(grade * 100, 2),
                "weight": category.weight,
                "contribution": round(contribution, 2),
            }
        )

    return {"subject_grade": round(weighted_average, 2), "breakdown": breakdown}


def get_activity_grade(assessments: list[Assessment]) -> float:
    earned_total = sum(a.earned_points for a in assessments)
    overall_total = sum(a.total_points for a in assessments)

    if overall_total == 0:
        return 0

    return earned_total / overall_total
