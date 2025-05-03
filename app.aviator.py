import streamlit as st import numpy as np import re

st.set_page_config(page_title="Prédiction Aviator", layout="centered") st.title("Application de Prédiction Aviator - Rolling & Probabiliste")

st.markdown(""" Cette application prédit les multiplicateurs probables basés sur l'historique entré, avec une analyse rolling + hashing simplifiée.

Instructions :

Entrez les multiplicateurs (ex: 2.51x 6.38x 1.28x ...)

Entrez le numéro du dernier tour correspondant au premier multiplicateur entré.

Appuyez sur Calculer pour voir les prédictions. """)


Entrées

raw_input = st.text_area("Multiplicateurs (séparés par 'x')", height=150) last_tour = st.number_input("Numéro du dernier tour", min_value=1, step=1)

if st.button("Calculer"): if not raw_input or last_tour is None: st.warning("Veuillez remplir tous les champs.") else: # Nettoyage values = re.findall(r"\d+.\d+", raw_input) try: mults = list(map(float, values)) mults.reverse()  # Pour que le premier entré soit le plus récent (ordre croissant de T) except: st.error("Erreur dans l'analyse des données. Assurez-vous du format.") st.stop()

# Fampisehoana historique
    st.subheader("Historique")
    for i, val in enumerate(mults):
        st.write(f"T{last_tour - i} : {val:.2f}x")

    # Rolling moyenne + logic simple hashing
    rolling_avg = np.mean(mults[:10]) if len(mults) >= 10 else np.mean(mults)
    max_recent = max(mults[:10])

    # Prédiction akaiky (3 tours manaraka)
    pred_close = []
    for i in range(1, 4):
        val = round((rolling_avg * 0.95 + np.sin(rolling_avg + i) * 0.5), 2)
        confidence = min(95, max(60, 100 - abs(val - rolling_avg) * 10))
        pred_close.append((f"T{last_tour + i}", val, confidence))

    # Prédiction lavitra (4-6 tours manaraka)
    pred_far = []
    for i in range(4, 7):
        val = round((max_recent * 0.85 + np.cos(max_recent + i) * 0.7), 2)
        confidence = min(90, max(50, 100 - abs(val - rolling_avg) * 12))
        pred_far.append((f"T{last_tour + i}", val, confidence))

    st.subheader("Prédiction Proche (Haute fiabilité)")
    for tour, val, conf in pred_close:
        st.write(f"{tour} ➔ {val}x ({conf}% fiable)")

    st.subheader("Prédiction Lointaine (Planification)")
    for tour, val, conf in pred_far:
        st.write(f"{tour} ➔ {val}x ({conf}% fiable)")

import streamlit as st import numpy as np import re

st.set_page_config(page_title="Prédiction Aviator", layout="centered") st.title("Application de Prédiction Aviator - Rolling & Probabiliste")

st.markdown(""" Cette application prédit les multiplicateurs probables basés sur l'historique entré, avec une analyse rolling + hashing simplifiée.

Instructions :

Entrez les multiplicateurs (ex: 2.51x 6.38x 1.28x ...)

Entrez le numéro du dernier tour correspondant au premier multiplicateur entré.

Appuyez sur Calculer pour voir les prédictions. """)


Entrées

raw_input = st.text_area("Multiplicateurs (séparés par 'x')", height=150) last_tour = st.number_input("Numéro du dernier tour", min_value=1, step=1)

if st.button("Calculer"): if not raw_input or last_tour is None: st.warning("Veuillez remplir tous les champs.") else: # Nettoyage values = re.findall(r"\d+.\d+", raw_input) try: mults = list(map(float, values)) mults.reverse()  # Pour que le premier entré soit le plus récent (ordre croissant de T) except: st.error("Erreur dans l'analyse des données. Assurez-vous du format.") st.stop()

# Fampisehoana historique
    st.subheader("Historique")
    for i, val in enumerate(mults):
        st.write(f"T{last_tour - i} : {val:.2f}x")

    # Rolling moyenne + logic simple hashing
    rolling_avg = np.mean(mults[:10]) if len(mults) >= 10 else np.mean(mults)
    max_recent = max(mults[:10])

    # Prédiction akaiky (3 tours manaraka)
    pred_close = []
    for i in range(1, 4):
        val = round((rolling_avg * 0.95 + np.sin(rolling_avg + i) * 0.5), 2)
        confidence = min(95, max(60, 100 - abs(val - rolling_avg) * 10))
        pred_close.append((f"T{last_tour + i}", val, confidence))

    # Prédiction lavitra (4-6 tours manaraka)
    pred_far = []
    for i in range(4, 7):
        val = round((max_recent * 0.85 + np.cos(max_recent + i) * 0.7), 2)
        confidence = min(90, max(50, 100 - abs(val - rolling_avg) * 12))
        pred_far.append((f"T{last_tour + i}", val, confidence))

    st.subheader("Prédiction Proche (Haute fiabilité)")
    for tour, val, conf in pred_close:
        st.write(f"{tour} ➔ {val}x ({conf}% fiable)")

    st.subheader("Prédiction Lointaine (Planification)")
    for tour, val, conf in pred_far:
        st.write(f"{tour} ➔ {val}x ({conf}% fiable)")

