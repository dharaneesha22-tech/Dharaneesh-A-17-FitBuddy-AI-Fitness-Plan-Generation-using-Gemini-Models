
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

from app.gemini_generator import generate_workout
from app.nutrition_generator import generate_nutrition_tip
from app.database import SessionLocal, Base, engine
from app.models import FitnessPlan


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator",
    version="1.0.0"
)


@app.get("/", response_class=HTMLResponse)
def home():

    return """
<html>
<head>
    <title>FitBuddy</title>
</head>

<body>

<h1>💪 FitBuddy</h1>

<p>AI Fitness Plan Generator</p>

<form action="/generate" method="post">

    <label>Name</label><br>
    <input type="text" name="name" required><br><br>

    <label>Age</label><br>
    <input type="number" name="age" required><br><br>

    <label>Weight (kg)</label><br>
    <input type="number" name="weight" step="0.1" required><br><br>

    <label>Fitness Goal</label><br>

    <select name="goal">

        <option value="Weight Loss">
            Weight Loss
        </option>

        <option value="Muscle Gain">
            Muscle Gain
        </option>

        <option value="General Fitness">
            General Fitness
        </option>

    </select>

    <br><br>

    <label>Workout Intensity</label><br>

    <select name="intensity">

        <option value="Beginner">
            Beginner
        </option>

        <option value="Intermediate">
            Intermediate
        </option>

        <option value="Advanced">
            Advanced
        </option>

    </select>

    <br><br>

    <button type="submit">
        Generate AI Fitness Plan
    </button>

</form>

<br>

<a href="/admin">
    Admin Dashboard
</a>

</body>
</html>
"""


@app.post("/generate", response_class=HTMLResponse)
def generate_plan(
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    workout_plan = generate_workout(
        name,
        age,
        weight,
        goal,
        intensity
    )

    nutrition_tip = generate_nutrition_tip(
        goal,
        weight
    )

    db = SessionLocal()

    try:

        fitness_plan = FitnessPlan(
            name=name,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
            workout_plan=workout_plan,
            nutrition_tip=nutrition_tip
        )

        db.add(fitness_plan)
        db.commit()
        db.refresh(fitness_plan)

        plan_id = fitness_plan.id

    finally:

        db.close()


    return f"""
<html>
<head>
    <title>FitBuddy AI Plan</title>
</head>

<body>

<h1>🎯 Your FitBuddy AI Plan</h1>

<h3>Plan ID: {plan_id}</h3>

<p>
<b>Name:</b> {name}
</p>

<p>
<b>Age:</b> {age}
</p>

<p>
<b>Weight:</b> {weight} kg
</p>

<p>
<b>Goal:</b> {goal}
</p>

<p>
<b>Intensity:</b> {intensity}
</p>


<h2>🏋️ 7-Day Workout Plan</h2>

<div style="white-space: pre-wrap;">
{workout_plan}
</div>


<h2>🥗 Nutrition & Recovery Tip</h2>

<div style="white-space: pre-wrap;">
{nutrition_tip}
</div>


<br>

<a href="/">
    Create Another Plan
</a>

<br><br>

<a href="/admin">
    Admin Dashboard
</a>

</body>
</html>
"""


@app.get("/admin", response_class=HTMLResponse)
def admin_page():

    db = SessionLocal()

    try:

        plans = db.query(FitnessPlan).order_by(
            FitnessPlan.id.desc()
        ).all()

        rows = ""

        for plan in plans:

            rows += f"""
<tr>
    <td>{plan.id}</td>
    <td>{plan.name}</td>
    <td>{plan.age}</td>
    <td>{plan.weight}</td>
    <td>{plan.goal}</td>
    <td>{plan.intensity}</td>
</tr>
"""

    finally:

        db.close()


    return f"""
<html>
<head>
    <title>FitBuddy Admin</title>
</head>

<body>

<h1>🔐 FitBuddy Admin Dashboard</h1>

<table border="1" cellpadding="10">

<tr>
    <th>ID</th>
    <th>Name</th>
    <th>Age</th>
    <th>Weight</th>
    <th>Goal</th>
    <th>Intensity</th>
</tr>

{rows}

</table>

<br>

<a href="/">
    Back to FitBuddy
</a>

</body>
</html>
"""


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "application": "FitBuddy"
    }

