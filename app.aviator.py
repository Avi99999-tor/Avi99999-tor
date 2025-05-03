import streamlit as st import random

st.set_page_config(page_title="Aviator Probabilistic Predictor", layout="centered")

st.title("Aviator Predictor - Stratégie Probabiliste") st.markdown(""" Toromarika: Ampidiro eto ambany ny 5 dernières valeurs an'ireo multiplicateurs (ex: 1.05, 2.00, ...) """)

Input user

cols = st.columns(5) values = [] for i, col in enumerate(cols): with col: val = st.text_input(f"T{62+i}", key=f"t{i}") if val: try: float_val = float(val) values.append(float_val) except: st.error(f"T{62+i} dia tsy isa manan-kery")

if len(values) == 5: # STEP 1: extraction chiffres après virgule digits = [] for val in values: digits += [int(d) for d in f"{val:.2f}".replace('.', '')]

st.markdown("### **Étape 1 : Chiffres extraits**")
st.write(digits)

# STEP 2: generate RNG digits
seed = int(st.secrets["seed"]) if "seed" in st.secrets else 20250502
random.seed(seed)
rng_digits = [random.randint(0, 9) for _ in range(len(digits))]

# STEP 3: Mod 10
result_digits = [(a + b) % 10 for a, b in zip(digits, rng_digits)]

# STEP 4: Seeds
grouped = [''.join(map(str, result_digits[i:i+10])) for i in range(0, len(result_digits), 10)]

st.markdown("### **Résultat (Vinavina)**")
for i, g in enumerate(grouped):
    if len(g) == 10:
        st.code(f"Seed {i+1}: {g}")

st.markdown("---")
# Analyse Probabiliste Simplifiée
high_digits = sum([1 for d in result_digits if d >= 7])
low_digits = sum([1 for d in result_digits if d <= 3])

if high_digits >= 4:
    st.success("Misy fiakarana (tendance X5–X10) afaka tour 1–3")
elif low_digits >= 6:
    st.warning("Tendance ambany (x1.00–x2.00), miandrasa")
else:
    st.info("Tendance mifangaro, mety hisy X3–X4")

else: st.info("Ampidiro daholo ny 5 valeurs")

