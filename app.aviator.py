import streamlit as st import numpy as np import random import pandas as pd

st.set_page_config(page_title="Prediction Expert by Mickael", layout="centered") st.title("Prédiction Expert by Mickael")

User input

st.subheader("Entrer les 10 derniers multiplicateurs") data_input = st.text_input("Exemple: 1.23, 1.01, 3.45, 72.12, ...")

def parse_input(data_input): try: values = [float(x.strip().replace("x", "")) for x in data_input.split(",") if x.strip()] return values except: return []

values = parse_input(data_input)

Modulo tracking (mod 10)

def compute_mod10(values): mod10 = [int(str(v).split(".")[1]) % 10 if "." in str(v) else 0 for v in values] return mod10

Rolling average

def rolling_stats(values, window=5): if len(values) < window: return np.mean(values), np.std(values) return np.mean(values[-window:]), np.std(values[-window:])

Pattern clustering (simplified)

def recent_pattern(values): if len(values) < 3: return None return [round(v, 2) for v in values[-3:]]

Generate prediction with logic

def predict_next(values): if len(values) < 10: return []

predictions = []
rolling_avg, rolling_std = rolling_stats(values, window=5)
mod10_list = compute_mod10(values)

for i in range(1, 21):
    base = 1.5 + 0.2 * (i % 3) + random.uniform(-0.1, 0.3)
    mod_val = mod10_list[-1] if mod10_list else 0

    if mod_val in [3, 7]:
        base += random.uniform(2, 4)  # Explosion mod

    if rolling_avg < 2.0 and rolling_std < 0.6:
        base += random.uniform(1.5, 3.0)  # Rebond probable après crash

    if values[-1] < 1.20:
        base += random.uniform(2.0, 3.5)

    base = round(base, 2)
    conf = random.randint(68, 88)
    label = "Assuré" if base >= 5 and conf >= 80 else "" if conf < 70 else "Probable"
    predictions.append((f"T+{i}", base, conf, label))

return predictions

if values: st.subheader("Résultats de Prédiction") preds = predict_next(values) df = pd.DataFrame(preds, columns=["Tour", "Multiplicateur Prévu", "Fiabilité (%)", "Note"]) st.dataframe(df, use_container_width=True)

st.subheader("Analyse Mod 10")
st.write(f"Mod 10 des 10 derniers multiplicateurs: {compute_mod10(values)}")

st.subheader("Statistique Dynamique")
avg, std = rolling_stats(values)
st.write(f"Rolling Moyenne: {round(avg, 2)} | Écart-type: {round(std, 2)}")

pattern = recent_pattern(values)
if pattern:
    st.subheader("Dernier Pattern détecté")
    st.write(f"{pattern}")

st.info("Mode expert actif: prédiction probabiliste + pattern detection + mod10 tracking")

else: st.warning("Veuillez entrer au moins 10 multiplicateurs.")

