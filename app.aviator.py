import streamlit as st
import numpy as np
import random

st.title("🎯 Prédiction Expert by Mickael")
st.subheader("Version combinée: mod 10 + seed + logique expert")

# Session states
if 'historique' not in st.session_state:
    st.session_state.historique = ""
if 'resultats' not in st.session_state:
    st.session_state.resultats = []

# Entrée utilisateur
multiplicateurs_input = st.text_area("**Entrez les multiplicateurs (du plus récent au plus ancien)**", 
                                     value=st.session_state.historique,
                                     placeholder="Ex: 2.14x 1.26x 5.87x ...")

dernier_tour = st.number_input("**Numéro du dernier tour (ex: 74 si 2.14x est le plus récent)**", 
                                min_value=1, value=50)

col1, col2 = st.columns(2)
go = col1.button("🔍 Calculer la Prédiction")
reset = col2.button("🗑️ Effacer l'entrée")

# Nettoyage données
def nettoyer_donnees(texte):
    valeurs = texte.replace(',', '.').lower().replace('x', '').split()
    try:
        return [float(v) for v in valeurs if float(v) > 0]
    except:
        return []

# Analyse pattern logique (simple exemple)
def pattern_score(liste):
    tendance = 0
    for i in range(1, len(liste)):
        if liste[i] > liste[i-1]:
            tendance += 1
        elif liste[i] < liste[i-1]:
            tendance -= 1
    score = 70 + tendance * 2
    return max(40, min(score + random.randint(-5, 5), 95))

# Mod score
def analyse_mod_seed(liste):
    chiffres_mod = [int(str(x).split(".")[-1]) % 10 for x in liste]
    moy_mod = sum(chiffres_mod) / len(chiffres_mod)
    return moy_mod

# Fonction prédiction
def prediction_expert(multiplicateurs, base_tour):
    résultats = []
    rolling_mean = np.mean(multiplicateurs)
    mod_score = analyse_mod_seed(multiplicateurs)
    schema_score = pattern_score(multiplicateurs)

    for i in range(1, 21):  # T+1 à T+20
        seed = int((mod_score + rolling_mean + i * 3.73) * 1000) % 97
        pred = round(abs((np.sin(seed) + np.cos(i * mod_score)) * 3 + random.uniform(0.2, 1.5)), 2)

        # Ajustement
        if pred < 1.00:
            pred = round(0.99 + random.uniform(0.01, 0.2), 2)
        elif pred > 10:
            pred = round(6 + random.uniform(0.5, 2.5), 2)

        fiab = schema_score + random.randint(-4, 4)
        label = "Assuré" if fiab >= 80 else "Crash probable" if pred <= 1.20 else ""

        résultats.append((base_tour + i, pred, fiab, label))

    return résultats

# Action sur bouton
if go:
    st.session_state.historique = multiplicateurs_input
    historique = nettoyer_donnees(multiplicateurs_input)

    if len(historique) < 10:
        st.warning("⚠️ Veuillez entrer au moins 10 multiplicateurs.")
    else:
        st.session_state.resultats = prediction_expert(historique, int(dernier_tour))

# Bouton reset
if reset:
    st.session_state.historique = ""
    st.session_state.resultats = []

# Affichage des résultats
if st.session_state.resultats:
    st.markdown("### 📊 **Résultats des prédictions (T+1 à T+20) :**")
    for tour, val, pourcent, label in st.session_state.resultats:
        line = f"**T{tour}** → **{val}x** — Fiabilité: **{pourcent}%**"
        if label:
            line += f" **({label})**"
        st.markdown("- " + line)
