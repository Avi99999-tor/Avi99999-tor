import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Aviator Prediction Expert", layout="centered")
st.title("Aviator Prediction Expert")

@st.cache_data
def generate_dummy_data():
    np.random.seed(42)
    multipliers = np.round(np.random.uniform(1.0, 50.0, 180), 2)
    df = pd.DataFrame({'multiplier': multipliers})
    df['decimal_part'] = (df['multiplier'] % 1) * 100
    df['mod_10'] = df['decimal_part'] % 10
    return df

data = generate_dummy_data()

window = st.sidebar.slider('Fenêtre (rounds)', 5, 20, 10)
threshold = st.sidebar.slider('Seuil prob X5+', 0.5, 0.9, 0.7)

if st.sidebar.button('Prédire X5+'):
    proba = (data['multiplier'].tail(window) > 5).mean()
    decision = proba >= threshold
    st.metric('Proba X5+ (%)', f"{proba * 100:.1f}")
    st.success("✅ Mety hilatsaka X5+" if decision else "❌ Tsy azo atokisana")

st.header("Données récentes")
st.dataframe(data.tail(20)[['multiplier', 'decimal_part', 'mod_10']])
