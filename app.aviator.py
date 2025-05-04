import streamlit as st
import numpy as np
import pandas as pd
import random

# --- Authentification ---
def check_login(username, password):
    return username == "Topexacte" and password == "5312288612bet261"

def calculate_predictions(history):
    multipliers = [float(x.replace("x", "")) for x in history.split()]
    predictions = []
    for i in range(1, 21):
        recent = multipliers[-5:]
        avg = np.mean(recent)
        std = np.std(recent)
        mod_vals = [int(str(x).split(".")[-1]) % 10 for x in recent if '.' in str(x)]
        mod_score = sum([1 for m in mod_vals if m in [2, 4, 7]])  # simple pattern

        pred_base = avg + random.uniform(-0.4, 0.6)
        fiab = 60 + min(40, max(0, 10 * (mod_score + (std > 1.2) + (avg < 2.0))))
        
        if pred_base < 1.2:
            fiab -= 10
        
        predictions.append({
            "Tour": f"T{i + len(multipliers)}",
            "Prédiction": round(pred_base, 2),
            "Fiabilité": f"{min(99, max(30, int(fiab)))}%"
        })
        multipliers.append(pred_base)
    return pd.DataFrame(predictions)

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
    
    if st.button("Calculer les prédictions"):
        if history_input.strip() == "":
            st.warning("Veuillez entrer l'historique des multiplicateurs.")
        else:
            st.markdown("---")
            st.subheader("Résultats des prédictions (T+1 à T+20)")
            df = calculate_predictions(history_input)
            st.dataframe(df, use_container_width=True)
