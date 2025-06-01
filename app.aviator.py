import streamlit as st
import numpy as np
import random
from sklearn.linear_model import LinearRegression

st.title("Prédiction Expert by Mickael")
st.subheader("Version combinée: mod 10 + seed + logique expert + IA simple")

# Entrée utilisateur
multiplicateurs_input = st.text_area("**Entrez les multiplicateurs (du plus récent au plus ancien)**", 
                                     placeholder="Ex: 2.14x 1.26x 5.87x ...")

dernier_tour = st.number_input("**Numéro du dernier tour (ex: 74 si 2.14x est le plus récent)**", min_value=1, value=50)

if 'multiplicateurs_historique' not in st.session_state:
    st.session_state.multiplicateurs_historique = ""

col1, col2 = st.columns(2)

with col1:
    calculer = st.button("✅ Calculer")
with col2:
    if st.button("🧹 Effacer"):
        multiplicateurs_input = ""
        st.session_state.multiplicateurs_historique = ""


def nettoyer_donnees(texte):
    valeurs = texte.replace(',', '.').lower().replace('x', '').split()
    try:
        return [float(v) for v in valeurs if float(v) > 0]
    except:
        return []

def fiabilite(pred, expert_val):
    base = 70
    ecart = abs(pred - expert_val)
    if ecart <= 0.5:
        return 90 + random.randint(0, 5)
    elif ecart <= 1:
        return 80 + random.randint(0, 5)
    else:
        return base + random.randint(-5, 5)

def analyse_mod_seed(liste):
    chiffres_mod = [int(str(x).split(".")[-1]) % 10 for x in liste]
    moy_mod = sum(chiffres_mod) / len(chiffres_mod)
    return moy_mod

def prediction_expert(multiplicateurs, base_tour):
    résultats = []
    rolling_mean = np.mean(multiplicateurs)
    mod_score = analyse_mod_seed(multiplicateurs)

    for i in range(1, 21):  # T+1 à T+20
        seed = int((mod_score + rolling_mean + i * 3.73) * 1000) % 97
        pred = round(abs((np.sin(seed) + np.cos(i * mod_score)) * 3 + random.uniform(0.2, 1.5)), 2)

        if pred < 1.00:
            pred = round(0.99 + random.uniform(0.01, 0.2), 2)
        elif pred > 10:
            pred = round(6 + random.uniform(0.5, 2.5), 2)

        résultats.append(pred)
    return résultats

def prediction_ia_simple(multiplicateurs):
    X, y = [], []
    window = 3
    for i in range(len(multiplicateurs) - window):
        X.append(multiplicateurs[i:i+window])
        y.append(multiplicateurs[i+window])
    if len(X) < 5:
        return []  # tsy ampy fanofanana

    model = LinearRegression()
    model.fit(X, y)

    derniers = multiplicateurs[:3]
    résultats = []
    for _ in range(20):
        pred = model.predict([derniers])[0]
        pred = round(max(0.99, min(pred, 10)), 2)
        résultats.append(pred)
        derniers = derniers[1:] + [pred]
    return résultats

if calculer and multiplicateurs_input:
    historique = nettoyer_donnees(multiplicateurs_input)
    if len(historique) < 10:
        st.warning("Veuillez entrer au moins 10 multiplicateurs.")
    else:
        expert_preds = prediction_expert(historique, int(dernier_tour))
        ia_preds = prediction_ia_simple(historique[::-1])  # car on entre du plus récent au plus ancien

        st.markdown("### **Résultats combinés des prédictions (T+1 à T+20) :**")
        if not ia_preds:
            st.error("Pas assez de données pour entraîner le modèle IA (minimum: 15 valeurs)")
        else:
            for i in range(20):
                tour = int(dernier_tour) + i + 1
                pred_ia = ia_preds[i]
                pred_exp = expert_preds[i]
                fiab = fiabilite(pred_ia, pred_exp)
                label = "Assuré" if fiab >= 80 else "Crash probable" if pred_ia <= 1.20 else ""

                line = f"**T{tour}** → IA: **{pred_ia}x** | Expert: **{pred_exp}x** — Fiabilité: **{fiab}%**"
                if label:
                    line += f" **({label})**"
                st.markdown("- " + line)
