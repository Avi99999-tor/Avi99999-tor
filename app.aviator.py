import streamlit as st import numpy as np import pandas as pd import random

--- Login Page ---

def login_page(): st.title("Prediction Expert by Mickael") username = st.text_input("Nom d'utilisateur") password = st.text_input("Mot de passe", type="password") if st.button("Se connecter"): if username == "Topexacte" and password == "5312288612bet261": st.session_state["logged_in"] = True else: st.error("Nom d'utilisateur ou mot de passe incorrect")

--- Strategies ---

def mod10_seed_pattern(values): mods = [int(str(v).split(".")[-1][:2]) % 10 for v in values] return mods

def rolling_stats(values): window = 5 roll_avg = pd.Series(values).rolling(window).mean().tolist() roll_std = pd.Series(values).rolling(window).std().tolist() return roll_avg, roll_std

def seed_tracking_pattern(values): seeds = [(int(str(v).split(".")[-1][:2]) + i) % 100 for i, v in enumerate(values)] return seeds

def pattern_clustering(values): clusters = [] for v in values: if v < 1.5: clusters.append("Low") elif v < 5: clusters.append("Mid") else: clusters.append("High") return clusters

def reverse_entropy_approx(values): diffs = [abs(values[i] - values[i-1]) for i in range(1, len(values))] mean_diff = np.mean(diffs) if diffs else 1.0 return round(1 / mean_diff, 2)

def prediction_expert(values): predictions = [] mods = mod10_seed_pattern(values) roll_avg, roll_std = rolling_stats(values) seeds = seed_tracking_pattern(values) clusters = pattern_clustering(values) entropy = reverse_entropy_approx(values) for i in range(len(values), len(values)+20): mod = mods[-1] if mods else 0 avg = roll_avg[-1] if roll_avg[-1] else 2 std = roll_std[-1] if roll_std[-1] else 0.5 seed_influence = seeds[-1] / 100 if seeds else 0.2 cluster_weight = 1.2 if clusters and clusters[-1] == "Low" else 1.0 rand_shift = random.uniform(-0.2, 0.2) pred = round((avg + std + mod * 0.05 + seed_influence + entropy * 0.3) * cluster_weight + rand_shift, 2) pred = min(max(pred, 1.01), 10.0) fiab = random.randint(70, 95) predictions.append((f"T{i+1}", f"{pred}x", f"Fiabilité: {fiab}%")) mods.append(mod) return predictions

--- Prediction Page ---

def prediction_page(): st.title("Prediction Expert - Aviator")

st.subheader("Admin: Mickael")
st.text("Contact: 033 31 744 68")

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

