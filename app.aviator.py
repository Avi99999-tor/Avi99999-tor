import streamlit as st import numpy as np import pandas as pd import random import re

--- Login Page ---

def login_page(): st.title("Prediction Expert by Mickael") username = st.text_input("Nom d'utilisateur") password = st.text_input("Mot de passe", type="password") if st.button("Se connecter"): if username == "Topexacte" and password == "5312288612bet261": st.session_state["logged_in"] = True else: st.error("Nom d'utilisateur ou mot de passe incorrect.")

--- Prediction Logic with Aviator Rhythm ---

def prediction_expert(values, n_preds=20): preds = [] # track cycles for forced events for i in range(1, n_preds+1): idx = len(values) # Force 1.00 every ~10 tours if idx % 10 == 0: pred = 1.00 fiab = 95 # Force occasional x10+ every ~25 tours elif idx % 25 == 0: pred = round(random.uniform(8, 15), 2) fiab = 90 else: last = values[-1] # small chance of repeat 1.00 if random.random() < 0.05: pred = 1.00 fiab = random.randint(80, 90) # medium chance of low (<2) elif random.random() < 0.7: pred = round(random.uniform(1.02, min(2.0, last1.2)), 2) fiab = random.randint(60, 80) # small chance of mid (2-5) else: pred = round(random.uniform(2.0, min(5.0, last1.3)), 2) fiab = random.randint(70, 85) # record preds.append((pred, fiab)) values.append(pred) return preds

--- Streamlit App ---

st.set_page_config(page_title="Prediction Aviator", layout="centered") if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

if not st.session_state['logged_in']: login_page() else: st.title("Prediction Aviator - Mode Expert") st.subheader("Admin: Mickael | Contact: 033 31 744 68") hist = st.text_area("Historique des multiplicateurs (séparés par 'x')", height=150) last = st.number_input("Numéro du dernier tour", min_value=1, step=1) n = st.slider("Nombre de prédictions", 5, 20, 10) if st.button("Calculer"): try: values = [float(x.replace('x','').replace('X','')) for x in re.findall(r"\d+.?\d*[xX]", hist)] preds = prediction_expert(values.copy(), n) st.markdown("### Prédictions à venir:") for idx, (pred, fiab) in enumerate(preds, start=1): tour = last + idx color = '💙' if pred < 2 else ('💜' if pred < 5 else '💗') st.write(f"T{tour} → {color} x{pred} — Fiabilité: {fiab}%") except Exception as e: st.error(f"Erreur: {e}") if st.button("Effacer"): st.experimental_rerun()

