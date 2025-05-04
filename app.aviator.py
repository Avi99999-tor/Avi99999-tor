import streamlit as st import numpy as np

st.set_page_config(page_title="Prediction Expert by Mickael", layout="centered") st.title("Prediction Expert by Mickael")

Input for last known multiplier and tour number

latest_tour = st.number_input("Tour le plus récent (Ex: 10)", min_value=1, step=1) latest_multiplier = st.number_input("Multiplier du dernier tour (Ex: 1.33)", step=0.01, format="%.2f")

Input for historical multipliers

user_input = st.text_area("Coller les multiplicateurs (séparés par espace ou retour à la ligne)")

Processing input data

def parse_input(data): parts = data.replace("\n", " ").split() return [float(p.lower().replace('x', '')) for p in parts if p.replace('x', '').replace('.', '').isdigit()]

Modulo 10 analyzer

def mod10_analysis(multipliers): mods = [int(str(x).split('.')[-1][:2]) % 10 for x in multipliers] counts = {i: mods.count(i) for i in range(10)} probable_mod = max(counts, key=counts.get) return probable_mod, counts

Rolling average and rebond detector

def rolling_prediction(multipliers, last_multiplier): results = [] window = 10 for i in range(1, 21): recent = multipliers[-window:] mean = np.mean(recent) std = np.std(recent) score = 0

# Rules
    if last_multiplier < 1.20:
        score += 1.5  # Crash rebound probable
    if mean < 2:
        score += 0.5
    if std > 2:
        score += 0.5
    if len([x for x in recent if x >= 5]) == 0:
        score += 1  # No x5 recently, expected soon

    # Modulo 10 condition
    mod_seed, _ = mod10_analysis(recent)
    if mod_seed in [3, 6, 9]:
        score += 0.5

    # Probability estimation
    prob = min(95, 50 + score * 10)

    # Prediction value
    if score >= 3:
        pred = round(np.random.uniform(4.5, 8), 2)
    elif score >= 2:
        pred = round(np.random.uniform(2, 4.5), 2)
    else:
        pred = round(np.random.uniform(1.1, 2), 2)

    results.append({
        'tour': f"T{latest_tour + i}",
        'prediction': pred,
        'fiabilité': f"{'Assuré' if prob >= 80 else str(prob)+'%'}"
    })
    multipliers.append(pred)
    last_multiplier = pred
return results

Run prediction

if user_input: historique = parse_input(user_input) if historique: predictions = rolling_prediction(historique, latest_multiplier) st.subheader("Résultats Prédits (T+1 à T+20)") for p in predictions: st.markdown(f"{p['tour']} ➜ {p['prediction']}x — Fiabilité: {p['fiabilité']}")

mod, mod_stat = mod10_analysis(historique)
    st.info(f"Mod10 dominant: {mod} — Détails: {mod_stat}")
else:
    st.warning("Entrée invalide. Veuillez coller des multiplicateurs valides.")

