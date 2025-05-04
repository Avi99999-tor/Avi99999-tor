import streamlit as st import numpy as np import pandas as pd import random import re

def login_page(): st.title("Prediction Expert by Mickael") username = st.text_input("Nom d'utilisateur") password = st.text_input("Mot de passe", type="password") if st.button("Se connecter"]): if username == "Topexacte" and password == "5312288612bet261": st.session_state["logged_in"] = True else: st.error("Nom d'utilisateur ou mot de passe incorrect.")

--- Core Prediction Logic ---

def expert_predict(history, last_tour, n_preds=10): vals = [float(x.replace('x','').replace('X','')) for x in re.findall(r"\d+.?\d*[xX]", history)] preds, consecutive_high = [], 0 for i in range(1, n_preds+1): recent = vals[-3:] last = recent[-1] # dynamic cap less boosts in a row boost_flag = last >= 5.0 if boost_flag: consecutive_high += 1 else: consecutive_high = 0 # prevent too many boosts boost_bonus = 0.2 if boost_flag and consecutive_high <= 1 else 0 # mod10 tweak mod_vals = [int(str(v).split('.')[-1])%10 for v in recent] mod_frac = (sum(mod_vals)%10)/200 noise = random.uniform(-0.05,0.05) raw = last + mod_frac + noise + boost_bonus cap = min(3.0, last1.2) if not boost_flag else min(4.0, last1.1) pred = round(max(1.0, min(raw, cap)),2) # tag tag = "💙" if pred<2 else ("💜" if pred<5 else "💗") preds.append((f"T{last_tour+i}",pred,tag)) vals.append(pred) return preds

--- Streamlit UI ---

st.set_page_config(page_title="Prediction Aviator",layout="centered") if "logged_in" not in st.session_state: st.session_state["logged_in"] = False if not st.session_state["logged_in"]: login_page() else: st.title("Prediction Aviator - Mode Expert") st.text("Admin: Mickael | Contact: 033 31 744 68") hist = st.text_area("Historique (ex: 39.50x 1.00x ...)", height=150) last = st.number_input("Numéro du dernier tour",min_value=1,step=1) n = st.slider("Nombre de prédictions",5,20,10) if st.button("Calculer"): try: preds = expert_predict(hist,last,n) st.markdown("### Prédictions:") for tour,val,tag in preds: st.write(f"{tour} → {tag} x{val}") except Exception as e: st.error(f"Erreur: {e}") if st.button("Effacer"): st.experimental_rerun()

