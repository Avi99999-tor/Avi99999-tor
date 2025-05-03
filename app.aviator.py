import streamlit as st import random

st.set_page_config(page_title="Rolling Prediction Aviator", layout="centered")

st.title("Rolling Prediction - Aviator Game")

Input zone

st.markdown("### Entrer les 5 derniers multiplicateurs") mults_input = st.text_input("Ex: 1.05, 2.00, 1.52, 1.52, 3.49")

if mults_input: try: mults = [float(m.strip()) for m in mults_input.split(",") if m.strip()] if len(mults) < 5: st.warning("Veuillez entrer au moins 5 multiplicateurs.") else: # STEP 1 - Extraction des chiffres après virgule digits = [] for m in mults: m_str = str(m).replace(".", "") digits.extend([int(c) for c in m_str])

# Seed simulation
        seed = int("20250503")
        random.seed(seed)
        rng_digits = [random.randint(0, 9) for _ in range(len(digits))]

        # Addition mod 10
        final = [(a + b) % 10 for a, b in zip(digits, rng_digits)]

        # Rolling prédiction (3 seeds)
        rolling_predictions = []
        for i in range(0, len(final) - 9, 3):
            segment = final[i:i+10]
            if len(segment) == 10:
                count_high = sum(1 for v in segment if v >= 7)
                count_low = sum(1 for v in segment if v <= 3)
                tendance = "X5+" if count_high >= 3 else ("Crash" if count_low >= 5 else "Stable")
                proba = round((count_high / 10) * 100) if tendance == "X5+" else round((count_low / 10) * 100) if tendance == "Crash" else 60

                rolling_predictions.append({
                    "Tour": f"T{67 + i//3}",
                    "Tendance": tendance,
                    "Probabilité": f"{proba}%"
                })

        # Affichage tableau
        st.markdown("### Résultats")
        st.table(rolling_predictions)

except Exception as e:
    st.error(f"Erreur de traitement: {e}")

