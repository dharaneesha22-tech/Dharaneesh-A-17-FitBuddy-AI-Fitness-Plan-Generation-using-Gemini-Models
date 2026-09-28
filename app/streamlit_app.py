import streamlit as st

from gemini_generator import generate_workout
from nutrition_generator import generate_nutrition_tip


st.set_page_config(
    page_title="FitBuddy",
    page_icon="💪",
    layout="centered"
)

st.title("💪 FitBuddy")
st.subheader("AI Fitness Plan Generator using Gemini")


name = st.text_input("Name")

age = st.number_input(
    "Age",
    min_value=10,
    max_value=100,
    value=20
)

weight = st.number_input(
    "Weight (kg)",
    min_value=20.0,
    max_value=300.0,
    value=60.0
)

goal = st.selectbox(
    "Fitness Goal",
    [
        "Weight Loss",
        "Muscle Gain",
        "General Fitness"
    ]
)

intensity = st.selectbox(
    "Workout Intensity",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)


if st.button("Generate AI Fitness Plan"):

    if not name:
        st.warning("Please enter your name.")

    else:

        with st.spinner("Generating your AI fitness plan..."):

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

        st.success("Your fitness plan is ready!")

        st.header("🏋️ 7-Day Workout Plan")
        st.write(workout_plan)

        st.header("🥗 Nutrition & Recovery")
        st.write(nutrition_tip)