import streamlit as st import random from datetime import datetime

st.set_page_config(page_title="Aviator Rolling Prediction", layout="centered")

st.title("Aviator Prediction - Probabilistic Mode")

st.markdown("---")

st.subheader("1. Input des multiplicateurs (5 derniers)") user_input = st.text_input("Entrez les 5 derniers multiplicateurs séparés par des virgules:", "1.05, 2.00, 1.52, 1.52, 3.49")

try: multipliers = [float(x.strip()) for x in user_input.split(",") if x.strip()] assert len(multipliers) >= 5

# STEP 1: Extraction des chiffres après la virgule
digits = []
for m in multipliers:
    parts = str(m).split(".")
    if len(parts) == 2:
        digits.append(int(parts[0]))
        digits.extend([int(d) for d in parts[1]])
    else:
        digits.append(int(parts[0]))
        digits.extend([0, 0])  # Si pas de virgule

# Limiter à 15 chiffres max
digits = digits[:15]

st.markdown(f"**Chiffres extraits :** {digits}")

# STEP 2: Generation RNG
seed_val = st.number_input("Seed (modifiable si besoin)", value=20250502, step=1)
random.seed(seed_val)
rng_digits = [random.randint(0, 9) for _ in range(len(digits))]

st.markdown(f"**RNG Digits :** {rng_digits}")

# STEP 3: Modulo 10
mod_digits = [(d + r) % 10 for d, r in zip(digits, rng_digits)]
st.markdown(f"**Résultat (mod 10):** {mod_digits}")

# STEP 4: Seeds groupés
seed1 = "".join(str(x) for x in mod_digits[:10])
seed2 = "".join(str(x) for x in mod_digits[10:])

st.markdown(f"**Seed 1 :** `{seed1}`")
st.markdown(f"**Seed 2 :** `{seed2}`")

st.markdown("---")
st.subheader("2. Prédictions possibles")

# Analyse probabiliste simple
signal_haut = sum(1 for x in mod_digits if x >= 7)
signal_moyen = sum(1 for x in mod_digits if 4 <= x <= 6)
signal_bas = sum(1 for x in mod_digits if x <= 3)

if signal_haut >= 4:
    tendance = "FORTE montée (possible X5 à X10 dans les 3 à 5 prochains tours)"
elif signal_haut >= 2:
    tendance = "Moyenne probabilité de montée (X3 à X5)"
elif signal_bas >= 5:
    tendance = "Crash probable (X1.00 à X2.00)"
else:
    tendance = "Stable ou fluctuation normale"

st.success(f"**Analyse :** {tendance}")

# Rolling prédiction
st.markdown("### Rolling prédictions")
st.markdown("**Tours prédits (prochains):**")
current_tour = st.number_input("Dernier numéro de tour connu:", value=80, step=1)

pred_tours = []
if signal_haut >= 3:
    pred_tours = [f"T{current_tour+3}", f"T{current_tour+4}", f"T{current_tour+5}"]
elif signal_bas >= 5:
    pred_tours = [f"T{current_tour+1}", f"T{current_tour+2}", f"T{current_tour+3}"]
else:
    pred_tours = [f"T{current_tour+2}", f"T{current_tour+3}", f"T{current_tour+4}"]

st.info(" / ".join(pred_tours) + " → **x5+ Possibility**")

except Exception as e: st.error("Erreur de traitement. Vérifiez vos données.") st.exception(e)

