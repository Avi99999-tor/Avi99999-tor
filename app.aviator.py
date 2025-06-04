import streamlit as st
import numpy as np
import random
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

# --- Configuration ---
st.set_page_config(page_title="🇲🇬 Prediction By Mickael", layout="centered")
st.title("🇲🇬 🎯 Prediction Expert By Mickael")

st.subheader("Fanatsarana probabilités AI sy Expert amin’ny lera ⏳")

# --- Fidirana data (multiplicateurs) ---
multiplicateurs_input = st.text_area("💾 Ampidiro ny multiplicateurs (misaraka amin'ny espace)", 
                                     placeholder="1.99x 2.30x 1.42x 1.12x ...", height=150)

dernier_tour = st.number_input("🔢 Numéro du dernier tour", min_value=1, value=34)
dernier_heure = st.text_input("🕒 Entrer l'heure du dernier tour (HH:MM:SS)", value="12:23:56")

# --- Bouton Calculer ---
calculer = st.button("🔄 Calculer les prédictions")

# --- Calcul durée multiplicateur (manaraka strategia vaovao) ---
def calcul_duree(multiplicateur):
    if 1.00 <= multiplicateur < 2.00:
        duree = (multiplicateur * 13) / 1.33
    elif 2.00 <= multiplicateur < 3.00:
        duree = (multiplicateur * 20) / 2.29
    elif 3.00 <= multiplicateur < 4.00:
        duree = (multiplicateur * 23) / 3.12
    elif 4.00 <= multiplicateur < 5.00:
        duree = (multiplicateur * 27) / 4.27
    elif 5.00 <= multiplicateur < 9.00:
        duree = (multiplicateur * 28) / 5.01
    elif 9.00 <= multiplicateur <= 20.00:
        duree = (multiplicateur * 39) / 11.87
    else:
        duree = 10  # Valeur par défaut

    # **Boriborizina automatique**
    return round(duree) if duree % 1 < 0.80 else round(duree + 1)

# --- Algorithme AI: Régression avancée ---
def regression_prediction(multiplicateurs):
    X = np.arange(len(multiplicateurs)).reshape(-1, 1)
    y = np.array(multiplicateurs).reshape(-1, 1)
    model = LinearRegression().fit(X, y)
    pred = model.predict(np.arange(len(multiplicateurs), len(multiplicateurs) + 20).reshape(-1, 1))
    return [round(max(1.00, float(p)), 2) for p in pred]

# --- Prediction Expert ---
def prediction_expert(multiplicateurs):
    résultats = []
    rolling_mean = np.mean(multiplicateurs)
    for i in range(1, 21):
        seed = int((rolling_mean + i * 3.73) * 1000) % 47
        résultats.append(round(abs(np.sin(seed) * 3.2 + random.uniform(0.3, 1.2)), 2))
    return résultats

# --- Prediction Combinée (Avec heure automatique) ---
def prediction_combinee(historique, base_tour, base_heure):
    ia_preds = regression_prediction(historique)
    exp_preds = prediction_expert(historique)
    résultats = []

    heure_actuelle = datetime.strptime(base_heure, "%H:%M:%S")

    for i in range(20):
        ai, exp = ia_preds[i], exp_preds[i]
        final = round((ai * 0.5 + exp * 0.5), 2)

        # **Calcul automatique heure prediction**
        duree = calcul_duree(final)
        heure_actuelle += timedelta(seconds=duree)
        heure_prediction = heure_actuelle.strftime("%H:%M:%S")

        résultats.append({
            "Tour": f"T{base_tour + i + 1}",
            "Prediction IA": f"{ai}x",
            "Prediction Expert": f"{exp}x",
            "Résultat Final": f"{final}x",
            "Heure": heure_prediction  # **Horaire automatique**
        })
    
    return pd.DataFrame(résultats)

# --- Fanodinana ---
if calculer:
    historique = [float(x) for x in multiplicateurs_input.replace(",", ".").replace("x", "").split()]
    résultats_df = prediction_combinee(historique, int(dernier_tour), dernier_heure)
    st.markdown("### 📊 Résultat T+35 à T+45 :")
    st.table(résultats_df)
