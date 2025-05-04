import streamlit as st
import numpy as np
import pandas as pd
import random
import re

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

# --- Strategies ---
def mod10_seed_pattern(values):
    mods = [int(str(v).split(".")[-1][:2]) % 10 for v in values]
    return mods

def rolling_stats(values):
    window = 5
    roll_avg = pd.Series(values).rolling(window).mean().tolist()
    roll_std = pd.Series(values).rolling(window).std().tolist()
    return roll_avg, roll_std

def avoid_high_spikes(values):
    if values[-1] > 10:
        return 1.5 + random.uniform(-0.2, 0.2)
    return None

def smart_prediction(values):
    predictions = []
    mods = mod10_seed_pattern(values)
    roll_avg, roll_std = rolling_stats(values)

    for i in range(20):
        avg = roll_avg[-1] if roll_avg[-1] else 2.0
        std = roll_std[-1] if roll_std[-1] else 0.5
        mod = mods[-1] if mods else 0

        avoid_spike = avoid_high_spikes(values)
        if avoid_spike:
            pred = avoid_spike
        else:
            rand_shift = random.uniform(-0.3, 0.3)
            pred = avg + std * 0.5 + mod * 0.07 + rand_shift
        pred = round(min(max(pred, 1.01), 10.0), 2)
        fiab = random.randint(67, 91)
        predictions.append((pred, fiab))
        values.append(pred)
        mods.append(mod)
    return predictions

# --- Prediction Page ---
def prediction_page():
    st.title("Prediction Expert - Aviator")
    st.subheader("Admin: Mickael")
    st.text("Contact: 033 31 744 68")

    tour_input = st.text_area("Historique des multiplicateurs (séparés par 'x')",
        placeholder="Exemple: 1.33x 2.74x 1.46x 72.61x 3.55x ...")
    tour_num = st.number_input("Numéro du tour le plus récent", min_value=1, step=1)

    if st.button("Calculer"):
        try:
            cleaned = [float(x.replace("x", "").replace(",", ".")) for x in tour_input.split() if "x" in x]
            results = smart_prediction(cleaned)
            for i, (val, fiab) in enumerate(results):
                tour = int(tour_num) + i + 1
                st.markdown(f"**T{tour}** → {val}x — Fiabilité: {fiab}%")
        except:
            st.error("Erreur lors de l'analyse. Vérifiez les entrées.")

# --- Main App ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login_page()
else:
    prediction_page()
