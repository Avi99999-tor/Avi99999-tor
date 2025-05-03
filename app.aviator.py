import streamlit as st
import random
from datetime import datetime

# Function to generate predictions based on RNG and historical data
def generate_prediction(historical_data, seed_value):
    random.seed(seed_value)
    
    # Extract the last few digits from the historical data (last 3-4 tours)
    last_data = [round(data % 10) for data in historical_data[-4:]]  # Example: take last 4 multipliers

    # Generate RNG sequence for predictions
    rng_digits = [random.randint(0, 9) for _ in range(10)]
    
    # Summing the RNG and historical data with Mod 10 for prediction
    combined_data = [(x + y) % 10 for x, y in zip(last_data, rng_digits)]
    
    # Result prediction: Use mod 10 logic or statistical model here
    prediction = "X" + str(sum(combined_data) % 10)  # Simplified logic for demonstration

    return prediction, rng_digits

# Function to analyze historical trends and output the next possible prediction
def analyze_trends(historical_data):
    last_multiplier = historical_data[-1]
    
    if last_multiplier > 5:
        prediction = "X10"
    else:
        prediction = "X5"
    
    return prediction

# Streamlit app structure
st.title("Aviator Game Prediction")

# User inputs
historical_input = st.text_area("Enter Historical Data", "1.39 2.00 1.52 1.52 3.49 10.00 5.00")  # Example input
historical_data = [float(x) for x in historical_input.split()]
seed_input = st.text_input("Enter RNG Seed", "20250502")

# Process inputs
seed_value = int(seed_input)
prediction, rng_digits = generate_prediction(historical_data, seed_value)
trend_prediction = analyze_trends(historical_data)

# Displaying predictions
st.write(f"Predicted Outcome: {prediction}")
st.write(f"RNG Digits Used: {rng_digits}")
st.write(f"Trend Based Prediction: {trend_prediction}")

# Display historical data and analysis
st.write("Historical Data (Last 4 Tours):", historical_data[-4:])
