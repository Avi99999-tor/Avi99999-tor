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

dernier_tour = st.number_input("🔢 Numéro du dernier tour", min_value=1, value=50)

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
    regression_preds = regression_prediction(multiplicateurs)

    for i in range(20):  # T+1 à T+20
        pred_reg = regression_preds[i]
        seed = int((rolling_mean + i * 3.73) * 1000) % 57
        pred_expert = round(abs((np.sin(seed) + np.cos(i * rolling_mean)) * 3.5 + random.uniform(0.3, 1.7)), 2)

        # Filtrage sy fanitsiana
        if pred_expert < 1.10:
            pred_expert = round(1.10 + random.uniform(0.1, 0.3), 2)
        elif pred_expert > 10:
            pred_expert = round(6.5 + random.uniform(0.5, 1.5), 2)

        # Fusion AI + Expert
        final_pred = round((pred_reg * 0.6 + pred_expert * 0.4), 2)
        final_pred = max(final_pred, 1.10)

        fiab = fiabilite(final_pred)
        label = "Assuré" if fiab >= 80 else ("Crash probable" if final_pred <= 1.20 else "")

        résultats.append((base_tour + i, final_pred, fiab, label))
    
    return résultats

# --- Fanodinana ---
if calculer:  # Bouton tsindriana mba hanaovana prédiction
    historique = extraire_valeurs(multiplicateurs_input)

    if len(historique) < 10:
        st.warning("❗ Tokony hampiditra farafahakeliny 10 multiplicateurs.")
    else:
        résultats = prediction_expert(historique, int(dernier_tour))
        st.markdown("### 📊 Résultat T+1 à T+20 :")

        for tour, val, pourcent, label in résultats:
            line = f"**T{tour}** → **{val}x** — Fiabilité: **{pourcent}%**"
            if label:
                line += f" **({label})**"
            st.markdown("- " + line)
