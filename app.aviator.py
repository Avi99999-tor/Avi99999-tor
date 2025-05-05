import streamlit as st import pandas as pd

Fonction de prédiction simple (mod10) basé sur le dernier tour

def predict_mod10(last_multiplier): # Extraire la partie décimale en entier decimal = int((last_multiplier % 1) * 100) mod10 = decimal % 10 # Déterminer la prédiction selon mod10 if mod10 < 3: return "Prévision: X1 - X2" elif mod10 < 7: return "Prévision: X2 - X5" else: return "Prévision: X5+"

Interface Streamlit

st.set_page_config(page_title="Aviator Prediction", layout="centered") st.title("Aviator Prediction Expert")

Saisie de l'historique des multiplicateurs

history_input = st.text_area( "Entrez l'historique des multiplicateurs (ex: 3.33 1.45 2.06 ...):", height=150 )

if history_input: # Nettoyage et parsing values = [] for token in history_input.replace('\n', ' ').split(): try: values.append(float(token.lower().replace('x', ''))) except: pass

if values:
    # Afficher numéro du dernier tour
    last_index = len(values)
    st.write(f"**Numéro du dernier tour : T{last_index}**")
    st.write(f"**Dernier multiplicateur : {values[-1]:.2f}x**")
    # Prédiction
    prediction = predict_mod10(values[-1])
    st.subheader("Prédiction suivante :")
    st.success(prediction)
else:
    st.error("Aucune valeur valide détectée.")

ellse: st.info("Veuillez entrer les multiplicateurs pour générer une prédiction.")

