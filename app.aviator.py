import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="Aviator Prediction", layout="centered")

st.title("Aviator Game Prediction — Rolling Version")
st.markdown("**Version probabiliste simple avec prédiction sur les 3-5 tours suivants.**")

# Input du dernier multiplicateur
dernier_tour = st.number_input("Dernier numéro de tour connu (ex: 70)", min_value=0, step=1)
multiplicateurs_input = st.text_input("Derniers multiplicateurs (5 valeurs séparées par des virgules)", value="1.05,2.00,1.52,1.52,3.49")

# Traitement
if st.button("Prédire les prochains tours"):
    try:
        multipliers = [float(x.strip()) for x in multiplicateurs_input.split(",") if x.strip()]
        digits = []

        for m in multipliers:
            int_str = str(m).replace('.', '')
            digits.extend([int(c) for c in int_str])

        # Seed automatique du jour
        seed_value = int(datetime.now().strftime("%Y%m%d"))
        random.seed(seed_value)
        rng_digits = [random.randint(0, 9) for _ in range(len(digits))]

        # Mod 10
        mod10 = [(d + r) % 10 for d, r in zip(digits, rng_digits)]

        # Groupement (10 par 10)
        seeds = [mod10[i:i + 10] for i in range(0, len(mod10), 10)]

        st.subheader("Résultat de l’analyse")
        for i, group in enumerate(seeds):
            seed_number = "".join(map(str, group))
            st.text(f"Seed {i + 1}: {seed_number}")

        # Analyse tendance
        st.subheader("Prédiction des tours suivants")

        predictions = []
        for i in range(3):
            next_tour = dernier_tour + 3 + i
            sub = mod10[-10 + i:] if len(mod10) >= 10 else mod10
            chance_haute = sub.count(8) + sub.count(9)
            if chance_haute >= 2:
                predictions.append((next_tour, "Possible x5/x10"))
            else:
                predictions.append((next_tour, "Probable crash (<x2)"))

        for t, pred in predictions:
            st.markdown(f"**T{t}** —> {pred}")

        st.info(f"Seed utilisée: `{seed_value}` — Tendance en cours évaluée sur {len(digits)} chiffres.")

    except Exception as e:
        st.error(f"Erreur lors de l’analyse: {e}")
