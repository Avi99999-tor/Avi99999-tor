import streamlit as st
import numpy as np
import pandas as pd
import random
import re

# --- Authentification ---
def check_login(username, password):
    return username == "Topexacte" and password == "5312288612bet261"

# --- Prediction logic ---
def calculate_predictions(history, last_tour):
    # Normalisation: remplacer X ou x par rien
    history = re.sub(r'[Xx]', '', history)
    parts = history.split()
    if len(parts) < 5:
        raise ValueError("Minimum 5 valeurs requises pour les prédictions.")

    try:
        multipliers = [float(x) for x in parts]
    except:
        raise ValueError("Une ou plusieurs valeurs ne sont pas valides.")

    if len(multipliers) > 20:
        multipliers = multipliers[-20:]

    predictions = []
    for i in range(1, 21):
        recent = multipliers[-5:]
        avg = np.mean(recent)
        std = np.std(recent)
        mod_vals = [int(str(x).split(".")[-1]) % 10 for x in recent]
        mod_score = sum([1 for m in mod_vals if m in [2, 4, 7]])

        # Reverse entropy approximation
        entropy = sum(abs(recent[i] - recent[i - 1]) for i in range(1, len(recent)))

        pred_base = avg + random.uniform(-0.4, 0.6)
        fiab = 60 + min(40, int(mod_score * 5 + (std * 3) + (entropy / 5)))

        if pred_base < 1.2:
            fiab -= 15

        predictions.append({
            "Tour": f"T{last_tour + i}",
            "Prédiction": round(pred_base, 2),
            "Fiabilité": f"{min(99, max(30, fiab))}%"
        })
        multipliers.append(pred_base)

    return pd.DataFrame(predictions)

# --- Interface ---
st.set_page_config(page_title="Prediction Expert by Mickael", layout="centered")

st.markdown("## **Prediction Expert by Mickael**")
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
    st.markdown("*Exemple: 1.22x 3.45x 1.00x ... (max 20 valeurs)*")
    
    with st.form("prediction_form"):
        history_input = st.text_area("Historique des tours précédents", height=150)
        last_tour = st.number_input("Numéro du dernier tour connu", min_value=0, step=1)
        submitted = st.form_submit_button("Calculer les prédictions")

        if submitted:
            if not history_input.strip():
                st.warning("Veuillez entrer l'historique des multiplicateurs.")
            else:
                try:
                    results = calculate_predictions(history_input, int(last_tour))
                    st.success("Prédictions générées avec succès!")
                    st.dataframe(results, use_container_width=True)
                except ValueError as e:
                    st.error(f"Erreur: {e}")

    if st.button("Effacer l’historique"):
        st.experimental_rerun()
