import streamlit as st
import numpy as np
import re
import pandas as pd

# --- Fonction de prédiction complète avec filtrage ---
def prediction_combinee(historique, dernier_tour):
    valeurs_brutes = [float(val.replace('x', '')) for val in historique]
    valeurs = []

    for v in valeurs_brutes:
        if v > 20:
            v = 20.0
        elif v > 10:
            v = v * 0.7
        valeurs.append(v)

    prediction = []
    moyenne = np.mean(valeurs[-10:])
    ecart_type = np.std(valeurs[-10:])

    for i in range(1, 21):
        prediction_val = round(moyenne + ((-1)**i) * (ecart_type * (i / 10)), 2)

        # Hashing simple basé sur le modulo
        if int(prediction_val * 100) % 10 in [0, 1, 2]:
            prediction_val = round(prediction_val * 0.75, 2)  # Crash probable
        elif int(prediction_val * 100) % 10 in [8, 9]:
            prediction_val = round(prediction_val * 1.5, 2)   # Boost possible

        # Fiabilité (plus on s'éloigne du présent, moins c'est fiable)
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
                
            # Export des prédictions en CSV
            export_data = []
            for tour, val, confiance in predictions:
                export_data.append([tour, val, confiance])
            
            df_export = pd.DataFrame(export_data, columns=["Numéro de tour", "Prédiction (x)", "Fiabilité (%)"])

            # Option d'exporter les résultats
            st.download_button(
                label="Télécharger les prédictions en CSV",
                data=df_export.to_csv(index=False).encode('utf-8'),
                file_name="predictions_aviator.csv",
                mime="text/csv"
            )
    else:
        st.error("Veuillez entrer les données d'historique.")
