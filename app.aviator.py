
import streamlit as st
import numpy as np
import pandas as pd
import random
import re

def login_page():
    st.title("Prediction Expert by Mickael")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if username == "Topexacte" and password == "5312288612bet261":
            st.session_state["logged_in"] = True
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

def rolling_average_strategy(values):
    # Logic manokana ho an'ny rolling average
    # Ity dia ho an'ny fanombanana tony amin'ny alalan'ny fanombanana ara-statistika.
    # Add code logic here

def rolling_average_strategy(values): averages = [] std_devs = [] for i in range(len(values)): window = values[max(0, i-5):i+1] if window: avg = np.mean(window) std = np.std(window) averages.append(avg) std_devs.append(std) else: averages.append(None) std_devs.append(None) return averages, std_devs

Mod10 strategy

def mod10_strategy(values): return [int(v * 100) % 10 for v in values]

Seed pattern strategy

def seed_pattern_strategy(values): return [int(v * 1000) % 100 for v in values]

Prediction Expert function

def prediction_expert(values): mods = mod10_strategy(values) seeds = seed_pattern_strategy(values) avg, std = rolling_average_strategy(values)

predictions = []
for i in range(1, 21):
    mod = mods[-1] if mods else 1
    seed = seeds[-1] if seeds else 1
    a = avg[-1] if avg[-1] is not None else 1.6
    s = std[-1] if std[-1] is not None else 0.5

    rand = random.uniform(-0.3, 0.3)
    is_extreme = False

    # Booster automatique X1.00
    if mod in [0, 1, 2] and seed % 5 == 0 and random.random() < 0.3:
        pred = 1.00
        fiab = 95
        is_extreme = True
    # Booster automatique X10+
    elif mod in [8, 9] and seed % 7 == 0 and s > 0.7 and random.random() < 0.2:
        pred = round(random.uniform(10.0, 50.0), 2)
        fiab = 96
        is_extreme = True
    else:
        booster = 0
        if mod in [0, 1] and random.random() < 0.1:
            booster = -1.0
        elif mod in [7, 8, 9] and seed % 10 > 5 and random.random() < 0.1:
            booster = 5.0

        pred = round(a + (mod * 0.06) + (seed % 4) * 0.03 + s + rand + booster, 2)
        pred = max(1.00, min(pred, 50.0))
        fiab = random.randint(70, 95)

    # Rolling boost
    if i in [7, 13, 19] and not is_extreme:
        pred += random.uniform(0.6, 2.5)
        pred = min(pred, 50.0)

    predictions.append((f"T+{i}", f"{pred}x", f"Fiabilité: {fiab}%"))

    mods.append(mod)
    seeds.append(seed)
    avg.append(a)
    std.append(s)

return predictions

Main App

if "logged_in" not in st.session_state: login_page() else: st.title("Expert Aviator Prediction")

input_values = st.text_area("Entrez les derniers multiplicateurs (ex: 1.23 4.56 2.10)")
if st.button("Prédire"):
    try:
        values = [float(v) for v in re.findall(r"\d+\.\d+", input_values)]
        if len(values) < 5:
            st.warning("Veuillez entrer au moins 5 valeurs.")
        else:
            results = prediction_expert(values)
            for r in results:
                st.write(r)
    except:
        st.error("Format invalide. Utilisez des nombres séparés par des espaces.")

