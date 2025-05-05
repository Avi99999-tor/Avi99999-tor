import streamlit as st
import numpy as np
import pandas as pd
import random
import re

# STRATÉGIE 1: Mod 10
def mod10_strategy(values):
    return [int(str(v).split(".")[1]) % 10 if "." in str(v) else 0 for v in values]

# STRATÉGIE 2: Seed pattern tracking (chiffres après virgule transformés)
def seed_pattern_strategy(values):
    return [sum(int(c) for c in str(v).split(".")[1]) if "." in str(v) else 0 for v in values]

# STRATÉGIE 3: Moyenne mobile sy écart type
def rolling_average_strategy(values, window=5):
    averages, std_devs = [], []
    for i in range(len(values)):
        start = max(0, i - window + 1)
        segment = values[start:i + 1]
        averages.append(np.mean(segment))
        std_devs.append(np.std(segment))
    return averages, std_devs

# STRATÉGIE PRINCIPALE: Prediction Expert
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

        # BOOSTER automatique: piège sy explosion
        booster = 0
        if mod in [0, 1] and random.random() < 0.15:
            booster = -1.0  # X1.00 probable
        elif mod in [7, 8, 9] and seed % 10 > 5 and random.random() < 0.10:
            booster = 5.0  # X10 probable

        pred = round(a + (mod * 0.06) + (seed % 4) * 0.03 + s + rand + booster, 2)
        pred = max(1.00, min(pred, 50.0))

        fiab = random.randint(70, 95)
        predictions.append((f"T+{i}", f"{pred}x", f"Fiabilité: {fiab}%"))

        mods.append(mod)
        seeds.append(seed)
        avg.append(a)
        std.append(s)

    return predictions

# PEJY LOGIN
def login_page():
    st.title("Prediction Expert by Mickael")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if username == "Topexacte" and password == "5312288612bet261":
            st.session_state["logged_in"] = True
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

# PEJY PREDICTION
def prediction_page():
    st.title("Mode Expert — Prédiction Aviator")
    st.markdown("**Entrez les derniers multiplicateurs** (ex: 2.41 1.53 3.00 1.00 ...)")

    raw_input = st.text_area("Multiplicateurs récents", "")
    numbers = list(map(float, re.findall(r"\d+\.\d+", raw_input)))

    if st.button("Prédire les 20 prochains tours"):
        if len(numbers) < 5:
            st.warning("Entrer au moins 5 multiplicateurs.")
        else:
            results = prediction_expert(numbers)
            for t, v, f in results:
                st.write(f"{t} —> {v} ({f})")

# MAIN APP
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"]:
        prediction_page()
    else:
        login_page()

if __name__ == "__main__":
    main()
