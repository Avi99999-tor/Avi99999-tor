import streamlit as st
from datetime import datetime, timedelta
from PIL import Image
import numpy as np
import easyocr

# --- Configuration ---
st.set_page_config(page_title="🎯 Hybride Prediction Aviator by Mickael", layout="centered")
st.title("🇲🇬 🎯 Hybride Prediction Aviator by Mickael")

# --- Interface de Connexion ---
st.markdown("## 🔐 Connexion")
username = st.text_input("👤 Nom utilisateur")
password = st.text_input("🔑 Code secret", type="password")

if username == "admin" and password == "1234":
    st.success("✅ Connexion réussie!")

    # --- Upload OCR Image ---
    st.markdown("### 📸 Upload image misy historique")
    uploaded_image = st.file_uploader("🖼️ Ampidiro capture de l'historique", type=["png", "jpg", "jpeg"])

    if uploaded_image is not None:
        try:
            image = Image.open(uploaded_image)
            st.image(image, caption="🖼️ Sary nampidirina", use_column_width=True)

            reader = easyocr.Reader(['en'], gpu=False)
            result = reader.readtext(np.array(image), detail=0)
            texte_ocr = " ".join(result)

            st.session_state['ocr_result'] = texte_ocr
            st.success("✅ OCR vita: texte nivoaka avy amin'ny image")
            st.text_area("📜 Résultat OCR (azo ovaina raha ilaina)", 
                         value=texte_ocr, height=100, key="ocr_result_affichage")

        except Exception as e:
            st.error(f"❌ OCR Error: {e}")

    # --- Fidirana angona texte manokana ---
    multiplicateurs_input = st.text_area(
        "📥 Ampidiro ny historique (ex: 1.21x 1.33x 12.66x ...)",
        value=st.session_state.get("ocr_result", ""),
        placeholder="1.21x 1.33x 12.66x 1.44x ...", height=150
    )

    dernier_tour = st.number_input("🔢 Numéro du dernier tour", min_value=1, value=123)
    heure_input = st.text_input("🕒 Heure du dernier tour (hh:mm:ss)", value="20:30:05")
    calculer = st.button("🔮 Lancer la prédiction")

    # --- Fonctions de traitement ---
    def extraire_valeurs(texte):
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
            st.warning("⚠️ Ampidiro farafahakeliny 2 multiplicateurs.")
        else:
            try:
                résultats_df = calcul_heure(heure_input, historique, dernier_tour)
                st.success("✅ Résultat Hybride T+1 à T+20")
                for resultat in résultats_df:
                    st.markdown(f"**{resultat['Tour']}** ➤ **{resultat['Multiplicateur']}x** — 🕓 {resultat['Heure Prédite']}")
            except Exception as e:
                st.error(f"❌ Olana tamin'ny prediction: {e}")

else:
    st.warning("⚠️ Mba ampidiro ny anarana sy mot de passe.")
