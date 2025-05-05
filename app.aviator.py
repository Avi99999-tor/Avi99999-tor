import streamlit as st import pandas as pd

Fonction de prédiction avec stratégie Mod 10

def predict_next_mod10(history): if not history: return "Pas de données." try: last_value = float(history[-1]) prediction = (int(last_value * 100) % 10) return f"Mod10 (chiffre après virgule): {prediction}" except: return "Erreur dans les données."

Interface Streamlit

st.set_page_config(page_title="Aviator Prediction Expert - Mode Mod10", layout="centered") st.title("Aviator Prediction Expert") st.header("Stratégie : Mod 10")

Saisie des multiplicateurs

user_input = st.text_area("Historique de multiplicateurs (séparés par espace ou retour à la ligne)")

if user_input: # Traitement du texte en liste de valeurs raw_values = user_input.replace('\n', ' ').split() cleaned_values = [] for val in raw_values: try: cleaned_values.append(float(val.lower().replace('x', ''))) except: pass

if cleaned_values:
    st.write(f"**Numéro du dernier tour : T{len(cleaned_values)}**")
    st.write("**Historique de tours (multiplicateurs)**")
    st.write(cleaned_values)

    # Prédiction selon stratégie Mod 10
    prediction = predict_next_mod10(cleaned_values)
    st.success(f"Prédiction prochaine tendance : {prediction}")
else:
    st.error("Aucune donnée valide détectée.")

else: st.info("Veuillez entrer l'historique des multiplicateurs.")

