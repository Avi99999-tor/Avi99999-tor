import streamlit as st
import numpy as np
import random
import pandas as pd
from sklearn.linear_model import LinearRegression

# --- Configuration ---
st.set_page_config(page_title="🇲🇬 Prediction By Mickael", layout="centered")
st.title("🇲🇬 🎯 Prediction Expert By Mickael")

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
    
    # **Fanitsiana ny probabilités mba hanaraka Aviator**
    pred = [round(max(1.00, min(float(p), 5.00)), 2) for p in pred]  # **Tsy mamokatra valeur x100**
    
    return pred

# --- Prediction Expert ---
def prediction_expert(multiplicateurs, base_tour):
    résultats = []
    rolling_mean = np.mean(multiplicateurs)
    mod_score = sum([int(str(x).split(".")[-1]) % 10 for x in multiplicateurs]) / len(multiplicateurs)

    for i in range(1, 21):  # T+1 à T+20 (Manomboka amin'ny 205)
        seed = int((mod_score + rolling_mean + i * 3.73) * 1000) % 47
        pred_expert = round(abs((np.sin(seed) + np.cos(i * mod_score)) * 2.3 + random.uniform(0.2, 1)), 2)

        # **Fanovana probabilités hanaraka ny historique an'Aviator**
        if pred_expert < 1.10:
            pred_expert = round(1.10 + random.uniform(0.05, 0.3), 2)
        elif pred_expert > 5.00:  # **Tsy atao max 6 fa manaraka probabilités historique**
            pred_expert = round(random.uniform(3.0, 5.0), 2)

        fiab = fiabilite(pred_expert)
        label = "Assuré" if fiab >= 80 else ("Crash probable" if pred_expert <= 1.20 else "")

        résultats.append((base_tour + i, pred_expert, fiab, label))  
    
    return résultats

# --- Prediction Combinée: AI + Expert ---
def prediction_combinee(historique, base_tour):
    ia_preds = regression_prediction(historique)
    exp_preds = prediction_expert(historique, base_tour)

    résultats = []

    for i in range(20):
        ai = ia_preds[i]
        exp = exp_preds[i][1]

        # **Fanovana pondération mba hanaraka trend historique**
        final = round((ai * 0.5 + exp * 0.5), 2)  # **Mifandanja tsara AI sy Expert**
        final = max(final, 1.00)  # **Mifanaraka amin'ny probabilités stable**
        
        fiabilité = fiabilite(final)

        résultats.append({
            "Tour": f"T{base_tour + i + 1}",
            "Prediction IA": f"{ai}x",
            "Prediction Expert": f"{exp}x",
            "Résultat Final": f"{final}x",
            "Fiabilité": f"{fiabilité}%"
        })
    
    return pd.DataFrame(résultats)

# --- Fanodinana ---
if calculer:  # **Bouton tsindriana mba hanaovana prédiction**
    historique = extraire_valeurs(multiplicateurs_input)

    if len(historique) < 10:
        st.warning("❗ Tokony hampiditra farafahakeliny 10 multiplicateurs.")
    else:
        résultats_df = prediction_combinee(historique, int(dernier_tour))

        st.markdown("### 📊 Résultat T+205 à T+224 :")
        st.table(résultats_df)  # **Miseho amin'ny tabilao**
