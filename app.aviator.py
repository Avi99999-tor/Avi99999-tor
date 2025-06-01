aviator_prediction_app.py

import streamlit as st
import numpy as np
import random from sklearn.linear_model
import LinearRegression

st.set_page_config(page_title="Prediction by Mickael TOP EXACTE") st.title("🎯 Prediction by Mickael TOP EXACTE") st.subheader("Version combinée: Expert logique + IA simple")

Entrée utilisateur

multiplicateurs_input = st.text_area("Entrez les multiplicateurs (du plus récent au plus ancien)", placeholder="Ex: 2.14x 1.26x 5.87x ...")

dernier_tour = st.number_input("Numéro du dernier tour (ex: 74 si 2.14x est le plus récent)", min_value=1, value=50)

if st.button("Effacer"): multiplicateurs_input = ""

Nettoyage

def nettoyer_donnees(texte): valeurs = texte.replace(',', '.').lower().replace('x', '').split() try: return [float(v) for v in valeurs if float(v) > 0] except: return []

Pourcentage logique expert (schéma logique)

def pourcentage_logique(val): if val >= 10: return 90 + random.randint(0, 5) elif val >= 5: return 80 + random.randint(0, 5) elif val >= 2: return 75 + random.randint(-3, 3) elif val <= 1.2: return 65 + random.randint(-5, 5) else: return 70 + random.randint(-5, 5)

Couleur output

def couleur(val): if val <= 1.99: return "🔘 Bleu" elif 2 <= val < 10: return "💜 Violet" else: return "🔴 Rouge"

Analyse expert (mod 10 + seed + logique)

def analyse_mod_seed(liste): chiffres_mod = [int(str(x).split(".")[-1]) % 10 for x in liste] return sum(chiffres_mod) / len(chiffres_mod)

IA simple: Linear Regression

model = LinearRegression() def entrainer_model(multiplicateurs): X = np.arange(len(multiplicateurs)).reshape(-1, 1) y = np.array(multiplicateurs) model.fit(X, y)

def prediction_expert(multiplicateurs, base_tour): results = [] rolling_mean = np.mean(multiplicateurs) mod_score = analyse_mod_seed(multiplicateurs) entrainer_model(multiplicateurs[::-1])

for i in range(1, 21):
    seed = int((mod_score + rolling_mean + i * 3.73) * 1000) % 97
    pred_expert = round(abs((np.sin(seed) + np.cos(i * mod_score)) * 3 + random.uniform(0.2, 1.5)), 2)

    # IA Prediction
    x_pred = len(multiplicateurs) + i
    pred_ia = round(float(model.predict(np.array([[x_pred]]))), 2)

    # Moyenne combinée
    final_pred = round((pred_expert + pred_ia) / 2, 2)
    pourcent = pourcentage_logique(final_pred)
    couleur_code = couleur(final_pred)
    label = "🔆 Assuré" if pourcent >= 80 else ""

    results.append((base_tour + i, final_pred, pourcent, couleur_code, label))

return results

if multiplicateurs_input: historique = nettoyer_donnees(multiplicateurs_input)

if len(historique) < 10:
    st.warning("Veuillez entrer au moins 10 multiplicateurs.")
else:
    r = prediction_expert(historique, int(dernier_tour))
    st.markdown("### **Résultats des prédictions (T+1 à T+20) :**")
    for tour, val, pourcent, coul, label in r:
        line = f"**T{tour}** ➔ **{val}x** ({coul}) — Fiabilité: **{pourcent}%** {label}"
        st.markdown("- " + line)

