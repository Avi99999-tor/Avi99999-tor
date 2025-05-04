import streamlit as st
import numpy as np
import pandas as pd
import random
import re

# --- Authentification ---
def check_login(username, password):
    return username == "Topexacte" and password == "5312288612bet261"

# --- Prédiction avec stratégie sy coloration ---
def calculate_predictions(history, last_tour):
    clean_history = re.findall(r"(\d+\.\d+)[xX]", history)
    if len(clean_history) < 5:
        raise ValueError("Historique insuffisant (minimum 5 valeurs).")
    if len(clean_history) > 20:
        raise ValueError("Maximum 20 valeurs historiques autorisées.")
    
    multipliers = list(map(float, clean_history))
    predictions = []
    current_tour = last_tour

    for i in range(1, 21):
        recent = multipliers[-5:]
        avg = np.mean(recent)
        std = np.std(recent)
        mod_vals = [int(str(x).split(".")[-1]) % 10 for x in recent if '.' in str(x)]
        mod_score = sum([1 for m in mod_vals if m in [2, 4, 7]])

        pred_base = avg + random.uniform(-0.4, 0.6)
        fiab = 60 + min(40, max(0, 10 * (mod_score + (std > 1.2) + (avg < 2.0))))
        if pred_base < 1.2:
            fiab -= 10

        pred_round = round(pred_base, 2)
        if pred_round < 2.0:
            color = "💙"
        elif pred_round < 10.0:
            color = "💜"
        else:
            color = "💗"

        predictions.append({
            "Tour": f"T{current_tour + i}",
            "Prédiction": f"{color} x{pred_round}",
            "Fiabilité": f"{min(99, max(30, int(fiab)))}%"
        })
        multipliers.append(pred_base)

    return pd.DataFrame(predictions)

# --- Page Configuration ---
st.set_page_config(page_title="Prediction Expert by Mickael", layout="centered")
st.markdown("### **Prediction Expert by Mickael**")
st.markdown("**Admin:** Mickael  |  **Contact:** 033 31 744 68")
st.markdown("---")

# Login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    with st.form("login_form"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter")
        if submitted and check_login(username, password):
            st.session_state.authenticated = True
            st.success("Connexion réussie!")
        elif submitted:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")
else:
    st.success("Connecté en tant que Topexacte")
    st.markdown("### **Entrer l'historique des multiplicateurs**")
    st.markdown("*Format: 1.22x 3.45x 1.00x ... (max: 20 valeurs)*")

    with st.form("prediction_form"):
        history_input = st.text_area("Historique des tours précédents", height=150)
        last_tour = st.text_input("Numéro de la dernière tour", value="100")
        col1, col2 = st.columns([1, 1])
        with col1:
            submit_pred = st.form_submit_button("Calculer les prédictions")
        with col2:
            clear_input = st.form_submit_button("Effacer")
    
    if clear_input:
        st.experimental_rerun()

    if submit_pred:
        if not history_input.strip():
            st.warning("Veuillez entrer l'historique.")
        elif not last_tour.isdigit():
            st.error("Le numéro de la dernière tour doit être un entier.")
        else:
            try:
                results = calculate_predictions(history_input, int(last_tour))
                st.subheader("Résultats des prédictions (T+1 à T+20)")
                for index, row in results.iterrows():
                    st.markdown(f"- **{row['Tour']}** → {row['Prédiction']} — {row['Fiabilité']}")
            except ValueError as e:
                st.error(str(e))
