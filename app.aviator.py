import streamlit as st import numpy as np import pandas as pd import random import re

--- Login Page ---

def login_page(): st.title("Prediction Expert by Mickael") username = st.text_input("Nom d'utilisateur") password = st.text_input("Mot de passe", type="password") if st.button("Se connecter"): if username == "Topexacte" and password == "5312288612bet261": st.session_state["logged_in"] = True else: st.error("Nom d'utilisateur ou mot de passe incorrect")

--- Utility Functions ---

def mod10_seed_pattern(values): mods = [int(str(v).split(".")[-1][:2]) % 10 for v in values] return mods

def rolling_stats(values): window = 5 roll_avg = pd.Series(values).rolling(window).mean().tolist() roll_std = pd.Series(values).rolling(window).std().tolist() return roll_avg, roll_std

def logic_booster(i, mods): # Inject logic for 1.00 and x10+ every certain intervals if i % 7 == 0: return 1.00, 90 if i % 13 == 0: return round(random.uniform(8.0, 15.0), 2), 80 if mods and mods[-1] in [0, 1, 9]: return round(random.uniform(4.0, 6.0), 2), 75 return None, None

--- Prediction Strategy Logic ---

def prediction_expert(values): predictions = [] mods = mod10_seed_pattern(values) roll_avg, roll_std = rolling_stats(values) for i in range(20): logic_val, logic_fiab = logic_booster(i, mods) if logic_val is not None: pred = logic_val fiab = logic_fiab else: mod = mods[-1] if mods else 0 avg = roll_avg[-1] if roll_avg[-1] else 2.0 std = roll_std[-1] if roll_std[-1] else 0.8 rand_shift = random.uniform(-1.0, 1.5) pred = round(avg + std + mod * 0.08 + rand_shift, 2) pred = min(max(pred, 1.00), 15.0) fiab = random.randint(65, 95) predictions.append((f"T{i+1}", f"{pred}x", f"Fiabilité: {fiab}%")) mods.append(mods[-1]) return predictions

--- Prediction Page ---

def prediction_page(): st.title("Prediction Expert - Aviator") st.subheader("Admin: Mickael") st.text("Contact: 033 31 744 68")

tour_input = st.text_area("Historique des multiplicateurs (séparés par 'x')",
    placeholder="Exemple: 1.33x 2.74x 1.46x 72.61x 3.55x ...")
tour_num = st.number_input("Numéro du tour le plus récent (ex: 133)", min_value=1, step=1)

if st.button("Calculer"):
    try:
        cleaned = [float(x.replace("x", "")) for x in tour_input.split() if "x" in x]
        predictions = prediction_expert(cleaned)
        for i, (label, val, prob) in enumerate(predictions):
            tour = tour_num + i + 1
            st.markdown(f"**T{tour}** → {val} — {prob}")
    except:
        st.error("Erreur lors de l'analyse. Vérifiez l'entrée.")

--- Main App ---

if "logged_in" not in st.session_state: st.session_state["logged_in"] = False

if not st.session_state["logged_in"]: login_page() else: prediction_page()

