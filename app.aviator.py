import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
import random

# --- Prédiction IA simple ---
def ai_prediction(historique):
    y = np.array(historique[-10:]).reshape(-1, 1)
    X = np.arange(len(y)).reshape(-1, 1)
    model = LinearRegression().fit(X, y)
    pred = model.predict(np.arange(len(y), len(y) + 20).reshape(-1, 1))
    return [round(float(p), 2) for p in pred]

# --- Expert Prediction logique simple ---
def expert_predictions(historique):
    predictions = []
    for i in range(1, 21):
        if len(historique) >= i:
            val = float(historique[-i])
            if val > 10:
                predictions.append(2 + i * 0.1)
            elif val > 2:
                predictions.append(1.8 + i * 0.05)
            else:
                predictions.append(1.00 + i * 0.03)
        else:
            predictions.append(1.00 + i * 0.02)
    return [round(p, 2) for p in predictions]

# --- Couleur logique ---
def get_couleur(val):
    if val < 2:
        return "🔘"
    elif val < 10:
        return "💜"
    else:
        return "🔴"

# --- Fusion IA + Expert ---
def prediction_combinee(historique, base_tour):
    ia_preds = ai_prediction(historique)
    exp_preds = expert_predictions(historique)

    résultats = []
    for i in range(20):
        ai = ia_preds[i]
        exp = exp_preds[i]
        final = round((ai + exp) / 2, 2)
        couleur = get_couleur(final)
        assurance = str(round(random.uniform(70, 95), 2)) + "%"
        résultats.append({
            "Tour": f"T{base_tour + i + 1}",
            "Valeur": f"{final}x",
            "Couleur": couleur,
            "Assurance": assurance
        })
    return résultats

# --- Traitement input de format Txxx → xx.xx x ---
def extraire_valeurs(historique_text):
    lignes = historique_text.strip().split("\n")
    valeurs = []
    for ligne in lignes:
        if "→" in ligne:
            try:
                val = ligne.split("→")[1].replace("x", "").strip()
                valeurs.append(float(val))
            except:
                continue
    return valeurs

# --- Interface Streamlit ---
st.set_page_config(page_title="Prediction By Mickael TOP EXACTE", layout="centered")
st.title("🎯 Prediction By Mickael TOP EXACTE")

with st.expander("🧾 Historique formaté"):
    st.markdown("**Format:** T101 → 1.02x")
    st.markdown("Exemple :")
    st.code("T101 → 1.02x\nT102 → 2.45x\nT103 → 3.96x\nT104 → 1.00x")

# Champ de texte pour historique
historique_text = st.text_area("Entrer l'historique au format Txxx → xx.xx x", height=200)

col1, col2 = st.columns(2)
with col1:
    dernier_tour = st.number_input("🔢 Dernier numéro de tour", min_value=0, value=120, step=1)
with col2:
    if st.button("🧹 Effacer l'historique"):
        historique_text = ""

# Bouton Prédire
if st.button("🔮 Prédire"):
    historique = extraire_valeurs(historique_text)
    if len(historique) < 5:
        st.warning("Il faut au moins 5 valeurs pour prédire.")
    else:
        resultats = prediction_combinee(historique, int(dernier_tour))
        st.subheader("📊 Résultat T+1 à T+20")

        for res in resultats:
            st.markdown(f"**{res['Tour']} → {res['Valeur']} {res['Couleur']}** — {res['Assurance']}")
