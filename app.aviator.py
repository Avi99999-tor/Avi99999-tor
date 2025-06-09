import streamlit as st
from datetime import datetime, timedelta

# --- Configuration ---
st.set_page_config(page_title="🎯 Hybride Prediction Aviator by Mickael", layout="centered")
st.title("🇲🇬 🎯 Hybride Prediction Aviator by Mickael")

# --- Connexion cachée ---
login_expanded = st.expander("🔐 Connexion")
with login_expanded:
    username = st.text_input("👤 Nom utilisateur", value="", key="username")
    password = st.text_input("🔑 Code secret", type="password", value="", key="password")

# --- Vérification ---
if username == "261 Topexacte 1xbet" and password == "288612byTsell":
    st.success("✅ Connexion réussie!")

    # --- Interface Heure & Multiplicateurs ---
    multiplicateurs_input = st.text_area("📥 Ampidiro ny historique (ex: 1.21x 1.33x 12.66x ...)", 
                                         placeholder="1.21x 1.33x 12.66x 1.44x ...", height=150)

    dernier_tour = st.number_input("🔢 Numéro du dernier tour", min_value=1, value=552)
    heure_input = st.text_input("🕒 Heure du dernier tour (hh:mm:ss)", value="20:30:05")

    calculer = st.button("🔮 Lancer la prédiction")

    # --- Calcul durée multiplicateur ---
    def calcul_duree(multiplicateur):
        if 1.00 <= multiplicateur < 1.35:
            coefficient = 12.5
            base_duree = 1.18
        elif 1.35 <= multiplicateur < 1.50:
            coefficient = 14.5
            base_duree = 1.29
        elif 1.51 <= multiplicateur < 2.00:
            coefficient = 17
            base_duree = 1.49
        elif 2.00 <= multiplicateur < 3.00:
            coefficient = 21
            base_duree = 2.18
        elif 3.00 <= multiplicateur < 4.00:
            coefficient = 25
            base_duree = 2.95
        elif 4.00 <= multiplicateur < 5.00:
            coefficient = 29
            base_duree = 4.10
        elif 5.00 <= multiplicateur < 5.49:
            coefficient = 30
            base_duree = 5.00
        elif 5.50 <= multiplicateur < 5.99:
            coefficient = 31
            base_duree = 5.25
        elif 6.00 <= multiplicateur < 6.99:
            coefficient = 32
            base_duree = 6.00
        elif 7.00 <= multiplicateur < 7.99:
            coefficient = 33
            base_duree = 6.80
        elif 8.00 <= multiplicateur < 8.99:
            coefficient = 34
            base_duree = 7.50
        elif 9.00 <= multiplicateur < 15.99:
            coefficient = 36
            base_duree = 10.45
        else:
            coefficient = 40
            base_duree = 18.15

        duree = (multiplicateur * coefficient) / base_duree
        return round(duree) if duree % 1 < 0.80 else round(duree + 1)

    # --- Calcul Heure automatique ---
    def calcul_heure(base_heure, multiplicateurs, dernier_tour):
        heure_actuelle = datetime.strptime(base_heure, "%H:%M:%S")
        résultats = []
        
        for i, multiplicateur in enumerate(multiplicateurs):
            duree_sec = calcul_duree(multiplicateur)
            heure_actuelle += timedelta(seconds=duree_sec)
            résultats.append({
                "Tour": f"T{dernier_tour + i + 1}",
                "Multiplicateur": multiplicateur,
                "Heure Prédite": heure_actuelle.strftime("%H:%M:%S")
            })
        
        return résultats

    # --- Fanodinana ---
    if calculer:
        historique = [float(x) for x in multiplicateurs_input.replace(",", ".").split()]
        résultats_df = calcul_heure(heure_input, historique, dernier_tour)
        st.success("✅ Résultat Hybride T+1 à T+20")
        for resultat in résultats_df:
            st.markdown(f"**{resultat['Tour']}** ➤ **{resultat['Multiplicateur']}x** — 🕓 {resultat['Heure Prédite']}")

else:
    st.warning("⚠️ Cliquez sur 'Connexion' pour entrer votre code utilisateur.")
