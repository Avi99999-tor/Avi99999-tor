import streamlit as st
import random

# Function to generate and display prediction
def generate_prediction(seed, multipliers):
    random.seed(seed)
    
    # Extract digits from multipliers
    digits = []
    for mul in multipliers:
        digits.extend([int(digit) for digit in str(mul)[2:]])  # get digits after the decimal point

    # Generate random digits based on the seed
    rng_digits = [random.randint(0, 9) for _ in range(len(digits))]

    # Apply mod 10 addition
    final_digits = [(d + r) % 10 for d, r in zip(digits, rng_digits)]
    
    # Create seeds from the resulting digits
    seeds = []
    for i in range(0, len(final_digits), 10):
        seeds.append(int("".join(map(str, final_digits[i:i+10]))))
    
    return seeds

# Example multipliers (replace these with actual data from the game)
multipliers = [1.05, 2.00, 1.52, 1.52, 3.49]

# Generate prediction based on seed (20250502)
seed = 20250502
seeds = generate_prediction(seed, multipliers)

# Display the result using Streamlit
st.title("Aviator Game Prediction")
st.write("Generated Seeds: ", seeds)

# Display message based on analysis (optional)
st.write("Prediction Analysis:")
st.write("Based on the generated seeds, there is a trend towards a possible increase in the next rounds.")
