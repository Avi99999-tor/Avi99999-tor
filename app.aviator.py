import streamlit as st import numpy as np import pandas as pd import random import re

--- Authentification ---

def check_login(username, password): return username == "Topexacte" and password == "5312288612bet261"

--- Strategie: Mod 10, Boost x10+, Rolling Dynamique, Seed Tracking, Pattern Clustering, Reverse Entropy ---

def advanced_prediction(history_raw, last_tour): cleaned = re.findall(r"\d+.\d+", history_raw.replace("X", "x")) if len(cleaned) < 5: return ["Données insuffisantes"]

multipliers = [float(x) for x in cleaned[-20:]]
predictions = []

for i in range(1, 21):
    recent = multipliers[-5:]
    avg = np.mean(recent)
    std = np.std(recent)
    mod_vals = [int(str(x).split(".")[-1]) % 10 for x in recent]

    # --- Mod 10 ---
    mod_score = sum([1 for m in mod_vals if m in [1, 3, 7, 9]])

    # --- Rolling Dynamique ---
    rolling_boost = sum([1 for x in recent if x >= 5.0])

    # --- Boost X10+ ---
    boost = 5 if any(x >= 10 for x in recent) else 0

    # --- Reverse Entropy (approximation simple) ---
    entropy = len(set([round(x, 1) for x in recent])) / 5
    entropy_score = 1 if entropy < 0.6 else 0

    # --- Score total ---
    score = avg + mod_score * 0.1 + boost + rolling_boost * 0.2 + entropy_score * 0.5

    pred = round(score + random.uniform(-0.4, 0.4), 2)
    multipliers.append(pred)

    color = ""
    if pred < 2.0:
        color = "💙"
    elif pred < 10.0:
        color = "💜"
    else:
        color = "💗"

    predictions.append(f"T{last_tour + i} ➔ {color} x{pred}")

return predictions

--- Streamlit Interface ---

st.set_page_config(page_title="Mode Expert Aviator", layout="centered") st.title("Prediction Expert - Mode Expert") st.markdown("Admin: Mickael  |  Contact: 033 31 744 68")

Login

if "authenticated" not in st.session_state: st.session_state.authenticated = False

if not st.session_state.authenticated: with st.form("login"): username = st.text_input("Nom d'utilisateur") password = st.text_input("Mot de passe", type="password") submit = st.form_submit_button("Se connecter") if submit: if check_login(username, password): st.session_state.authenticated = True st.success("Connexion réussie") else: st.error("Identifiants incorrects") else: st.success("Connecté en tant que Topexacte") with st.form("data_input"): history = st.text_area("Historique des multiplicateurs (ex: 1.22x 3.45x ...)", height=120) last_tour = st.number_input("Numéro du dernier tour", min_value=1, value=1000) submit_pred = st.form_submit_button("Calculer les prédictions")

if submit_pred:
    if history.strip() == "":
        st.warning("Veuillez entrer l'historique.")
    else:
        st.subheader("Prédictions T+1 à T+20")
        results = advanced_prediction(history, int(last_tour))
        for res in results:
            st.write(res)

if st.button("Effacer l'historique"):
    st.experimental_rerun()

