import streamlit as st

--- Function to convert multiplier to integer (remove dot) ---

def convert_to_int(value): return int(str(value).replace('.', ''))

--- Strategy using mod 10 logic ---

def mod10_strategy(multipliers): results = [] for i, m in enumerate(multipliers): val = convert_to_int(m) mod_val = val % 10

if mod_val in [3, 6, 9]:
        prediction = f"T{i} → {m} → MOD10: {mod_val} → Possible x5+"
    else:
        prediction = f"T{i} → {m} → MOD10: {mod_val} → Tendance faible"

    results.append(prediction)
return results

--- Streamlit UI ---

st.set_page_config(page_title="Aviator Mod10 Prediction", page_icon="✈️", layout="centered") st.title("✈️ Aviator Prediction - Mod10 Strategy")

st.markdown(""" Toromarika:

Ampidiro ny 10 na mihoatra amin'ny multiplicateurs (oh: 1.13, 1.02, 3.49)

Ny logique: raha MOD10 = 3, 6, 9 → dia misy possibilité hahatonga x5+ """)


input_values = st.text_input("Multiplicateurs (séparés par des virgules)")

if input_values: try: raw_list = [float(x.strip()) for x in input_values.split(',')] results = mod10_strategy(raw_list)

st.subheader("Résultat des prédictions:")
    for res in results:
        st.success(res)
except ValueError:
    st.error("Azafady, ampidiro tsara ny isa (ex: 1.15, 2.00, 3.49)")

