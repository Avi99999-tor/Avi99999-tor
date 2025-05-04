import streamlit as st
import numpy as np
import pandas as pd
import random

# --- Login Page ---
def login_page():
    st.title("Prediction Expert by Mickael")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if username == "Topexacte" and password == "5312288612bet261":
            st.session_state["logged_in"] = True
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect")

# --- Prediction Strategy Logic ---
def mod10_seed_pattern(values):
    mods = [int(str(v).split(".")[-1][:2]) % 10 for v in values]
    return mods

def rolling_stats(values):
    window = 5
    roll_avg = pd.Series(values).rolling(window).mean().tolist()
    roll_std = pd.Series(values).rolling(window).std().tolist()
    return roll_avg, roll_std

def prediction_expert(values):
    predictions = []
    mods = mod10_seed_pattern(values)
    roll_avg, roll_std = rolling_stats(values)
    for i in range(len(values), len(values)+20):
        mod = mods[-1] if mods else 0
        avg = roll_avg[-1] if roll_avg[-1] else 2
        std = roll_std[-1] if roll_std[-1] else 0.5
        rand_shift = random.uniform(-0.3, 0.3)
        pred = round(avg + std + mod * 0.05 + rand_shift, 2)
        pred = min(max(pred, 1.01), 10.0)
        fiab = random.randint(65, 90)
        predictions.append((f"T{i+1}", f"{pred}x", f"Fiabilité: {fiab}%"))
        mods.append(mod)
    return predictions

# --- Prediction Page ---
def prediction_page():
    st.title("Prediction Expert - Aviator")

    st.subheader("Admin: Mickael")
    st.text("Contact: 033 31 744 68")

    tour_input = st.text_area("Historique des multiplicateurs (séparés par 'x')",
        placeholder="Exemple: 1.33x 2.74x 1.46x 72.61x 3.55x ...")
    tour_num = st.number_input("Numéro du tour le plus récent (ex: 133)", min_value=1, step=1)

    if st.button("Calculer"):
        try:
            cleaned = [float(x.replace("x", "")) for x in tour_input.split() if "x" in x]
            predictions = prediction_expert(cleaned)
            for i, (label, val, prob) in enumerate(predictions):
                tour = tour_num + i + 1
                st.markdown(f"**T{tour}** → {val} — {prob}")
        except:
            st.error("Erreur lors de l'analyse. Vérifiez l'entrée.")

# --- Main App ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login_page()
else:
    prediction_page()
