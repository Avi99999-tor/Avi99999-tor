import streamlit as st import numpy as np import pandas as pd import random import re

--- Login Page ---

def login_page(): st.title("Prediction Expert by Mickael") username = st.text_input("Nom d'utilisateur") password = st.text_input("Mot de passe", type="password") if st.button("Se connecter"): if username == "Topexacte" and password == "5312288612bet261": st.session_state["logged_in"] = True else: st.error("Nom d'utilisateur ou mot de passe incorrect")

--- Prediction Logic ---

def mod10_seed_pattern(values): return [int(str(v).split('.')[1][:2]) % 10 if '.' in str(v) else 0 for v in values]

def rolling_stats(values, window=5): s = pd.Series(values) return s.rolling(window).mean().tolist(), s.rolling(window).std().tolist()

def logic_booster(index, mods): # every 7th -> 1.00x, every 13th -> big boost, mod-based -> mid boost if index and index % 7 == 0: return 1.00, 90 if index and index % 13 == 0: return round(random.uniform(8.0, 15.0), 2), 80 if mods and mods[-1] in [0, 1, 9]: return round(random.uniform(4.0, 6.0), 2), 75 return None, None

--- Expert Prediction ---

def prediction_expert(values, n_preds): preds = [] mods = mod10_seed_pattern(values) roll_avg, roll_std = rolling_stats(values) for i in range(1, n_preds+1): logic_val, logic_fiab = logic_booster(i, mods) if logic_val is not None: pred, fiab = logic_val, logic_fiab else: avg = roll_avg[-1] or values[-1] std = roll_std[-1] or 0.5 mod = mods[-1] if mods else 0 noise = random.uniform(-0.5, 0.5) pred = round(avg + std * 0.3 + mod * 0.05 + noise, 2) pred = max(1.00, min(pred, 10.00)) fiab = random.randint(65, 90) preds.append((f"T{i}", f"{pred}x", f"Fiabilité: {fiab}%")) values.append(pred) mods = mod10_seed_pattern(values) roll_avg, roll_std = rolling_stats(values) return preds

--- Streamlit App ---

st.set_page_config(page_title="Prediction Aviator", layout="centered") if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False if not st.session_state['logged_in']: login_page() else: st.title("Prediction Aviator - Mode Expert") st.subheader("Admin: Mickael | Contact: 033 31 744 68") hist = st.text_area("Historique (ex: 39.50x 1.00x ...)", height=150) last = st.number_input("Numéro du dernier tour", min_value=1, step=1) n = st.slider("Nombre de prédictions", min_value=5, max_value=20, value=10) if st.button("Calculer"): try: values = [float(x.replace('x','').replace('X','').replace(',','.')) for x in re.findall(r"\d+.?\d*[xX]", hist)] preds = prediction_expert(values.copy(), n) st.markdown("### Prédictions à venir:") for idx, (label, val, prob) in enumerate(preds): tour = last + idx + 1 st.write(f"T{tour} → {val} — {prob}") except Exception as e: st.error(f"Erreur: {e}") if st.button("Effacer"): st.experimental_rerun()

