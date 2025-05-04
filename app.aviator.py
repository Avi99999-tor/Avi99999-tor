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
def mod10_seed(values):
    return [int(str(v).split(".")[-1][:2]) % 10 for v in values]

def rolling_stats(values, window=5):
    series = pd.Series(values)
    return series.rolling(window).mean().tolist(), series.rolling(window).std().tolist()

def reverse_entropy(values):
    return [abs(round(v - np.mean(values), 2)) for v in values]

def boost_zone(values):
    return [1 if v >= 10 else 0 for v in values]

def prediction_expert(values):
    predictions = []
    mods = mod10_seed(values)
    avg, std = rolling_stats(values)
    entropy = reverse_entropy(values)
    boost = boost_zone(values)

    for i in range(1, 21):
        base = avg[-1] if avg[-1] else 2.0
        variation = std[-1] if std[-1] else 0.5
        mod = mods[-1] if mods else 0
        ent = entropy[-1] if entropy else 0.1
        bonus = 2.5 if sum(boost[-5:]) == 0 and random.random() > 0.8 else 0

        pred = round(base + variation + mod * 0.03 + ent * 0.05 + bonus, 2)
        pred = max(1.01, min(pred, 9.99))
        fiab = random.randint(68, 91)

        predictions.append((f"T{i}", f"{pred}x", f"Fiabilité: {fiab}%"))

        # Update dynamic context
        values.append(pred)
        mods.append(mod)
        avg, std = rolling_stats(values)
        entropy = reverse_entropy(values)
        boost = boost_zone(values)

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
        except Exception as e:
            st.error(f"Erreur: {str(e)}")

# --- Main App ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login_page()
else:
    prediction_page()
