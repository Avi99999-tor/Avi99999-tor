import streamlit as st import numpy as np

--- Fonctions Stratégiques ---

def extract_mod10(val): try: last_digit = int(str(val).split('.')[-1][-1]) return last_digit % 10 except: return 0

def get_seed_pattern(values): return [round((float(str(v).split('.')[-1])/100), 2) for v in values]

def rolling_average(values, window=5): if len(values) < window: return np.mean(values) return np.mean(values[-window:])

def expert_prediction(history, start_tour): pred = [] seeds = get_seed_pattern(history[-10:]) mod10_vals = [extract_mod10(v) for v in history[-10:]] avg = rolling_average(history[-5:]) std = np.std(history[-5:])

for i in range(1, 11):
    fluct = np.sin(i + sum(mod10_vals[-3:])) + np.mean(seeds[-3:]) * 2
    result = round(avg + (fluct * std * 0.5), 2)
    result = max(1.01, result)
    fiability = 60 + min(40, abs(result - avg) * 10)
    tour_number = start_tour + i
    pred.append((f"T{tour_number}", result, round(min(99, fiability))))
return pred

--- Streamlit App ---

st.set_page_config(page_title="AVIATOR EXPERT PREDICTOR", layout="centered") st.title("AVIATOR PREDICTOR - MODE EXPERT")

with st.form("input_form"): input_data = st.text_area("Multiplicateurs (séparés par des espaces)", "") tour_recent = st.number_input("Numéro du tour le plus récent (ex: 130)", min_value=1, value=130) submitted = st.form_submit_button("Prédire")

if submitted: try: history = list(map(float, input_data.strip().split())) if len(history) >= 10: preds = expert_prediction(history, start_tour=tour_recent) st.subheader("Prédictions Expert") for t, val, f in preds: if f >= 60: color = "green" if f >= 80 else ("orange" if f >= 70 else "gray") st.markdown(f"{t} → {val}x — Fiabilité: :{color}[{f}%]") else: st.warning("Ampidiro multiplicateurs farafahakeliny 10.") except: st.error("Format diso. Azafady, ampiasao espace hanasarahana ny isa.")

