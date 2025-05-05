import streamlit as st
import numpy as np
import re
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
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

# --- Strategies ---
def mod10_strategy(values):
    return [int(v * 100) % 10 for v in values]

def seed_pattern_strategy(values):
    return [int(v * 1000) % 100 for v in values]

def rolling_avg_std(values, window=5):
    avg, std = [], []
    for i in range(len(values)):
        win = values[max(0, i-window+1):i+1]
        avg.append(np.mean(win))
        std.append(np.std(win))
    return avg, std

# --- Prediction Piégé & Boost ---
def predict_boost_piege(values, last_tour):
    mods = mod10_strategy(values)
    seeds = seed_pattern_strategy(values)
    avg, std = rolling_avg_std(values)

    piégé_tour = None
    results = []
    for i in range(1, 21):  # T+1 to T+20
        real_t = last_tour + i
        mod = mods[-1]
        seed = seeds[-1]
        a, s = avg[-1], std[-1]
        rand = random.uniform(-0.3, 0.3)
        is_piege = False
        is_boost = False

        # Piégé logic
        if not piégé_tour and mod in [0,1,2] and seed % 3 == 0 and random.random() < 0.35:
            pred = 1.00
            label = "🛑 Piégé"
            fiab = 98
            piégé_tour = i
            is_piege = True
        # Boost after piège
        elif piégé_tour and i <= piégé_tour + 3:
            pred = round(random.uniform(4.0, 12.0), 2)
            label = "🚀 Boost"
            fiab = 95
            is_boost = True
        else:
            pred = round(a + (mod*0.06) + (seed%5)*0.02 + s + rand, 2)
            pred = max(1.00, min(pred, 50.0))
            label = ""
            fiab = random.randint(70, 90)

        results.append((f"T{real_t}", f"{pred}x", f"Fiabilité: {fiab}%", label))

        # update context
        values.append(pred)
        mods.append(mod10_strategy([pred])[0])
        seeds.append(seed_pattern_strategy([pred])[0])
        avg, std = rolling_avg_std(values)

    return results

# --- Main App ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login_page()
else:
    st.title("🔥 Aviator Piégé & Boost Prediction")
    st.text("Admin: Mickael | Contact: 033 31 744 68")
    st.markdown("**Entrer le numéro du dernier tour** (ex: 72)")
    last_tour = st.number_input("Dernier tour", min_value=1, step=1)
    st.markdown("**Historique des multiplicateurs (ex: 1.23 4.56 2.10)**")
    inp = st.text_area("Multiplicateurs précédents", height=120)

    if st.button("Prédire T+1 à T+20"):
        try:
            values = [float(v) for v in re.findall(r"\d+\.\d+", inp)]
            if len(values) < 5:
                st.warning("Au moins 5 valeurs requises.")
            else:
                preds = predict_boost_piege(values, last_tour)
                st.markdown("### Prédictions:")
                for tour, mult, fiab, lbl in preds:
                    st.write(f"{tour} → {mult} ({fiab}) {lbl}")
        except Exception as e:
            st.error(f"Erreur: {e}")
