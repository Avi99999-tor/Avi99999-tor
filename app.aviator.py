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

    # --- Fidirana angona ---
    multiplicateurs_input = st.text_area("📥 Ampidiro ny historique (ex: 1.21x 1.33x 12.66x ...)", 
                                         placeholder="1.21x 1.33x 12.66x 1.44x ...", height=150)

    dernier_tour = st.number_input("🔢 Numéro du dernier tour", min_value=1, value=123)
    heure_input = st.text_input("🕒 Heure du dernier tour (hh:mm:ss)", value="20:30:05")

    calculer = st.button("🔮 Lancer la prédiction")

    # --- Nettoyage des données ---
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

    # --- Calcul durée multiplicateur ---
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

    # --- Calcul Heure automatique ---
    def calcul_heure(base_heure, multiplicateurs, dernier_tour):
        heure_actuelle = datetime.strptime(base_heure, "%H:%M:%S")
        résultats = []

        # Calcul Heure T+1 depuis durée(base multiplicateur)
        base_m = multiplicateurs[0]
        base_duree = calculer_duree(base_m)
        heure_actuelle += timedelta(seconds=base_duree)

        for i, multiplicateur in enumerate(multiplicateurs[1:]):  # Dès T+1
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
            st.warning("⚠️ Ampidiro farafahakeliny 2 multiplicateurs (base + prédiction).")
        else:
            résultats_df = calcul_heure(heure_input, historique, dernier_tour)
            st.success("✅ Résultat Hybride T+1 à T+20")
            for resultat in résultats_df:
                st.markdown(f"**{resultat['Tour']}** ➤ **{resultat['Multiplicateur']}x** — 🕓 {resultat['Heure Prédite']}")

else:
    st.warning("⚠️ Cliquez sur 'Connexion' pour entrer votre code utilisateur.")
