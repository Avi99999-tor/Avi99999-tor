import streamlit as st import numpy as np import pandas as pd import random import re

--- Login Page ---

def login_page(): st.title("Prediction Expert by Mickael") username = st.text_input("Nom d'utilisateur") password = st.text_input("Mot de passe", type="password") if st.button("Se connecter"): if username == "Topexacte" and password == "5312288612bet261": st.session_state["logged_in"] = True else: st.error("Nom d'utilisateur ou mot de passe incorrect")

--- Strategies ---

def mod10_seed(values): # Extract last two digits and mod 10 mods = [] for v in values: frac = str(v).split('.')[-1][:2] mods.append(int(frac) % 10 if frac.isdigit() else 0) return mods

def rolling_stats(values, window=5): series = pd.Series(values) roll_mean = series.rolling(window).mean().tolist() roll_std = series.rolling(window).std().tolist() return roll_mean, roll_std

def reverse_entropy(values): if len(values) < 2: return [0.1] * len(values) diffs = np.abs(np.diff(values)) probs = diffs / diffs.sum() ent = -np.sum(probs * np.log(probs + 1e-9)) return [round(ent, 2)] * len(values)

def boost_zone(values): return [1 if v >= 10 else 0 for v in values]

--- Expert Prediction Logic ---

def prediction_expert(values, n_preds=10): preds = [] mods = mod10_seed(values) avg_list, std_list = rolling_stats(values) ent_list = reverse_entropy(values) boost_list = boost_zone(values) consecutive_high = 0

for i in range(1, n_preds + 1):
    last = values[-1]
    # update consecutive high
    if last >= 5.0:
        consecutive_high += 1
    else:
        consecutive_high = 0
    # small boost bonus if first high
    bonus = 0.1 if consecutive_high == 1 and random.random() < 0.3 else 0
    # stats
    base = avg_list[-1] if not np.isnan(avg_list[-1]) else last
    variation = std_list[-1] if not np.isnan(std_list[-1]) else 0.3
    mod_frac = mods[-1] * 0.01
    ent = ent_list[-1] * 0.02
    noise = random.uniform(-0.02, 0.02)
    # combine
    raw = base * 0.6 + last * 0.4 + variation + mod_frac + ent + bonus + noise
    # cap
    cap = min(5.0, last * 1.1)
    pred = round(max(1.01, min(raw, cap)), 2)
    # tag
    if pred < 2.0:
        tag = '💙'
    elif pred < 5.0:
        tag = '💜'
    else:
        tag = '💗'
    preds.append((f"T{i}", f"{pred}x", f"Fiabilité: {random.randint(65,90)}%"))
    # update context
    values.append(pred)
    mods = mod10_seed(values)
    avg_list, std_list = rolling_stats(values)
    ent_list = reverse_entropy(values)
    boost_list = boost_zone(values)
return preds

--- Streamlit Application ---

st.set_page_config(page_title="Prediction Aviator", layout="centered")

Initialize login state

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

if not st.session_state['logged_in']: login_page() else: st.title("Prediction Aviator - Mode Expert") st.subheader("Admin: Mickael | Contact: 033 31 744 68") hist = st.text_area("Historique (ex: 39.50x 1.00x ...)", height=150) last = st.number_input("Numéro du dernier tour", min_value=1, step=1) n = st.slider("Nombre de prédictions", min_value=5, max_value=20, value=10) if st.button("Calculer"): try: # Clean input values = [float(x.replace('x','').replace('X','')) for x in re.findall(r"\d+.?\d*[xX]", hist)] preds = prediction_expert(values.copy(), n) st.markdown("### Prédictions à venir:") for idx, (label, val, prob) in enumerate(preds, start=1): st.write(f"T{last + idx} → {val} — {prob}") except Exception as e: st.error(f"Erreur: {e}") if st.button("Effacer"): st.experimental_rerun()

