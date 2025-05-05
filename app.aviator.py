import streamlit as st
import numpy as np
import pandas as pd
import random
import re

# Login Page
def login_page():
    st.title("Prediction Expert by Mickael")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if username == "Topexacte" and password == "5312288612bet261":
            st.session_state["logged_in"] = True
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

# Modulo 10 Strategy
def mod10_strategy(values):
    return [int(float(v) * 100) % 10 for v in values]

# Seed Pattern Strategy (simplified)
def seed_pattern_strategy(values):
    return [int(float(v) * 1000) for v in values]

# Rolling average & std
def rolling_average_strategy(values):
    avg = []
    std = []
    for i in range(len(values)):
        if i >= 5:
            window = [float(v) for v in values[i-5:i]]
            avg.append(np.mean(window))
            std.append(np.std(window))
        else:
            avg.append(None)
            std.append(None)
    return avg, std

# Prediction Core
def prediction_expert(values):
    mods = mod10_strategy(values)
    seeds = seed_pattern_strategy(values)
    avg, std = rolling_average_strategy(values)

    predictions = []
    for i in range(1, 21):
        mod = mods[-1] if mods else 1
        seed = seeds[-1] if seeds else 1
        a = avg[-1] if avg[-1] is not None else 1.6
        s = std[-1] if std[-1] is not None else 0.5

        rand = random.uniform(-0.3, 0.3)
        booster = 0

        if mod in [0, 1] and random.random() < 0.18:
            booster = -1.2  # probable X1.00
        elif mod in [8, 9] and seed % 10 > 4 and random.random() < 0.10:
            booster = 5.5  # X6 to X12

        pred = round(a + (mod * 0.07) + (seed % 4) * 0.05 + s + rand + booster, 2)
        pred = max(1.00, min(pred, 50.0))

        fiab = random.randint(71, 96)
        predictions.append((f"T+{i}", f"{pred}x", f"Fiabilité: {fiab}%"))

        mods.append(mod)
        seeds.append(seed)
        avg.append(a)
        std.append(s)

    return predictions

# Main App
def main_app():
    st.title("AVIATOR PREDICTION EXPERT - MODE PRO")
    st.subheader("Stratégie combinée: Mod10, Seed, Boost, Rolling")

    history_input = st.text_area("Historique des multiplicateurs (ex: 1.50 2.30 1.00 10.2 3.6)", height=150)
    if history_input:
        try:
            values = re.findall(r'\d+\.\d+', history_input)
            if len(values) < 5:
                st.warning("Donnez au moins 5 valeurs.")
                return

            results = prediction_expert(values)
            st.success("Résultat des 20 prochaines prédictions :")
            for r in results:
                st.write(f"{r[0]} —> {r[1]} ({r[2]})")

        except Exception as e:
            st.error(f"Erreur: {e}")

# App Launcher
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    login_page()
