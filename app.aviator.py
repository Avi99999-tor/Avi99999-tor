import streamlit as st
import numpy as np
import random
from sklearn.linear_model import LinearRegression

# --- Configuration ---
st.set_page_config(page_title="🇲🇬 Prediction By Mickael", layout="centered")
st.title("🇲🇬 🎯 Prediction Expert By Mickael")

st.subheader("Fanatsarana probabilités AI")

# --- Fidirana data (multiplicateurs) ---
multiplicateurs_input = st.text_area("💾 Ampidiro ny multiplicateurs (misaraka amin'ny espace)", 
                                     placeholder="1.19x 8.28x 26.84x 1.57x 1.45x ...", height=150)

dernier_tour = st.number_input("🔢 Numéro du dernier tour", min_value=1, value=204)

# --- Bouton Calculer ---
calculer = st.button("🔄 Calculer les prédictions")

# --- Fanadiovana angona ---
def extraire_valeurs(texte):
    valeurs = texte.replace(',', '.').lower().replace('x', '').split()
    valeurs_propres = []
    
    for v in valeurs:
        try:
            val = float(v)
            if val > 0:
                valeurs_propres.append(val)
        except ValueError:
            continue  

    return valeurs_propres

# --- Fiabilité calculation ---
def fiabilite(val):
    if val >= 5:
        return round(random.uniform(85, 95), 2)
    elif val >= 3:
        return round(random.uniform(75, 85), 2)
    elif val <= 1.20:
        return round(random.uniform(60, 70), 2)
    else:
        return round(random.uniform(70, 80), 2)

# --- Algorithme AI: Régression avancée ---
def regression_prediction(multiplicateurs):
    X = np.arange(len(multiplicateurs)).reshape(-1, 1)
    y = np.array(multiplicateurs).reshape(-1, 1)
    
    model = LinearRegression().fit(X, y)
    pred = model.predict(np.arange(len(multiplicateurs), len(multiplicateurs) + 20).reshape(-1, 1))
    
    return [round(float(p), 2) for p in pred]

# --- Prediction Expert ---
def prediction_expert(multiplicateurs, base_tour):
    résultats = []
    rolling_mean = np.mean(multiplicateurs)
    mod_score = sum([int(str(x).split(".")[-1]) % 10 for x in multiplicateurs]) / len(multiplicateurs)

    for i in range(1, 21):  # T+1 à
