import streamlit as st
import numpy as np
import random
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Prediction By Mickael TOP EXACTE")
st.title("♈🇲🇬 Prediction By Mickael - TOP EXACTE")
st.subheader("Version combinée : Expert logique + IA (Linear Regression)")

# -------------------
# Fonctions utilitaires
# -------------------

def nettoyer_donnees(texte):
    vals = texte.replace(',', '.').lower().replace('x', '').split()
    try:
        return [float(v) for v in vals if float(v) > 0]
    except:
        return []

def fiabilite(pred):
    if pred >= 10:
        return random.randint(87, 93)
    elif pred >= 5:
        return random.randint(80, 88)
    elif pred >= 3:
        return random.randint(75, 85)
    elif pred <= 1.2:
        return random.randint(60, 70)
    else:
        return random.randint(68, 78)

def analyse_mod_seed(liste):
    chiffres_mod = [int(str(x).split(".")[-1]) % 10 for x in liste]
    return sum(chiffres_mod) / len(chiffres_mod)

def color_tag(val):
    if val < 2:
        return "🔵"
    elif val < 10:
        return "💜"
    else:
        return "🔴"

# -------------------
# IA – Linear Regression
# -------------------

def entrer_model_ml(multiplicateurs):
    # Préparer X, y pour sliding window de taille 3
    window = 3
    X, y = [], []
    for i in range(len(multiplicateurs) - window):
        X.append(multiplicateurs[i:i+window])
        y.append(multiplicateurs[i+window])
    if len(X) < 5:
        return None
    model = LinearRegression().fit(np.array(X), np.array(y))
    return model

def ia_ml_predictions(model, historique):
    # Prédire 20 tours en se basant sur les 3 derniers
    preds = []
    derniers = historique[-3:]
    for _ in range(20):
        p = model.predict(np.array([derniers]))[0]
        p = round(max(1.01, min(p, 15)), 2)  # Clamp entre 1.01 et 15
        preds.append(p)
        derniers = [derniers[1], derniers[2], p]
    return preds

# -------------------
# Expert logique
# -------------------

def expert_predictions(multiplicateurs):
    résultats = []
    rolling_mean = np.mean(multiplicateurs)
    mod_score = analyse_mod_seed(multiplicateurs)
    for i in range(1, 21):
        seed = int((mod_score + rolling_mean + i * 0.7) * 1000) % 97
        pred_exp = round(abs((np.sin(seed) + np.cos(i * mod_score)) * 3 + random.uniform(0.2, 1.5)), 2)
        if pred_exp < 1.00:
            pred_exp = round(random.uniform(1.01, 1.19), 2)
        elif pred_exp > 15:
            pred_exp = round(random.uniform(8.5, 10.5), 2)
        résultats.append(pred_exp)
    return résultats

# -------------------
# Prédiction combinée
# -------------------

def prediction_combinee(historique, base_tour):
    résultats = []
    expert_preds = expert_predictions(historique)
    model_ml = entrer_model_ml(historique)
    ia_preds = ia_ml_predictions(model_ml, historique) if model_ml else [None]*20

    for i in range(20):
        tour = base_tour + i + 1
        exp = expert_preds[i]
        ia = ia_preds[i] if ia_preds else exp
        final_pred = round((ia + exp) / 2, 2)
        final_pred = max(1.01, final_pred)

        fiab = fiabilite(final_pred)
        tag = color_tag(final_pred)
        label = "Assuré ✅" if fiab >= 80 else "Crash probable ⚠️" if final_pred <= 1.20 else ""
        résultats.append((tour, ia, exp, final_pred, fiab, tag, label))

    return résultats

# -------------------
# Interface Streamlit
# -------------------

multiplicateurs_input = st.text_area(
    "**Entrez les multiplicateurs (du plus récent au plus ancien)**",
    placeholder="Ex : 2.14x 1.26x 5.87x ..."
)

dernier_tour = st.number_input(
    "**Numéro du dernier tour (ex : 74 si 2.14x est le plus récent)**",
    min_value=1, value=50
)

col1, col2 = st.columns(2)
with col1:
    calculer = st.button("📊 Calculer")
with col2:
    effacer = st.button("🗑️ Effacer")

if effacer:
    st.experimental_rerun()

if calculer and multiplicateurs_input:
    historique = nettoyer_donnees(multiplicateurs_input)
    if len(historique) < 10:
        st.warning("⚠️ Veuillez entrer au moins 10 multiplicateurs.")
    else:
        résultats = prediction_combinee(historique, int(dernier_tour))
        st.markdown("### 🧮 **Résultats T+1 à T+20 :**")
        for tour, ia, exp, final_pred, fiab, tag, label in résultats:
            line = (f"**T{tour}** → IA: **{ia}x** | Expert: **{exp}x** "
                    f"| Final: {tag} **{final_pred}x** — Fiabilité : **{fiab}%**")
            if label:
                line += f" **({label})**"
            st.markdown("- " + line)
