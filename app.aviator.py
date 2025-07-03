import streamlit as st
from datetime import datetime, timedelta
from PIL import Image
import numpy as np
import easyocr

# --- Configuration ---
st.set_page_config(page_title="🎯 Hybride Prediction Aviator by Mickael", layout="centered")
st.title("🇲🇬 🎯 Hybride Prediction Aviator by Mickael")

# --- Connexion simplifiée ---
st.markdown("## 🔐 Connexion")
username = st.text_input("👤 Nom utilisateur")
password = st.text_input("🔑 Code secret", type="password")

if username == "admin" and password == "1234":
    st.success("✅ Connexion réussie!")

    # --- OCR Upload avec correction automatique ---
    st.markdown("### 📸 Image Historique (OCR automatique avec nettoyage)")
    uploaded_image = st.file_uploader("🖼️ Ampidiro capture historique", type=["png", "jpg", "jpeg"])

    def corriger_ocr(raw_text):
        text = raw_text.replace("O", "0").replace("o", "0")
        text = text.replace("X", "x").replace("x", "x")
        return text

    if uploaded_image is not None:
        with st.spinner("🔍 Traitement OCR..."):
            try:
                image = Image.open(uploaded_image)
                st.image(image, caption="🖼️ Sary nampidirina", use_column_width=True)
                reader = easyocr.Reader(['en'], gpu=False)
                result = reader.readtext(np.array(image), detail=0)
                texte_ocr = corriger_ocr(" ".join(result))
                st.session_state['ocr_result'] = texte_ocr
                st.success("✅ OCR sy correction automatique vita.")
            except Exception as e:
                st.error(f"❌ OCR Error: {e}")

    # --- Zone unique pour historique (auto + manokana)
    multiplicateurs_input = st.text_area("📥 Historique (OCR automatique na tànana)", 
        value=st.session_state.get("ocr_result", ""), 
        placeholder="Ex: 1.21x 1.33x 12.66x 1.44x ...", height=150)

    # --- Paramètres prédiction ---
    dernier_tour = st.number_input("🔢 Numéro du dernier tour", min_value=1, value=123)
    heure_input = st.text_input("🕒 Heure du dernier tour (hh:mm:ss)", value="20:30:05")
    calculer = st.button("🔮 Lancer la prédiction")

    # --- Fonctions ---
    def extraire_valeurs(texte):
        texte = corriger_ocr(texte)
        valeurs = texte.replace(",", ".").lower().replace("x", "").split()
        propres = []
        for v in valeurs:
            try:
                val = float(v)
                if val > 0:
                    propres.append(val)
            except:
                continue
        return propres

    def calculer_duree(m):
        if 1.00 <= m < 1.35:
            return round((m * 12.5) / 1.18)
        elif 1.35 <= m < 1.50:
            return round((m * 14.5) / 1.29)
        elif 1.51 <= m < 2.00:
            return round((m * 17) / 1.49)
        elif 2.00 <= m < 2.99:
            return round((m * 21) / 2.18)
        elif 3.00 <= m < 3.99:
            return round((m * 25) / 2.95)
        elif 4.00 <= m < 4.99:
            return round((m * 29) / 4.10)
        else:
            return round((m * 40) / 18.15)

    def calcul_heure(base_heure, multiplicateurs, dernier_tour):
        heure_actuelle = datetime.strptime(base_heure, "%H:%M:%S")
        résultats = []

        base_m = multiplicateurs[0]
        base_duree = calculer_duree(base_m)
        heure_actuelle += timedelta(seconds=base_duree)

        for i, multiplicateur in enumerate(multiplicateurs[1:]):
            duree_sec = calculer_duree(multiplicateur)
            résultats.append({
                "Tour": f"T{dernier_tour + i + 1}",
                "Multiplicateur": multiplicateur,
                "Heure Prédite": heure_actuelle.strftime("%H:%M:%S")
            })
            heure_actuelle += timedelta(seconds=duree_sec)

        return résultats

    # --- Execution ---
    if calculer:
        historique = extraire_valeurs(multiplicateurs_input)
        if len(historique) < 2:
            st.warning("⚠️ Vérifiez l’historique: angona diso format na tsy ampy.")
        else:
            try:
                résultats_df = calcul_heure(heure_input, historique, dernier_tour)
                st.success("✅ Résultat Hybride T+1 à T+20")
                for resultat in résultats_df:
                    st.markdown(f"**{resultat['Tour']}** ➤ **{resultat['Multiplicateur']}x** — 🕓 {resultat['Heure Prédite']}")
            except Exception as e:
                st.error(f"❌ Olana tamin'ny prediction: {e}")

else:
    st.warning("⚠️ Ampidiro ny anarana sy mot de passe.")
