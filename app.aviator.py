import streamlit as st
import random

st.title("Aviator Prediction - Probabiliste Fiable")

# Saisie automatique an'ireo multiplicateurs 5 farany
multipliers_input = st.text_input("Multiplicateurs 5 farany (misaraka amin'ny virgule)", "1.05,2.00,1.52,1.52,3.49")
last_tour = st.number_input("Numéro du dernier tour (ex: 66)", value=66, step=1)
seed_value = st.number_input("Seed (ex: 20250502)", value=20250502, step=1)

# Traitement
def extract_digits(multis):
    digits = []
    for m in multis:
        parts = str(m).split(".")
        if len(parts) == 2:
            digits += [int(x) for x in parts[1]]
    return digits

def prediction_analysis(multis, seed):
    digits = extract_digits(multis)
    random.seed(seed)
    rng = [random.randint(0,9) for _ in range(len(digits))]
    results = [(d + r) % 10 for d, r in zip(digits, rng)]

    # Analyse tendance
    count_high = sum(1 for d in results if d >= 7)
    count_mid = sum(1 for d in results if 4 <= d <= 6)

    crash = count_high <= 1
    x5_possible = count_high >= 2 and count_high <= 3
    x10_possible = count_high >= 4

    return results, crash, x5_possible, x10_possible

# Execution
try:
    multipliers = [float(x.strip()) for x in multipliers_input.split(",")]
    if len(multipliers) == 5:
        results, crash, x5, x10 = prediction_analysis(multipliers, seed_value)

        # Numéros de tours à venir
        T1 = last_tour + 1
        T2 = last_tour + 2
        T3 = last_tour + 3

        st.markdown(f"### Résultats calculés : T{T1} → T{T3}")
        if crash:
            st.error("**Crash probable** dans les prochaines 3 tours.")
        elif x10:
            st.success(f"**Haute probabilité** de X10 entre T{T1}/T{T2}/T{T3}")
        elif x5:
            st.warning(f"**Possibilité de X5** entre T{T1}/T{T2}/T{T3}")
        else:
            st.info("**Tendance moyenne** – Prépare stratégie ou attendre.")

        st.markdown(f"**Numéros de Tours analysés:** {last_tour - 4} à {last_tour}")
        st.markdown(f"**Multiplicateurs Entrés:** {multipliers}")
    else:
        st.warning("Ampidiro tsara ny 5 multiplicateurs farany.")
except:
    st.error("Olana tamin'ny fanodinana ny angona. Zahao tsara ny format.")
