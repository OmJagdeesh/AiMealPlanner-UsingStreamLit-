import streamlit as st
import openai

# Set OpenAI API Key (Replace with your key)
openai.api_key = st.secrets["pass"]
# Title
st.title("AI-Powered Personalized Indian Meal Plan Generator")
st.write("Get a personalized Indian meal plan based on your health profile and dietary preferences.")

# Sidebar for User Input
st.sidebar.header("Personal Information")
age = st.sidebar.number_input("Age (years)", min_value=10, max_value=100, value=25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250, value=170)
weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
activity_level = st.sidebar.selectbox("Activity Level", [
    "Sedentary (little to no exercise)",
    "Lightly active (light exercise/sports 1-3 days/week)",
    "Moderately active (moderate exercise/sports 3-5 days/week)",
    "Very active (hard exercise/sports 6-7 days/week)"
])

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
    Each meal should include traditional Indian dishes with simple recipes. Break the calorie distribution across meals evenly.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error("Error generating meal plan. Please check your OpenAI API Key or try again.")
        return None

# Generate Button
if st.sidebar.button("Generate Meal Plan"):
    st.subheader("Your Personalized Indian Meal Plan")
    with st.spinner("Generating..."):
        meal_plan = generate_indian_meal_plan(calories, diet, allergies, meals_per_day)
        if meal_plan:
            st.text(meal_plan)
        else:
            st.error("Unable to generate a meal plan. Please try again later.")

# Footer
st.write("Powered by AI. Built with Streamlit.")
