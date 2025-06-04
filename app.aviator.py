import streamlit as st
import numpy as np
import random
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import math

# --- Configuration ---
st.set_page_config(page_title="🎯 Hybride Prediction Aviator by Mickael", layout="centered")
st.title("🇲🇬 🎯 Hybride Prediction Aviator by Mickael")

st.subheader("🤖 Stratégie Hybride : AI & Mode Expert")

# --- Fidirana angona ---
multiplicateurs_input = st.text_area("📥 Ampidiro ny historique (ex: 1.21x 1.33x 12.66x ...)", 
                                     placeholder="1.21x 1.33x 12.66x 1.44x ...", height=150)

dernier_tour = st.number_input("🔢 Numéro du dernier tour (correspondant au 1er multiplicateur)", min_value=1, value=123)
heure_input = st.text_input("🕒 Heure du dernier tour (hh:mm:ss)", value="12:31:02")

mode_expert = st.checkbox("🧠 Activer le mode Expert")

calculer = st.button("🔮 Lancer la prédiction Hybride (T+1 à T+20)")

# --- Nettoyage des données ---
def extraire_valeurs(texte):
    valeurs = texte.replace(',', '.').lower().replace('x', '').split()
    propres = []
    for v in valeurs:
        try:
            val = float(v)
            if val > 0:
                propres.append(val)
        except ValueError:
            continue
    return propres

# --- Calcul durée basée sur multiplicateur ---
def calculer_duree(m):
    if 1.00 <= m < 2.00:
        d = (m * 13) / 1.33
    elif 2.00 <= m < 3.00:
        d = (m * 20) / 2.29
    elif 3.00 <= m < 4.00:
        d = (m * 23) / 3.12
    elif 4.00 <= m < 5.00:
        d = (m * 27) / 4.27
    elif 5.00 <= m <= 8.00:
        d = (m * 28) / 5.01
    elif 9.00 <= m <= 20.00:
        d = (m * 39) / 11.87
    else:
        d = 15
    return int(d) if d % 1 < 0.8 else int(d) + 1

# --- Fiabilité ---
def fiabilite(val, expert=False):
    if expert:
        if val >= 5:
            return round(random.uniform(92, 98), 2)
        elif val >= 3:
            return round(random.uniform(85, 92), 2)
        else:
            return round(random.uniform(80, 90), 2)
    else:
        if val >= 5:
            return round(random.uniform(85, 95), 2)
        elif val >= 3:
            return round(random.uniform(75, 85), 2)
        elif val <= 1.20:
            return round(random.uniform(60, 70), 2)
        else:
            return round(random.uniform(70, 80), 2)

# --- Mode Expert spécial prédiction ---
def prediction_expert(i, mod_score, rolling_mean):
    base = (mod_score * i + rolling_mean) / (i % 5 + 1)
    fluct = np.sin(i) + np.cos(mod_score)
    return round(abs(base + fluct + random.uniform(0.1, 0.5)), 2)

# --- Algorithme prédiction ---
def prediction_hybride(multiplicateurs, base_tour, heure_str, mode_expert=False):
    resultats = []
    rolling_mean = np.mean(multiplicateurs)
    mod_score = sum([int(str(x).split(".")[-1]) % 10 for x in multiplicateurs]) / len(multiplicateurs)

    # Heure de départ (dernier tour)
    heure_depart = datetime.strptime(heure_str, "%H:%M:%S")
    m_depart = multiplicateurs[0]
    heure_courante = heure_depart + timedelta(seconds=calculer_duree(m_depart))

    for i in range(1, 21):
        if mode_expert:
            pred = prediction_expert(i, mod_score, rolling_mean)
        else:
            seed = int((mod_score + rolling_mean + i * 3.73) * 1000) % 47
            pred = round(abs((np.sin(seed) + np.cos(i * mod_score)) * 2.5 + random.uniform(0.3, 1.2)), 2)

        if pred < 1.10:
            pred = round(1.10 + random.uniform(0.1, 0.3), 2)
        elif pred > 15:
            pred = round(6.2 + random.uniform(0.5, 1.5), 2)

        duree = calculer_duree(pred)
        fiab = fiabilite(pred, expert=mode_expert)
        resultats.append((base_tour + i, pred, heure_courante.strftime("%H:%M:%S"), fiab))
        heure_courante += timedelta(seconds=duree)

    return resultats

# --- Execution ---
if calculer:
    historique = extraire_valeurs(multiplicateurs_input)
    if len(historique) < 5:
        st.warning("⚠️ Ampidiro farafahakeliny 5 multiplicateurs.")
    else:
        resultats = prediction_hybride(historique, int(dernier_tour), heure_input, mode_expert)
        st.success("✅ Résultat Hybride T+1 à T+20")
        for t, m, h, f in resultats:
            label = "🌟" if mode_expert and m >= 5 else ""
            st.markdown(f"**T{t}** ➤ **{m}x** — 🕓 {h} — 🎯 Fiabilité: **{f}%** {label}")
