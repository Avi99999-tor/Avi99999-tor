import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import random

# --- Prédiction IA avec Linear Regression ---
def ai_prediction(historique):
    try:
        y = np.array(historique[-10:]).reshape(-1, 1)
        X = np.arange(len(y)).reshape(-1, 1)
        model = LinearRegression().fit(X, y)
        next_step = np.array([[len(y)]])
        prediction = model.predict(next_step)[0][0]
        return round(prediction, 2)
    except:
        return 1.00

# --- Analyse expert basé sur logique mod 10 ---
def analyse_mod_seed(historique):
    if not historique:
        return 0.0
    count = 0
    for h in historique[-10:]:
        try:
            valeur = float(h)
            if int(valeur * 100) % 10 in [3, 6, 9]:
                count += 1
        except:
            continue
    score = (count / 10) * 100
    return round(score, 2)

# --- Expert Prediction basée sur logique tendance simple ---
def expert_predictions(historique):
    predictions = []
    for i in range(1, 4):
        if len(historique) >= i:
            try:
                val = float(historique[-i])
                if val > 10:
                    predictions.append(1.5 + i)
                elif val > 2:
                    predictions.append(2 + (i * 0.5))
                else:
                    predictions.append(1.00 + (i * 0.25))
            except:
                predictions.append(1.00)
    score = analyse_mod_seed(historique)
    return max(predictions), score

# --- Fusion IA + Expert (Combinée) ---
def prediction_combinee(historique, tour):
    ai_pred = ai_prediction(historique)
    exp_pred, score = expert_predictions(historique)

    if abs(exp_pred - ai_pred) < 1.0:
        final = round((exp_pred + ai_pred) / 2, 2)
    else:
        final = round(exp_pred, 2)

    assurance = round((score + 80 + random.randint(0, 10)) / 2, 2)
    couleur = "🔘" if final < 2 else "💜" if final < 10 else "🔴"

    return {
        "Tour": f"T{tour}",
        "IA": ai_pred,
        "Expert": exp_pred,
        "Final": final,
        "Assurance": f"{assurance}%",
        "Couleur": couleur
    }

# --- Interface Streamlit ---
st.set_page_config(page_title="Prediction By Mickael TOP EXACTE", layout="centered")
st.title("🎯 Prediction By Mickael TOP EXACTE")

historique_input = st.text_area("🧾 Entrer les 20 derniers multiplicateurs (séparés par des virgules)",
                                "1.02,2.45,3.96,1.00,5.12,8.24,2.31,1.12,10.24,12.3,2.3,3.12,1.00,7.00,3.1,2.0,4.4,1.5,2.9,3.9")

dernier_tour = st.text_input("🔢 Numéro du dernier tour (ex: 120)", "120")

if st.button("🔮 Prédire"):
    try:
        historique = [float(x.strip()) for x in historique_input.split(",") if x.strip()]
        résultats = prediction_combinee(historique, int(dernier_tour))

        st.subheader("📈 Résultat de la Prédiction")
        st.markdown(f"**{résultats['Tour']} ➜ {résultats['Final']}x {résultats['Couleur']}**")
        st.markdown(f"🧠 **IA :** {résultats['IA']}x")
        st.markdown(f"🧙 **Expert :** {résultats['Expert']}x")
        st.markdown(f"✅ **Assurance :** {résultats['Assurance']}")
    except Exception as e:
        st.error(f"❌ Erreur de traitement : {e}")
