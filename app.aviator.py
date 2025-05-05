import streamlit as st
import pandas as pd

st.set_page_config(page_title="Aviator Prediction Expert", layout="centered")
st.title("Aviator Prediction Expert")

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df = df[df['multiplier'] > 1.0]
    df['decimal_part'] = (df['multiplier'] % 1) * 100
    df['mod_10'] = df['decimal_part'] % 10
    df['rolling_mean_5'] = df['multiplier'].rolling(5).mean()
    df['lag'] = df['multiplier'].shift(1)
    return df.dropna()

def predict_x5_plus(data, window, threshold):
    recent = data.tail(window)
    count_high = (recent['multiplier'] >= 5.0).sum()
    proba = count_high / window
    decision = proba >= threshold
    return proba, decision

data = load_data('data/processed_data.csv')

st.sidebar.header("Paramètres")
window = st.sidebar.slider('Fenêtre (rounds)', 5, 20, 10)
threshold = st.sidebar.slider('Seuil probabilité X5+', 0.5, 0.9, 0.7)

if st.sidebar.button('Prédire X5+'):
    proba, decision = predict_x5_plus(data, window, threshold)
    st.metric('Probabilité X5+ (%)', f"{proba * 100:.1f}")
    st.success("✅ Azo atao ny milalao X5+" if decision else "❌ Aza milalao amin'izao")

st.header("Historique farany (Top 10)")
st.dataframe(data.tail(10)[['multiplier', 'mod_10']])
