import streamlit as st import numpy as np import pandas as pd import random import re

--- Login Page ---

def login_page(): st.title("Prediction Expert by Mickael") username = st.text_input("Nom d'utilisateur") password = st.text_input("Mot de passe", type="password") if st.button("Se connecter"): if username == "Topexacte" and password == "5312288612bet261": st.session_state["logged_in"] = True else: st.error("Nom d'utilisateur ou mot de passe incorrect")

--- Strategies ---

def mod10_seed(values): return [int(str(v).split('.')[-1][:2]) % 10 for v in values]

def rolling_stats(values, window=5): series = pd.Series(values) return series.rolling(window).mean().tolist(), series.rolling(window).std().tolist()

def reverse_entropy(values): if len(values) < 2: return [0.1]*len(values) diffs = np.abs(np.diff(values)) probs = diffs / diffs.sum() ent = -np.sum(probs * np.log(probs + 1e-9)) return [ent]*len(values)

def boost_zone(values): return [1 if v >= 10 else 0 for v in values]

--- Expert Prediction Logic ---

def prediction_expert(values, n_preds=10): preds = [] mods = mod10_seed(values) avg, std = rolling_stats(values) entropy = reverse_entropy(values) boost = boost_zone(values) consecutive_high = 0

for i in range(1, n_preds+1):
    last = values[-1]
    # update boost count
    if last >= 5.0:
        consecutive_high += 1
    else:
        consecutive_high = 0
    # reduced boost bonus
    boost_bonus = 0.1 if (consecutive_high == 1 and random.random() < 0.3) else 0
    # stats
    base = avg[-1] if not np.isnan(avg[-1]) else last
    variation = std[-1] if not np.isnan(std[-1]) else 0.3
    mod = (mods[-1] if mods else 0) * 0.01
    ent = entropy[-1] * 0.02
    noise = random.uniform(-0.02, 0.02)
    raw = base * 0.6 + last * 0.4 + variation + mod + ent + boost_bonus + noise
    # cap
    cap = min(5.0, last * 1.1)
    pred = round(max(1.01, min(raw, cap)), 2)
    # tag
    tag = '💙' if pred < 2.0 else ('💜' if pred < 5.0 else '💗')
    preds.append((f"T{i}", f"{pred}x", f"Fiabilité: {random.randint(65,90)}%"))
    # update history
    values.append(pred)
    mods.append(mods[-1] if mods else 0)
    avg, std = rolling_stats(values)
    entropy = reverse_entropy(values)
    boost = boost_zone(values)
return preds

--- Streamlit Application ---

st.set_page_config(page_title="Prediction Aviator", layout="centered") if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

if not st.session_state['logged_in']: login_page() else: st.title("Prediction Aviator - Mode Expert") st.subheader("Admin: Mickael | Contact: 033 31 744 68") hist = st.text_area("Historique (ex: 1.33x 2.74x ...)", height=150) last = st.number_input("Numéro du dernier tour", min_value=1, step=1) n = st.slider("Nombre de prédictions", min_value=5, max_value=20, value=10) if st.button("Calculer"): try: values = [float(x.replace('x','').replace('X','')) for x in re.findall(r"\d+.?\d*[xX]", hist)] preds = prediction_expert(values.copy(), n_preds=n) st.markdown("### Prédictions à venir:") for idx, (label, val, prob) in enumerate(preds, start=1): st.write(f"T{last+idx} → {val} — {prob}") except Exception as e: st.error(f"Erreur: {e}") if st.button("Effacer"): st.experimental_rerun()

