import streamlit as st
import anthropic

# Access the API key from Streamlit secrets
API_KEY = st.secrets["api_keys"]["anthropic_api_key"]

def get_meal_plan(fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preferences):
    # Initialize the Claude AI client with the API key from secrets
    client = anthropic.Anthropic(api_key=API_KEY)

    # Define the prompt to send to Claude AI
    prompt = (
        f"My fasting sugar level is {fasting_sugar} mg/dL, "
        f"my pre-meal sugar level is {pre_meal_sugar} mg/dL, "
        f"and my post-meal sugar level is {post_meal_sugar} mg/dL. "
        f"My dietary preferences are {dietary_preferences}. "
        "Please provide a personalized meal plan that can help me manage my blood sugar levels effectively."
    )

    # Call Claude AI API
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        temperature=0.7,
        system="You are a world-class nutritionist who specializes in diabetes management and your response should be to the point.",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    # Extract text from the response content
    if hasattr(response, 'content') and isinstance(response.content, list):
        meal_plan = '\n'.join([text_block.text for text_block in response.content]).strip()
    else:
        st.error("Unexpected response structure. Please check the response object.")
        meal_plan = "Error: Unable to parse response."

    return meal_plan

# Streamlit app
st.title("GlucoGuide By Umar Majeed [v1.0]")
st.write("""
GlucoGuide is a personalized meal planning app designed for individuals managing their blood sugar levels.
By entering your fasting sugar levels, pre-meal sugar levels, post-meal sugar levels, and dietary preferences,
you can receive a customized meal plan to help you manage your diabetes effectively.
""")

# Sidebar Inputs for sugar levels and dietary preferences
st.sidebar.header("Enter Your Details")

fasting_sugar = st.sidebar.number_input("Fasting Sugar Levels (mg/dL)", min_value=0, max_value=500, step=1)
pre_meal_sugar = st.sidebar.number_input("Pre-Meal Sugar Levels (mg/dL)", min_value=0, max_value=500, step=1)
post_meal_sugar = st.sidebar.number_input("Post-Meal Sugar Levels (mg/dL)", min_value=0, max_value=500, step=1)

# Dietary preferences dropdown
dietary_preferences = st.sidebar.selectbox(
    "Dietary Preferences",
    [
        "Vegetarian",
        "Vegan",
        "Low-Carb",
        "Low-Fat",
        "Gluten-Free",
        "Dairy-Free",
        "Paleo",
        "Ketogenic",
        "Mediterranean",
        "Whole30"
    ]
)

# Generate meal plan button
if st.sidebar.button("Generate Meal Plan"):
    meal_plan = get_meal_plan(fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preferences)
    st.write("Based on your sugar levels and dietary preferences, here is a personalized meal plan:")
    st.markdown(meal_plan)
