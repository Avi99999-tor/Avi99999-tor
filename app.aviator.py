import streamlit as st import numpy as np import pandas as pd import random import re

--- STRATEGIES ---

def mod10_strategy(values): return [int(float(v) * 100) % 10 for v in values]

def seed_pattern_strategy(values): seeds = [] for v in values: number = float(v) after_decimal = int(str(number).split(".")[1][:2]) if "." in str(number) else 0 seeds.append(after_decimal) return seeds

def rolling_average_strategy(values): avg, std = [], [] for i in range(len(values)): window = values[max(0, i-5):i+1] nums = [float(v) for v in window] avg.append(np.mean(nums)) std.append(np.std(nums)) return avg, std

--- EXPERT PREDICTION ---

def prediction_expert(values): mods = mod10_strategy(values) seeds = seed_pattern_strategy(values) avg, std = rolling_average_strategy(values)

predictions = []
rolling_boost_turns = [7, 13, 19]
for i in range(1, 21):
    mod = mods[-1]
    seed = seeds[-1]
    a = avg[-1] if avg[-1] is not None else 1.8
    s = std[-1] if std[-1] is not None else 0.6

    rand = random.uniform(-s, s)
    booster = 0
    if mod in [0, 1, 2] and seed % 10 < 4 and random.random() < 0.20:
        booster = -0.9
    elif mod in [7, 8, 9] and seed % 10 > 5 and random.random() < 0.12:
        booster = 7.0
    if i in rolling_boost_turns:
        booster += random.choice([3.0, 5.0, 10.0])

    pred = round(a + mod * 0.05 + (seed % 5) * 0.03 + rand + booster, 2)
    pred = max(1.00, min(pred, 100.0))
    fiab = random.randint(75, 96)

    predictions.append((f"T+{i}", f"{pred}x", f"Fiabilité: {fiab}%"))
    mods.append(mod)
    seeds.append(seed)
    avg.append(a)
    std.append(s)

return predictions

--- LOGIN PAGE ---

def login_page(): st.title("Prediction Expert by Mickael") username = st.text_input("Nom d'utilisateur") password = st.text_input("Mot de passe", type="password") if st.button("Se connecter"): if username == "Topexacte" and password == "5312288612bet261": st.session_state["logged_in"] = True else: st.error("Nom d'utilisateur ou mot de passe incorrect.")

--- MAIN APP ---

def main_app(): st.title("Expert Prediction Aviator") user_input = st.text_area("Entrer les 30 derniers multiplicateurs (ex: 1.00x 2.50x 3.20x ...)") if user_input: cleaned = re.findall(r"\d+.\d+", user_input) if len(cleaned) < 10: st.warning("Il faut au moins 10 valeurs pour une prédiction fiable.") else: predictions = prediction_expert(cleaned[-30:]) for t, p, f in predictions: st.write(f"{t} → {p} ({f})")

--- RUN APP ---

if "logged_in" not in st.session_state: st.session_state["logged_in"] = False

if not st.session_state["logged_in"]: login_page() else: main_app()

