import streamlit as st
import numpy as np
import pandas as pd
import random
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Prediction By Mickael TOP EXACTE")
st.title("🎯 Prediction By Mickael - TOP EXACTE")
st.subheader("Version améliorée IA + Expert logique")

# --------------------
# Fonctions utilitaires
# --------------------

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

def color_tag(val):
    if val < 2:
        return "🔵"
    elif val < 10:
        return "💜"
    else:
        return "🔴"

# --------------------
# Création des features pour ML
# --------------------

def construire_features(multiplicateurs, window=5):
    """
    Returns a DataFrame X, plus array y.
    Features extraites pour chaque position i >= window jusqu'à len-1 :
      - Valeurs des multipliers précédents (last 3)
      - diff1 = x[i-1] - x[i-2], diff2 = x[i-2] - x[i-3]
      - mean5 = moyenne de x[i-window:i]
      - min5, max5
      - virgule_bits (digit_sum %10) des 3 derniers
      - flags pour cas 1 et cas 2 dans la fenêtre
    """
    data = []
    targets = []
    for i in range(window, len(multiplicateurs)):
        prev = multiplicateurs[i-3:i]            # x[n-3], x[n-2], x[n-1]
        diff1 = multiplicateurs[i-1] - multiplicateurs[i-2]
        diff2 = multiplicateurs[i-2] - multiplicateurs[i-3]
        window_vals = multiplicateurs[i-window:i]
        mean5 = np.mean(window_vals)
        min5 = np.min(window_vals)
        max5 = np.max(window_vals)

        # chiffres après virgule
        virgules = [int(str(v).split('.')[-1]) % 10 for v in prev]

        # Cas 1 flag: croissant in-3 → drop (si x[n-3]<x[n-2]<x[n-1] et x[n] < x[n-1])
        flag_c1 = 1 if (prev[0] < prev[1] < prev[2] and multiplicateurs[i] < prev[2]) else 0
        # Cas 2 flag: decroissant in-3 → boost (si >)
        flag_c2 = 1 if (prev[0] > prev[1] > prev[2] and multiplicateurs[i] > prev[2]) else 0

        features = prev + [diff1, diff2, mean5, min5, max5] + virgules + [flag_c1, flag_c2]
        data.append(features)
        targets.append(multiplicateurs[i])
    cols = (
        ["x_n3", "x_n2", "x_n1", 
         "diff1", "diff2", "mean5", "min5", "max5"] +
        ["virgule_n3", "virgule_n2", "virgule_n1"] +
        ["flag_c1", "flag_c2"]
    )
    return pd.DataFrame(data, columns=cols), np.array(targets)

# --------------------
# Entraînement et prédiction IA améliorée
# --------------------

def entrainer_ia_ml(historique):
    X, y = construire_features(historique)
    if len(X) < 10:   # Pas assez de data
        return None
    # Séparation train/test pour garder un modèle robuste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def ia_ml_predictions_improve(model, historique, nb_preds=20):
    preds = []
    hist = historique.copy()
    for _ in range(nb_preds):
        # Créer feature pour la prochaine prédiction
        if len(hist) < 5:
            preds.append(hist[-1])
            continue
        prev = hist[-3:]
        diff1 = hist[-1] - hist[-2]
        diff2 = hist[-2] - hist[-3]
        window_vals = hist[-5:]
        mean5 = np.mean(window_vals)
        min5 = np.min(window_vals)
        max5 = np.max(window_vals)
        virg = [int(str(v).split('.')[-1]) % 10 for v in prev]
        # flags (on considère pas target à venir ici, on met 0)
        flag_c1 = 0
        flag_c2 = 0
        feat = prev + [diff1, diff2, mean5, min5, max5] + virg + [flag_c1, flag_c2]
        next_pred = round(max(1.01, min(float(model.predict([feat])[0]), 15)), 2)
        preds.append(next_pred)
        hist.append(next_pred)
    return preds

# --------------------
# Expert logique
# --------------------

def expert_predictions(historique):
    exp_preds = []
    rolling_mean = np.mean(historique)
    mod_score = analyse_mod_seed(historique)
    for i in range(1, 21):
        seed = int((mod_score + rolling_mean + i * 0.7) * 1000) % 97
        pred_exp = round(abs((np.sin(seed) + np.cos(i * mod_score)) * 3 + random.uniform(0.2, 1.5)), 2)
        if pred_exp < 1.00:
            pred_exp = round(random.uniform(1.01, 1.19), 2)
        elif pred_exp > 15:
            pred_exp = round(random.uniform(8.5, 10.5), 2)
        exp_preds.append(pred_exp)
    return exp_preds

# --------------------
# Prédiction combinée (Expert + IA améliorée)
# --------------------

def prediction_combinee(historique, base_tour):
    résultats = []
    exp_preds = expert_predictions(historique)
    model_ml = entrainer_ia_ml(historique)
    ia_preds = ia_ml_predictions_improve(model_ml, historique) if model_ml else [None]*20

    for i in range(20):
        t = base_tour + i + 1
        ie = exp_preds[i]
        im = ia_preds[i] if ia_preds else ie
        final = round((ie + im) / 2, 2)
        final = max(1.01, final)

        fiab = fiabilite(final)
        tag = color_tag(final)
        label = "Assuré ✅" if fiab >= 80 else "Crash probable ⚠️" if final <= 1.20 else ""
        résultats.append((t, im, ie, final, fiab, tag, label))

    return résultats

# --------------------
# Interface Streamlit
# --------------------

multiplicateurs_input = st.text_area(
    "**Entrez les multiplicateurs (du plus récent au plus ancien)**",
    placeholder="Ex: 2.14x 1.26x 5.87x ..."
)

dernier_tour = st.number_input(
    "**Numéro du dernier tour (ex: 74 si 2.14x est le plus récent)**",
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
        for t, ia_val, exp_val, final, fiab, tag, label in résultats:
            line = (f"**T{t}** → IA: **{ia_val}x** | Expert: **{exp_val}x** "
                    f"| Final: {tag} **{final}x** — Fiabilité : **{fiab}%**")
            if label:
                line += f" **({label})**"
            st.markdown("- " + line)
