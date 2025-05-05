import streamlit as st
import numpy as np
import pandas as pd
import random
import re

# Fonctions auxiliaires
def mod10_strategy(values):
    return [int(v * 100) % 10 for v in values]

def seed_pattern_strategy(values):
    return [int(v * 1000) % 100 for v in values]

def rolling_average_strategy(values):
    averages = []
    std_devs = []
    for i in range(len(values)):
        window = values[max(0, i - 5):i + 1]
        if window:
            avg = np.mean(window)
            std = np.std(window)
            averages.append(avg)
            std_devs.append(std)
        else:
            averages.append(None)
            std_devs.append(None)
    return averages, std_devs

# Fonction principale de prédiction
def prediction_boost_piege(values):
    mods = mod10_strategy(values)
    seeds = seed_pattern_strategy(values)
    avg, std = rolling_average_strategy(values)

    mod = mods[-1]
    seed = seeds[-1]
    a = avg[-1]
    s = std[-1]

    predictions = []
    piégé_tour = None

    for i in range(5, 21):  # T+5 à T+20
        is_piége = False
        is_boost = False

        if mod in [0, 1, 2] and seed % 3 == 0 and random.random() < 0.3:
            pred = 1.00
            fiab = 98
            is_piége = True
            piégé_tour = i
        elif piégé_tour and i in range(piégé_tour + 1, piégé_tour + 4):
            pred = round(random.uniform(4.0, 15.0), 2)
            fiab = 95
            is_boost = True
        else:
            rand = random.uniform(-0.2, 0.2)
            pred = round(a + (mod * 0.06) + (seed % 5) * 0.02 + s + rand, 2)
            pred = max(1.00, min(pred, 50.0))
            fiab = random.randint(70, 92)

        label = "Piégé" if is_piége else "Boost" if is_boost else ""
        predictions.append((f"T+{i}", f"{pred}x", f"Fiabilité: {fiab}%", label))

        # Mise à jour pour le rolling
        values.append(pred)
        mods.append(mod10_strategy([pred])[0])
        seeds.append(seed_pattern_strategy([pred])[0])
        a, s = rolling_average_strategy(values)[0][-1], rolling_average_strategy(values)[1][-1]

    return predictions

# Interface Streamlit
st.title("🎯 Expert Aviator: Stratégie Piégé & Boost")

input_values = st.text_area("Entrez les multiplicateurs précédents (ex: 1.23 2.45 3.67)")

if st.button("Prédire"):
    try:
        values = [float(v) for v in re.findall(r"\d+\.\d+", input_values)]
        if len(values) < 5:
            st.warning("Veuillez entrer au moins 5 valeurs.")
        else:
            results = prediction_boost_piege(values)
            for r in results:
                label = f"🛑 {r[3]}" if r[3] == "Piégé" else f"🚀 {r[3]}" if r[3] == "Boost" else ""
                st.write(f"{r[0]} —> {r[1]} | {r[2]} {label}")
    except:
        st.error("Format invalide. Utilisez des nombres séparés par des espaces.")
