import streamlit as st import numpy as np import pandas as pd import random import re

--- Login Page ---

def login_page(): st.title("Prediction Expert by Mickael") username = st.text_input("Nom d'utilisateur") password = st.text_input("Mot de passe", type="password") if st.button("Se connecter"): if username == "Topexacte" and password == "5312288612bet261": st.session_state["logged_in"] = True else: st.error("Nom d'utilisateur ou mot de passe incorrect")

--- Strategies ---

def mod10_seed_pattern(values): return [int(str(v).split('.')[-1][:2]) % 10 for v in values]

def rolling_stats(values, window=5): series = pd.Series(values) return series.rolling(window).mean().tolist(), series.rolling(window).std().tolist()

def seed_tracking_pattern(values): return [(int(str(v).split('.')[-1][:2]) + idx) % 100 for idx, v in enumerate(values)]

def pattern_clustering(values): clusters = [] for v in values: if v < 1.5: clusters.append('Low') elif v < 5: clusters.append('Mid') else: clusters.append('High') return clusters

def reverse_entropy_approx(values): if len(values) < 2: return 0.0 diffs = np.abs(np.diff(values)) probs = diffs / diffs.sum() entropy = -np.sum(probs * np.log(probs + 1e-9)) return round(entropy, 2)

--- Expert Prediction Logic ---

def prediction_expert(values, n_preds=10): mods = mod10_seed_pattern(values) avg_roll, std_roll = rolling_stats(values) seeds = seed_tracking_pattern(values) clusters = pattern_clustering(values) entropy = reverse_entropy_approx(values)

preds = []
consecutive_high = 0
for i in range(n_preds):
    last = values[-1]
    # boost detection
    if last >= 5.0:
        consecutive_high += 1
    else:
        consecutive_high = 0
    boost_bonus = 0.2 if (consecutive_high == 1) else 0.0
    # base stats
    avg = avg_roll[-1] if not np.isnan(avg_roll[-1]) else 2.0
    std = std_roll[-1] if not np.isnan(std_roll[-1]) else 0.5
    mod_frac = (mods[-1] if mods else 0) / 200.0
    seed_inf = seeds[-1] / 100.0
    cluster_weight = 1.2 if clusters[-1] == 'Low' else 1.0
    noise = random.uniform(-0.05, 0.05)
    raw = (avg + std + mod_frac + seed_inf + entropy * 0.1) * cluster_weight + boost_bonus + noise
    # dynamic cap
    if consecutive_high == 1:
        cap = min(4.0, last * 1.1)
    else:
        cap = min(3.0, last * 1.2)
    pred = round(max(1.0, min(raw, cap)), 2)
    tag = '💙' if pred < 2.0 else ('💜' if pred < 5.0 else '💗')
    preds.append((pred, tag))
    values.append(pred)
    mods.append(mods[-1] if mods else 0)
    avg_roll, std_roll = rolling_stats(values)
    seeds = seed_tracking_pattern(values)
    clusters = pattern_clustering(values)
    entropy = reverse_entropy_approx(values)
return preds

--- Streamlit Application ---

st.set_page_config(page_title="Prediction Aviator", layout="centered")

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

if not st.session_state['logged_in']: login_page() else: st.title("Prediction Aviator - Mode Expert") st.subheader("Admin: Mickael | Contact: 033 31 744 68") hist = st.text_area("Historique (ex: 1.33x 2.74x ...)", height=150) last = st.number_input("Numéro du dernier tour", min_value=1, step=1) n = st.slider("Nombre de prédictions", min_value=5, max_value=20, value=10) if st.button("Calculer"): try: values = [float(x.replace('x','').replace('X','')) for x in re.findall(r"\d+.?\d*[xX]", hist)] preds = prediction_expert(values.copy(), n_preds=n) st.markdown("### Prédictions à venir:") for idx, (pred, tag) in enumerate(preds, start=1): st.write(f"T{last+idx} → {tag} x{pred}") except Exception as e: st.error(f"Erreur: {e}") if st.button("Effacer"): st.experimental_rerun()

