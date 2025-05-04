import streamlit as st
import numpy as np
import re

# --- Fonction de prédiction complète ---
def prediction_combinee(historique, dernier_tour):
    valeurs = [float(val.replace('x', '')) for val in historique]
    prediction = []
    fiabilites = []

    # Rolling Prediction
    moyenne = np.mean(valeurs[-10:])
    ecart_type = np.std(valeurs[-10:])
    
    # Gérer les prédictions en fonction de la fiabilité
    for i in range(1, 21):
        prediction_val = round(moyenne + ((-1)**i) * (ecart_type * (i / 10)), 2)

        # Gestion des valeurs critiques (crash et haute valeur)
        if prediction_val < 1.5:
            prediction_val = round(prediction_val * 0.75, 2)  # Crash probable
        elif prediction_val >= 5:
            prediction_val = round(prediction_val * 1.5, 2)  # Haute valeur possible

        # Fiabilité - plus la prédiction est éloignée, moins elle est fiable
        pourcentage = max(30, 100 - i * 3)
        prediction.append((dernier_tour + i, prediction_val, pourcentage))

    return prediction

# --- Interface Streamlit ---
st.title("Prédiction Aviator - Version complète")

st.markdown("**Entrez l'historique des multiplicateurs** *(du plus récent au plus ancien, séparés par x)*:")
historique_input = st.text_area("Multiplicateurs (ex: 2.51x 6.38x 1.28x ...)")

numero_tour = st.number_input("Entrez le numéro du dernier tour (ex: 74 si 2.51x est le plus récent):", min_value=0, step=1)

if st.button("Calculer les prédictions"):
    if historique_input:
        historique = re.findall(r"\d+\.\d+x", historique_input)

        if len(historique) < 10:
            st.warning("Veuillez entrer au moins 10 valeurs de multiplicateurs.")
        else:
            predictions = prediction_combinee(historique, numero_tour)

            st.subheader("**Résultats des prédictions :**")
            for tour, val, confiance in predictions:
                couleur = "**(Crash probable)**" if val < 2 else ("**(Haute valeur probable)**" if val >= 5 else "")
                st.markdown(f"- **T{tour}** → **{val}x** — Fiabilité: **{confiance}%** {couleur}")
    else:
        st.error("Veuillez entrer les données d'historique.")
