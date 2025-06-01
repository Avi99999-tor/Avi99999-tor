import streamlit as st
import numpy as np
import random

# --- Configuration ---
st.set_page_config(page_title="🇲🇬 Prediction By Mickael", layout="centered")
st.title("🇲🇬 🎯 Prediction Expert By Mickael")

st.subheader("Version manaraka statistika Aviator")

# --- Fidirana data (multiplicateurs) ---
multiplicateurs_input = st.text_area("💾 Ampidiro ny multiplicateurs (misaraka amin'ny espace)", 
                                     placeholder="1.19x 8.28x 26.84x 1.57x 1.45x ...", height=150)

dernier_tour = st.number_input("🔢 Numéro du dernier tour", min_value=1, value=50)

# --- Fanadiovana angona ---
def extraire_valeurs(texte):
    valeurs = texte.replace(',', '.').lower().replace('x', '').split()
    return [float(v) for v in valeurs if float(v) > 0]

# --- Fiabilité calculation ---
def fiabilite(val):
    if val >= 5:
        return round(random.uniform(85, 95), 2)
    elif val >= 3:
        return round(random.uniform(75, 85), 2)
    elif val <= 1.20:
        return round(random.uniform(60, 70), 2)
    else:
        return round(random.uniform(70, 80), 2)

# --- Analiza Mod Seed ---
def analyse_mod_seed(liste):
    chiffres_mod = [int(str(x).split(".")[-1]) % 10 for x in liste]
    return sum(chiffres_mod) / len(chiffres_mod)

# --- Prediction Expert ---
def prediction_expert(multiplicateurs, base_tour):
    résultats = []
    rolling_mean = np.mean(multiplicateurs)
    mod_score = analyse_mod_seed(multiplicateurs)

    for i in range(1, 21):  # T+1 à T+20
        seed = int((mod_score + rolling_mean + i * 3.73) * 1000) % 57
        pred = round(abs((np.sin(seed) + np.cos(i * mod_score)) * 3.5 + random.uniform(0.3, 1.7)), 2)

        # Fanitsiana ho ara-statistikan'ny Aviator
        if pred < 1.10:
            pred = round(1.10 + random.uniform(0.1, 0.3), 2)
        elif pred > 10:
            pred = round(6.5 + random.uniform(0.5, 1.5), 2)

        fiab = fiabilite(pred)
        label = "Assuré" if fiab >= 80 else ("Crash probable" if pred <= 1.20 else "")

        résultats.append((base_tour + i, pred, fiab, label))
    
    return résultats

# --- Fanodinana ---
if multiplicateurs_input:
    historique = extraire_valeurs(multiplicateurs_input)

    if len(historique) < 10:
        st.warning("❗ Tokony hampiditra farafahakeliny 10 multiplicateurs.")
    else:
        résultats = prediction_expert(historique, int(dernier_tour))
        st.markdown("### 📊 Résultat T+1 à T+20 :")

        for tour, val, pourcent, label in résultats:
            line = f"**T{tour}** → **{val}x** — Fiabilité: **{pourcent}%**"
            if label:
                line += f" **({label})**"
            st.markdown("- " + line)
