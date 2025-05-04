import streamlit as st import numpy as np import pandas as pd import random import re

--- Authentification ---

def check_login(username, password): return username == "Topexacte" and password == "5312288612bet261"

--- Strategy helpers ---

def clean_history(history): raw_values = history.split() clean_values = [] errors = [] for val in raw_values: cleaned = val.lower().replace('x', '') try: clean_values.append(float(cleaned)) except: errors.append(val) return clean_values, errors

--- Prediction Core Logic ---

def calculate_predictions(history, last_tour): multipliers, errors = clean_history(history) predictions = []

for i in range(1, 21):
    recent = multipliers[-5:] if len(multipliers) >= 5 else multipliers
    avg = np.mean(recent)
    std = np.std(recent)

    # Mod 10 Strategy
    mod_vals = [int(str(x).split(".")[-1]) % 10 for x in recent if '.' in str(x)]
    mod_score = sum([1 for m in mod_vals if m in [2, 4, 7]])

    # Reverse entropy approximation (heuristic)
    entropy = len(set(mod_vals)) / 10

    # Base prediction
    pred_base = avg + random.uniform(-0.4, 0.6)

    # Fiabilité estimate
    fiab = 60 + min(40, max(0, 10 * (mod_score + (std > 1.2) + (avg < 2.0) - entropy)))
    if pred_base < 1.2:
        fiab -= 10

    tag = ""
    if pred_base >= 5.0:
        tag = "X5+"
    if pred_base >= 10.0:
        tag = "X10+"
    if round(pred_base, 2) <= 1.01:
        tag = "PIÈGE X1.00"

    predictions.append({
        "Tour": f"T{last_tour + i}",
        "Prédiction": round(pred_base, 2),
        "Fiabilité": f"{min(99, max(30, int(fiab)))}%",
        "Tendance": tag
    })
    multipliers.append(pred_base)

return pd.DataFrame(predictions), errors

--- Streamlit App ---

st.set_page_config(page_title="Prediction Expert by Mickael", layout="centered")

st.markdown("### Prediction Expert by Mickael") st.markdown("Admin: Mickael  |  Contact: 033 31 744 68") st.markdown("---")

if "authenticated" not in st.session_state: st.session_state.authenticated = False

if not st.session_state.authenticated: with st.form("login_form"): username = st.text_input("Nom d'utilisateur") password = st.text_input("Mot de passe", type="password") submitted = st.form_submit_button("Se connecter") if submitted and check_login(username, password): st.session_state.authenticated = True st.success("Connexion réussie!") elif submitted: st.error("Nom d'utilisateur ou mot de passe incorrect.") else: st.success("Connecté en tant que Topexacte") st.markdown("### Entrer l'historique des multiplicateurs") st.markdown("Format: 1.22x 3.45x 1.00x ...")

with st.form("history_form"):
    history_input = st.text_area("Historique des tours précédents (max 20)", height=150)
    last_tour = st.number_input("Numéro du dernier tour", min_value=0, step=1)
    submitted = st.form_submit_button("Calculer les prédictions")

    if submitted:
        clean_hist, hist_errors = clean_history(history_input)
        if len(clean_hist) > 20:
            st.error("Veuillez entrer un maximum de 20 tours.")
        elif len(clean_hist) < 5:
            st.warning("Au moins 5 valeurs sont recommandées pour une bonne précision.")
        else:
            df, errors = calculate_predictions(history_input, int(last_tour))
            if errors:
                st.warning(f"Les valeurs suivantes sont incorrectes: {' '.join(errors)}")
            st.markdown("---")
            st.subheader("Résultats des prédictions (T+1 à T+20)")
            st.dataframe(df, use_container_width=True)

if st.button("Effacer l'historique"):
    st.experimental_rerun()

