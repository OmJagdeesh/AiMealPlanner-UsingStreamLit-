import streamlit as st
import openai
import pandas as pd
import random
from fpdf import FPDF
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Title
st.title("AI-Powered Personalized Indian Meal Plan Generator")
st.write(
    "Get a personalized Indian meal plan based on your health profile and dietary preferences."
)

# Sidebar for User Input
st.sidebar.header("Personal Information")
age = st.sidebar.number_input("Age (years)", min_value=10, max_value=100, value=25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250, value=170)
weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
activity_level = st.sidebar.selectbox(
    "Activity Level",
    [
        "Sedentary (little to no exercise)",
        "Lightly active (light exercise/sports 1-3 days/week)",
        "Moderately active (moderate exercise/sports 3-5 days/week)",
        "Very active (hard exercise/sports 6-7 days/week)",
    ],
)

st.sidebar.header("Dietary Preferences")
diet = st.sidebar.selectbox("Diet Preference", ["None", "Vegetarian", "Vegan"])
allergies = st.sidebar.text_input("Allergies (comma-separated)")
meals_per_day = st.sidebar.slider("Number of Meals Per Day", 3, 6, 4)


# Calculate Caloric Requirement
def calculate_calories(age, gender, height, weight, activity_level):
    # Mifflin-St Jeor Equation
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Adjust for activity level
    activity_multiplier = {
        "Sedentary (little to no exercise)": 1.2,
        "Lightly active (light exercise/sports 1-3 days/week)": 1.375,
        "Moderately active (moderate exercise/sports 3-5 days/week)": 1.55,
        "Very active (hard exercise/sports 6-7 days/week)": 1.725,
    }
    return int(bmr * activity_multiplier[activity_level])


calories = calculate_calories(age, gender, height, weight, activity_level)
st.sidebar.write(f"Estimated Caloric Requirement: {calories} kcal")


# Generate Meal Plan
def generate_indian_meal_plan(calories, diet, allergies, meals_per_day):
    prompt = f"""
    Create a personalized Indian meal plan for one day with approximately {calories} calories. 
    The plan should include {meals_per_day} meals, suitable for a {diet.lower()} diet. Avoid the following allergens or ingredients: {allergies}.
    Each meal should include traditional Indian dishes with simple recipes. Break the calorie distribution evenly across meals.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000,
        )
        return response.choices[0].message["content"]
    except Exception as e:
        st.error(
            "Error generating meal plan. Please check your OpenAI API Key or try again."
        )
        return None


# Generate PDF of Meal Plan
def save_to_pdf(meal_plan):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, meal_plan)
    pdf_output = "meal_plan.pdf"
    pdf.output(pdf_output)
    return pdf_output


# Generate Button
if st.sidebar.button("Generate Meal Plan"):
    st.subheader("Your Personalized Indian Meal Plan")
    with st.spinner("Generating..."):
        meal_plan = generate_indian_meal_plan(calories, diet, allergies, meals_per_day)
        if meal_plan:
            # Display Meal Plan
            st.text(meal_plan)

            # Add Save as PDF Option
            if st.button("Download Meal Plan as PDF"):
                pdf_file = save_to_pdf(meal_plan)
                st.success("Meal Plan saved! Click below to download.")
                with open(pdf_file, "rb") as file:
                    st.download_button(
                        label="Download PDF",
                        data=file,
                        file_name="meal_plan.pdf",
                        mime="application/pdf",
                    )
        else:
            st.error("Unable to generate a meal plan. Please try again later.")

# Example Indian Food Images (for demo purposes, static placeholders)
st.subheader("Sample Indian Dishes")
sample_dishes = {
    "Breakfast": "Masala Dosa",
    "Lunch": "Paneer Butter Masala with Roti",
    "Dinner": "Vegetable Pulao with Raita",
    "Snacks": "Chana Chaat",
}

for meal, dish in sample_dishes.items():
    st.write(f"**{meal}**: {dish}")
    st.image(
        f"https://via.placeholder.com/300x200.png?text={dish.replace(' ', '+')}",
        caption=dish,
    )

# Footer
st.write("Powered by AI. Built with Streamlit.")
