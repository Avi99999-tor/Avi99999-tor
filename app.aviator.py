import streamlit as st
import numpy as np
import pandas as pd
import random

# --- Authentification ---
def check_login(username, password):
    return username == "Topexacte" and password == "5312288612bet261"

# --- Nettoyage et validation ---
def clean_and_validate_history(raw_text):
    entries = raw_text.strip().split()
    cleaned = []
    errors = []
    for val in entries:
        val = val.upper().replace("O", "0").replace(",", ".")
        if not val.endswith("X"):
            val += "X"
        try:
            float(val.replace("X", ""))
            cleaned.append(val)
        except:
            errors.append(val)
    return cleaned, errors

# --- Prédiction ---
def calculate_predictions(cleaned_history, last_tour_number):
    multipliers = [float(x.replace("X", "")) for x in cleaned_history]
    predictions = []
    for i in range(1, 21):
        recent = multipliers[-5:]
        avg = np.mean(recent)
        std = np.std(recent)
        mod_vals = [int(str(x).split(".")[-1]) % 10 for x in recent if '.' in str(x)]
        mod_score = sum([1 for m in mod_vals if m in [2, 4, 7]])

        pred_base = avg + random.uniform(-0.4, 0.6)
        fiab = 60 + min(40, max(0, 10 * (mod_score + (std > 1.2) + (avg < 2.0))))
        if pred_base < 1.2:
            fiab -= 10

        predictions.append({
            "Tour": f"T{last_tour_number + i}",
            "Prédiction": round(pred_base, 2),
            "Fiabilité": f"{min(99, max(30, int(fiab)))}%"
        })
        multipliers.append(pred_base)
    return pd.DataFrame(predictions)

# --- Interface Streamlit ---
st.set_page_config(page_title="Prediction Expert by Mickael", layout="centered")
st.markdown("### **Prediction Expert by Mickael**")
st.markdown("**Admin:** Mickael  |  **Contact:** 033 31 744 68")
st.markdown("---")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    with st.form("login_form"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter")
        if submitted and check_login(username, password):
            st.session_state.authenticated = True
            st.success("Connexion réussie!")
        elif submitted:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

else:
    st.success("Connecté en tant que Topexacte")
    st.markdown("### **Entrer l'historique des multiplicateurs**")
    st.markdown("*Format: 1.22x 3.45x 1.00x ...*")

    with st.form("prediction_form"):
        history_input = st.text_area("Historique des tours précédents", height=150)
        last_tour = st.text_input("Numéro du dernier tour", placeholder="Ex: 150")
        submitted_predict = st.form_submit_button("Calculer les prédictions")
        clear_button = st.form_submit_button("Effacer")

    if clear_button:
        st.experimental_rerun()

    if submitted_predict:
        if not history_input.strip() or not last_tour.strip():
            st.warning("Veuillez entrer l'historique et le numéro du dernier tour.")
        else:
            cleaned_history, errors = clean_and_validate_history(history_input)
            if len(cleaned_history) < 5:
                st.error("Il faut au moins 5 valeurs valides.")
            elif len(cleaned_history) > 20:
                st.warning("Seulement les 20 dernières valeurs seront prises en compte.")
                cleaned_history = cleaned_history[-20:]

            if errors:
                st.error(f"Erreurs trouvées: {', '.join(errors)}")
                st.info("Les erreurs sont affichées en rouge ci-dessus. Veuillez corriger.")
            else:
                results = calculate_predictions(cleaned_history, int(last_tour))
                st.markdown("---")
                st.subheader("Résultats des prédictions (T+1 à T+20)")
                st.dataframe(results, use_container_width=True)
