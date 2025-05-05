import streamlit as st
import pandas as pd

st.set_page_config(page_title="Aviator Prediction Expert", layout="centered")
st.title("Aviator Prediction Expert")

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df = df[df["multiplier"] > 1.0]
    df['decimal_part'] = (df['multiplier'] % 1) * 100
    df['mod_10'] = df['decimal_part'] % 10
    df['rolling_mean_5'] = df['multiplier'].rolling(window=5).mean()
    df['lag'] = df['multiplier'].shift(1)
    return df.dropna().reset_index(drop=True)

# Charger données
 data = load_data('data/processed_data.csv')

# Saisie ny multiplier anio
last_default = float(round(data['multiplier'].iloc[-1], 2))
today = st.sidebar.number_input('Ampidiro ny multiplier anio:', value=last_default, step=0.01)
if st.sidebar.button('Ampidiro anio'):
    new_row = {
        'multiplier': today,
        'decimal_part': (today % 1) * 100,
        'mod_10': int((today % 1) * 100) % 10,
        'rolling_mean_5': data['multiplier'].rolling(5).mean().iloc[-1],
        'lag': data['multiplier'].iloc[-1]
    }
    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
    st.success(f"Voasoratra ny multiplier {today:.2f}x ho an'ny anio")

# Paramètres
window = st.sidebar.slider('Fenêtre (rounds)', 5, 20, 10)
threshold = st.sidebar.slider('Seuil probabilité X5+', 0.5, 0.9, 0.7)

# Prédiction X5+
def predict_x5_plus(data, window, threshold):
    recent = data.tail(window)
    proba = (recent['multiplier'] >= 5.0).mean()
    decision = proba >= threshold
    return proba, decision

if st.sidebar.button('Prédire X5+'):
    proba, decision = predict_x5_plus(data, window, threshold)
    st.metric('Probabilité X5+ (%)', f"{proba * 100:.1f}")
    if decision:
        st.success("✅ Azo atao ny milalao X5+")
    else:
        st.error("❌ Aza milalao")

# Affichage farany
st.header("Historique farany (Top 10)")
st.dataframe(data.tail(10)[['multiplier', 'mod_10']])

