import streamlit as st
import random
from datetime import datetime

# Fonction pour traiter les données historiques saisies et les convertir en une liste de flottants
def process_historical_input(historical_input):
    try:
        # Nettoyer l'entrée : enlever les caractères indésirables ou les espaces supplémentaires, et séparer par des espaces
        historical_data = [float(x.strip()) for x in historical_input.split() if x.strip()]
        return historical_data
    except ValueError as e:
        st.error(f"Erreur lors du traitement des données historiques : {e}")
        return []

# Fonction pour générer la prédiction basée sur les données historiques et la graine RNG
def generate_prediction(historical_data, seed_value):
    random.seed(seed_value)
    
    # Simuler la génération des chiffres à partir de la graine
    rng_digits = [random.randint(0, 9) for _ in range(len(historical_data))]
    
    # Logique pour générer une prédiction en fonction des données historiques et de la graine
    prediction = sum(historical_data) / len(historical_data)  # Juste un exemple simple
    return prediction, rng_digits

# Fonction pour analyser la tendance des données historiques
def analyze_trends(historical_data):
    if len(historical_data) < 4:
        return "Données insuffisantes pour analyser les tendances"
    
    # Simple analyse de tendance basée sur les dernières valeurs
    trend = "Croissante" if historical_data[-1] > historical_data[-2] else "Décroissante"
    return trend

# Structure de l'application Streamlit
st.title("Prédiction du jeu Aviator")

# Entrée de l'utilisateur pour les données historiques
historical_input = st.text_area("Entrez les données historiques", "1.39 2.00 1.52 1.52 3.49 10.00 5.00")  # Exemple d'entrée

# Traitement des données d'entrée
historical_data = process_historical_input(historical_input)

if historical_data:
    # Entrée de l'utilisateur pour la graine RNG
    seed_input = st.text_input("Entrez la graine RNG", "20250502")
    seed_value = int(seed_input)
    
    # Générer les prédictions
    prediction, rng_digits = generate_prediction(historical_data, seed_value)
    trend_prediction = analyze_trends(historical_data)
    
    # Affichage des résultats
    st.write(f"Prédiction de résultat : {prediction}")
    st.write(f"Chiffres RNG utilisés : {rng_digits}")
    st.write(f"Prédiction basée sur les tendances : {trend_prediction}")
    
    # Affichage des données historiques et de l'analyse
    st.write("Données historiques (derniers 4 tours) :", historical_data[-4:])
else:
    st.error("Veuillez entrer des données historiques valides.")
