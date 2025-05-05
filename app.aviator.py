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
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

# --- Strategies ---
def mod10_strategy(values):
    return [int(str(v).split(".")[-1][:2]) % 10 for v in values]

def rolling_average_strategy(values, window=5):
    s = pd.Series(values)
    avg = s.rolling(window).mean().tolist()
    std = s.rolling(window).std().tolist()
    return avg, std

def seed_pattern_strategy(values):
    seeds = []
    for v in values:
        if "." in str(v):
            decimals = str(v).split(".")[1]
            seed = int(decimals[:2]) if len(decimals) >= 2 else int(decimals + "0")
            seeds.append(seed)
        else:
            seeds.append(0)
    return seeds

# --- Prediction Expert Logic ---
def prediction_expert(values):
    mods = mod10_strategy(values)
    seeds = seed_pattern_strategy(values)
    avg, std = rolling_average_strategy(values)

    predictions = []
    for i in range(1, 21):
        mod = mods[-1] if mods else 1
        seed = seeds[-1] if seeds else 1
        a = avg[-1] if avg[-1] is not None else 1.5
        s = std[-1] if std[-1] is not None else 0.4

        # Logique probabiliste ajustée
        rand = random.uniform(-0.2, 0.2)
        pred = round(a + (mod * 0.05) + (seed % 3) * 0.03 + s + rand, 2)
        pred = min(max(pred, 1.01), 10.0)

        fiab = random.randint(68, 92)
        predictions.append((f"T+{i}", f"{pred}x", f"Fiabilité: {fiab}%"))

        mods.append(mod)
        seeds.append(seed)
        avg.append(a)
        std.append(s)

    return predictions

# --- Prediction Page ---
def prediction_page():
    st.title("Mode Expert - Aviator Prediction")

    st.subheader("Admin: Mickael")
    st.text("Contact: 033 31 744 68")

    input_text = st.text_area("Historique des multiplicateurs (séparés par 'x')",
        placeholder="Exemple: 1.33x 2.74x 1.46x 72.61x ...")
    tour_number = st.number_input("Numéro du tour le plus récent", min_value=1, step=1)

    if st.button("Prédire"):
        try:
            cleaned = [float(x.replace("x", "")) for x in input_text.split() if "x" in x]
            preds = prediction_expert(cleaned)
            for i, (label, val, conf) in enumerate(preds):
                st.markdown(f"**T{tour_number + i + 1}** → {val} — {conf}")
        except Exception as e:
            st.error(f"Erreur lors du traitement: {e}")

# --- Main App ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login_page()
else:
    prediction_page()
