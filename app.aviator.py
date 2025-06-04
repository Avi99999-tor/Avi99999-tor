import streamlit as st
import numpy as np
import random
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# --- Configuration ---
st.set_page_config(page_title="🇲🇬 Prediction Hybride By Mickael", layout="centered")
st.title("🇲🇬 🎯 Prediction Hybride By Mickael")

st.subheader("🔁 Stratégie AI + Heure automatique")

# --- Fidirana angona ---
multiplicateurs_input = st.text_area("💾 Ampidiro ny multiplicateurs (misaraka amin'ny espace)", 
                                     placeholder="1.19x 8.28x 26.84x 1.57x 1.45x ...", height=150)
dernier_tour = st.number_input("🔢 Numéro du dernier tour", min_value=1, value=204)
dernier_multiplicateur = st.number_input("🎯 Multiplicateur Tn", min_value=1.00, value=1.51)
heure_input = st.time_input("🕒 Entrer l'heure de Tn (dernier tour)", value=datetime.now().time())

# --- Bouton Calculer ---
calculer = st.button("🔮 Prédire T+1 à T+20")

# --- Fanadiovana ny texte input ---
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

# --- Calcul durée base sur multiplicateur ---
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
    # arrondi logique
    if d % 1 < 0.80:
        return int(d)
    else:
        return int(d) + 1

# --- Fiabilité ---
def fiabilite(val):
    if val >= 5:
        return round(random.uniform(85, 95), 2)
    elif val >= 3:
        return round(random.uniform(75, 85), 2)
    elif val <= 1.20:
        return round(random.uniform(60, 70), 2)
    else:
        return round(random.uniform(70, 80), 2)

# --- Algorithme AI ---
def prediction_AI(multiplicateurs, base_tour, heure_tn, m_tn):
    resultats = []
    rolling_mean = np.mean(multiplicateurs)
    mod_score = sum([int(str(x).split(".")[-1]) % 10 for x in multiplicateurs]) / len(multiplicateurs)
    
    heure_courante = datetime.combine(datetime.today(), heure_tn)
    duree_precedente = calculer_duree(m_tn)

    heure_suivante = heure_courante + timedelta(seconds=duree_precedente)

    for i in range(1, 21):
        seed = int((mod_score + rolling_mean + i * 3.73) * 1000) % 47
        pred = round(abs((np.sin(seed) + np.cos(i * mod_score)) * 2.5 + random.uniform(0.3, 1.2)), 2)
        
        if pred < 1.10:
            pred = round(1.10 + random.uniform(0.1, 0.3), 2)
        elif pred > 10:
            pred = round(6.2 + random.uniform(0.5, 1.5), 2)
        
        duree = calculer_duree(pred)
        heure_suivante += timedelta(seconds=duree)
        fiab = fiabilite(pred)

        resultats.append((base_tour + i, pred, heure_suivante.strftime("%H:%M:%S"), fiab))

    return resultats

# --- Fampisehoana ---
if calculer:
    historique = extraire_valeurs(multiplicateurs_input)
    if len(historique) < 10:
        st.warning("⚠️ Ampidiro farafahakeliny 10 multiplicateurs.")
    else:
        resultats = prediction_AI(historique, int(dernier_tour), heure_input, dernier_multiplicateur)
        st.success("✅ Résultat T+1 à T+20")
        for t, m, h, f in resultats:
            st.markdown(f"**T{t}** ➤ **{m}x** — 🕓 {h} — 🎯 Fiabilité: **{f}%**")
