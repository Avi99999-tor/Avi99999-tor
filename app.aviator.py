import streamlit as st
import numpy as np
import pandas as pd
import random
import re

# --- Authentification ---
def check_login(username, password):
    return username == "Topexacte" and password == "5312288612bet261"

# --- Calculation of predictions ---
def calculate_predictions(history, last_tour):
    multipliers = [float(x.replace("x", "")) for x in history.split()]
    predictions = []
    
    for i in range(1, 21):
        recent = multipliers[-5:]
        avg = np.mean(recent)
        std = np.std(recent)
        mod_vals = [int(str(x).split(".")[-1]) % 10 for x in recent if '.' in str(x)]
        mod_score = sum([1 for m in mod_vals if m in [2, 4, 7]])  # simple pattern

        # Applying mod 10 strategy
        mod_10 = (sum(mod_vals) % 10) / 10
        pred_base = avg + random.uniform(-0.4, 0.6) + mod_10
        
        # Apply x10 boost strategy
        if avg > 5:
            pred_base *= 1.2
        
        # Apply rolling dynamic strategy (based on recent trends)
        if std > 1.5:
            pred_base += 0.3
        
        # Apply pattern clustering strategy (cluster recent values)
        if len(set(recent)) < 3:
            pred_base += 0.2
        
        # Apply reverse entropy approximation (based on the entropy of the recent values)
        entropy = -sum([p * np.log2(p) if p > 0 else 0 for p in np.histogram(recent, bins=3)[0] / len(recent)])
        pred_base += entropy * 0.5

        # Predicted value and its reliability
        fiab = 60 + min(40, max(0, 10 * (mod_score + (std > 1.2) + (avg < 2.0))))
        if pred_base < 1.2:
            fiab -= 10
        fiab = min(99, max(30, int(fiab)))
        
        # Assign color based on multiplier value
        if pred_base < 2:
            color = "💙"  # Blue
        elif 2 <= pred_base < 10:
            color = "💜"  # Purple
        else:
            color = "💗"  # Pink
        
        predictions.append({
            "Tour": f"T{last_tour + i}",
            "Prédiction": round(pred_base, 2),
            "Fiabilité": f"{fiab}%",
            "Couleur": color
        })
        multipliers.append(pred_base)
    
    return predictions

# --- Interface ---
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
    st.markdown("*Format: 1.22x 3.45x 1.00x ...*")
    history_input = st.text_area("Historique des tours précédents", height=150)
    
    # Input for last tour number
    last_tour_input = st.number_input("Numéro du dernier tour", value=0, step=1)
    
    if st.button("Calculer les prédictions"):
        if history_input.strip() == "":
            st.warning("Veuillez entrer l'historique des multiplicateurs.")
        else:
            st.markdown("---")
            st.subheader("Résultats des prédictions (T+1 à T+20)")
            
            predictions = calculate_predictions(history_input, last_tour_input)
            
            # Affichage des prédictions en liste
            for prediction in predictions:
                st.markdown(f"**{prediction['Tour']}**: {prediction['Prédiction']} x {prediction['Couleur']} - Fiabilité: {prediction['Fiabilité']}")
