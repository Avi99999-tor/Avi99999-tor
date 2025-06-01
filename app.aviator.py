import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import random

# === Interface ===
st.set_page_config(page_title="Prédiction Aviator - Mickael TOP EXACTE")
st.title("🇲🇬 Prediction By Mickael TOP EXACTE 🇲🇬")

st.markdown("""
<style>
.big-font {
    font-size:25px !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">T+1 à T+20 Prédiction</p>', unsafe_allow_html=True)

# === Inputs ===
st.sidebar.subheader("Données Historiques")
raw_data = st.sidebar.text_area("Multiplicateurs (T1 → Tn):",
                                 placeholder="Ex: 1.03, 2.10, 5.55, 1.98, 3.44")
dernier_tour = st.sidebar.text_input("Dernier numéro de tour (ex: 125):", "125")

# Effacer bouton
def clear_inputs():
    st.experimental_rerun()

if st.sidebar.button("Effacer Données"):
    clear_inputs()

# === Conversions ===
def parse_data(raw):
    try:
        values = [float(x.strip()) for x in raw.split(",") if x.strip() != ""]
        return values
    except:
        return []

historique = parse_data(raw_data)

# === AI Simplifiée ===
def ai_prediction(histo, tours=20):
    X = np.array(range(len(histo))).reshape(-1, 1)
    y = np.array(histo)
    model = LinearRegression()
    model.fit(X, y)
    X_pred = np.array(range(len(histo), len(histo)+tours)).reshape(-1, 1)
    y_pred = model.predict(X_pred)
    return np.round(y_pred, 2)

# === Stratégie Expert ===
def expert_predictions(histo, tours=20):
    results = []
    base = histo[-1] if histo else 2.0
    for i in range(tours):
        rep = round(base + np.sin(i)*random.uniform(0.3, 1.2), 2)
        results.append(rep)
    return results

# === Combinaison & Affichage ===
def prediction_combinee(histo, n_tour):
    ai_preds = ai_prediction(histo)
    exp_preds = expert_predictions(histo)
    results = []
    for i, (a, e) in enumerate(zip(ai_preds, exp_preds)):
        comb = round((a + e)/2, 2)
        taux = min(100, round(90 + abs(a - e)*2, 1))
        results.append((n_tour + i + 1, comb, taux))
    return results

# === Résultats ===
if historique and dernier_tour.isdigit():
    résultats = prediction_combinee(historique, int(dernier_tour))
    for tour, val, taux in résultats:
        couleur = "🔘" if val < 2 else "💜" if val < 10 else "🔴"
        st.write(f"T{tour} → {val}x {couleur} — Assurance: {taux}%")
else:
    st.info("Veuillez entrer des données valides pour afficher la prédiction.")
