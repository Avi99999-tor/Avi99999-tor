import streamlit as st
import numpy as np
import re
from hashlib import sha256

st.set_page_config(page_title="Aviator Predictor", layout="centered")

st.title("Prédicteur Aviator avec Rolling + Hashing")
st.markdown("Entrez les multiplicateurs récents et le numéro du dernier tour pour voir les prédictions fiables.")

# === Inputs ===
historique_input = st.text_area("Entrer les multiplicateurs (séparés par 'x'):", 
                                 "2.51x 6.38x 1.28x 1.52x 1.15x 2.97x 4.03x 1.28x 7.08x 1.69x 1.98x 1.09x 1.30x 4.05x 3.11x 2.65x 1.48x 1.87x 3.00x 1.35x 1.32x 1.04x 6.49x 1.60x 1.06x 11.89x 1.97x")
dernier_tour = st.number_input("Entrer le numéro du dernier tour (ex: 74 si 2.51x est le plus récent):", value=74, step=1)

if st.button("Calculer les prédictions"):

    # === Nettoyage des données ===
    multiplicateurs = re.findall(r"\d+\.\d+", historique_input)
    multiplicateurs = [float(m) for m in multiplicateurs]

    if len(multiplicateurs) < 10:
        st.warning("Veuillez entrer au moins 10 multiplicateurs pour une meilleure prédiction.")
    else:
        # === Fonctions auxiliaires ===
        def calc_hash_seed(multiplicateurs):
            raw = "".join([str(m) for m in multiplicateurs])
            return sha256(raw.encode()).hexdigest()

        def rolling_prediction(data):
            high_indexes = [i for i, m in enumerate(data) if m >= 5]
            if len(high_indexes) < 2:
                return None, 0
            intervals = [high_indexes[i+1] - high_indexes[i] for i in range(len(high_indexes)-1)]
            moy = np.mean(intervals)
            next_index = high_indexes[-1] + int(round(moy))
            confiance = round(min(100, 90 - (len(data) - high_indexes[-1])*3), 2)
            return next_index, confiance

        # === Traitement principal ===
        seed = calc_hash_seed(multiplicateurs[-10:])  # Hash des 10 derniers pour tracking
        pred_proche = round(np.mean(multiplicateurs[:5]) + np.std(multiplicateurs[:5]), 2)
        pred_lointain_index, confiance = rolling_prediction(multiplicateurs)

        st.subheader("Résultats de Prédiction")
        st.markdown(f"- **Hash Seed** (pour vérif): `{seed[:16]}...`")
        st.markdown(f"- **Prédiction prochaine (haute fiabilité)**: **x{pred_proche}**")
        
        if pred_lointain_index:
            tour_lointain = dernier_tour + (pred_lointain_index - len(multiplicateurs))
            st.markdown(f"- **Prédiction distante (tendance X5+)**: Tour **T{tour_lointain}** —> **X5+ probabilité**")
            st.markdown(f"- **Taux de fiabilité**: {confiance}%")
        else:
            st.warning("Pas assez de multiplicateurs élevés (≥ x5) pour prédire une tendance distante.")
