import streamlit as st
import random
import datetime

st.set_page_config(page_title="Aviator Probabilistic Predictor", layout="centered")

st.title("Aviator Probabilistic Predictor")
st.markdown("**Miorina amin'ny stratégie: RNG seed + Mod 10 + Analyse tendancielle**")

st.subheader("1. Input dernières multiplicateurs")
multipliers_input = st.text_area("Ex: 1.05, 2.00, 1.52, 1.52, 3.49", height=100)

if st.button("Calculer prédiction"):
    try:
        # STEP 1: Extraction des chiffres après virgule
        multipliers = [float(m.strip()) for m in multipliers_input.split(",")]
        all_digits = []
        for m in multipliers:
            parts = str(m).split(".")
            if len(parts) == 2:
                digits = [int(d) for d in parts[0] + parts[1]]
            else:
                digits = [int(d) for d in parts[0]]
            all_digits.extend(digits)

        st.write(f"Chiffres extraits ({len(all_digits)} total): {all_digits}")

        # STEP 2: Génération de chiffres RNG (seed = date du jour)
        seed = int(datetime.date.today().strftime("%Y%m%d"))
        random.seed(seed)
        rng_digits = [random.randint(0, 9) for _ in range(len(all_digits))]
        st.write(f"RNG (seed = {seed}): {rng_digits}")

        # STEP 3: Addition Mod 10
        final_digits = [(a + b) % 10 for a, b in zip(all_digits, rng_digits)]
        st.write(f"Résultat après Mod 10: {final_digits}")

        # STEP 4: Groupement & Analyse
        window_size = 10
        seeds = [final_digits[i:i+window_size] for i in range(0, len(final_digits), window_size)]

        st.subheader("Résultat Analyse:")
        for i, group in enumerate(seeds):
            if len(group) < 5:
                continue
            count_high = sum(1 for x in group if x >= 8)
            pourcentage = round((count_high / len(group)) * 100, 2)
            tendance = "Possible montée (X5+)" if count_high >= 2 else "Tendance faible"

            st.markdown(f"""
            **T{i+1} → T{i+1+window_size-1}**  
            → Pourcentage haute valeur: `{pourcentage}%`  
            → Prédiction: `{tendance}`  
            """)
    except Exception as e:
        st.error(f"Erreur: {e}")
