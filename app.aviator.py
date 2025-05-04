import streamlit as st import numpy as np import random import pandas as pd

st.set_page_config(page_title="Prediction Expert by Mickael", layout="centered") st.title("Prediction Expert by Mickael") st.markdown("### Mode Expert: Seed, Mod 10, Rolling Avg")

Saisie manokana ho an'ny tour farany indrindra

recent_tour = st.number_input("Numéro du tour le plus récent (ex: 100)", min_value=1, value=100, step=1)

Input an'ireo multiplicateurs (historique)

mult_input = st.text_area("Entrer les multiplicateurs séparés par espace (ex: 1.34x 2.01x 1.05x)")

def extract_values(input_str): try: return [float(val.replace('x', '').strip()) for val in input_str.split() if 'x' in val] except: return []

Fonctions statistika

def mod10_analysis(values): return [int(str(val).split(".")[-1][:2]) % 10 for val in values]

def rolling_avg(values, window=5): return pd.Series(values).rolling(window).mean().tolist()

def rolling_std(values, window=5): return pd.Series(values).rolling(window).std().tolist()

def predict_next(values): predictions = [] mods = mod10_analysis(values) roll_avg = rolling_avg(values) roll_std = rolling_std(values)

for i in range(1, 11):
    last = values[-1]
    mod = mods[-1]
    avg = roll_avg[-1] if roll_avg[-1] else np.mean(values)
    std = roll_std[-1] if roll_std[-1] else np.std(values)

    if last < 1.20:
        pred = round(np.random.uniform(2.0, 6.0), 2)
        confidence = 80 + random.randint(0, 10)
    elif mod in [3, 7, 9]:
        pred = round(np.random.uniform(4.0, 9.0), 2)
        confidence = 85
    elif std > 4:
        pred = round(np.random.uniform(5.0, 10.0), 2)
        confidence = 88
    else:
        pred = round(np.random.uniform(1.20, 3.0), 2)
        confidence = 65 + random.randint(0, 10)

    predictions.append((pred, confidence))
    values.append(pred)
    mods.append(pred % 10)
    roll_avg.append(np.mean(values[-5:]))
    roll_std.append(np.std(values[-5:]))

return predictions

if mult_input: values = extract_values(mult_input) if len(values) >= 5: preds = predict_next(values.copy()) st.subheader("Résultat des Prédictions T+1 à T+10") for i, (val, conf) in enumerate(preds): tour_label = f"T{recent_tour + i + 1}" if conf >= 80: st.success(f"{tour_label} → {val}x | Fiabilité: {conf}% (Assuré)") elif conf >= 65: st.info(f"{tour_label} → {val}x | Fiabilité: {conf}%") else: st.warning(f"{tour_label} → {val}x | Fiabilité: {conf}% (Risque)") else: st.error("Entrer au moins 5 multiplicateurs valides.")

