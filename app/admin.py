
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.database import SessionLocal
from app.models import FitnessPlan


admin_app = FastAPI(title="FitBuddy Admin")


@admin_app.get("/admin", response_class=HTMLResponse)
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
    <!DOCTYPE html>

    <html>

    <head>

        <title>FitBuddy Admin</title>

        <style>

            body {{
                font-family: Arial;
                background: #eef6ff;
                padding: 30px;
            }}

            .container {{
                max-width: 1100px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
            }}

            h1 {{
                color: #2563eb;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 25px;
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}

            th {{
                background: #2563eb;
                color: white;
            }}

            tr:nth-child(even) {{
                background: #f8fafc;
            }}

        </style>

    </head>

    <body>

        <div class="container">

            <h1>🔐 FitBuddy Admin Dashboard</h1>

            <p>
                Saved Fitness Plans
            </p>

            <table>

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

        </div>

    </body>

    </html>
    """
