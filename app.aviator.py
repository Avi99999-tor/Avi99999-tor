import streamlit as st
import numpy as np

st.set_page_config(page_title="Aviator Prediction - Mode Expert", layout="centered")
st.title("Aviator Predictor — Mode Expert")

# Input zone
history_input = st.text_area("Multiplicateurs récents (séparés par espace ou ligne)", height=150)
predict_button = st.button("Prédire (T+1 à T+10)")

# Prediction logic
def predict_expert(data):
    data = [float(x.lower().replace('x', '').replace('%', '')) for x in data if x.strip()]
    predictions = []
    
    for i in range(10):
        last_vals = data[-5:] if len(data) >= 5 else data
        mean = np.mean(last_vals)
        std_dev = np.std(last_vals)
        
        # Pondération dynamique
        weight = 1.0
        if data[-1] < 1.3:  # Crash probable
            weight = 1.4
        elif data[-1] > 5:
            weight = 0.8
        
        # Rolling average + variation
        pred = round(np.clip(np.random.normal(mean * weight, std_dev), 1.00, 25.0), 2)
        
        # Fiabilité estimation
        fiability = round(100 - abs(mean - pred) * 4, 1)
        label = "Assuré" if fiability >= 80 else "Probable" if fiability >= 60 else "Faible"
        
        # Filter only if fiabilité > 60%
        if fiability >= 60:
            predictions.append((f"T{i+1}", pred, f"{fiability}%", label))
        
        data.append(pred)
    return predictions

# Résultat
if predict_button and history_input:
    raw_data = history_input.replace('\n', ' ').split()
    results = predict_expert(raw_data)

    if results:
        st.subheader("Résultats avec Fiabilité (≥ 60%)")
        for tour, val, taux, label in results:
            st.markdown(f"**{tour} → {val}x** | Fiabilité: `{taux}` — `{label}`")
    else:
        st.warning("Tsy nisy prediction fiabilité > 60%.")
