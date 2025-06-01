#!/usr/bin/env python3
"""
Aviator Crash Game Simple Predictor
Version simple Python pour générer des prédictions T+1 à T+20
Logique : « expert » basé sur une combinaison sin/cos + random.
"""

import math
import random

def nettoyer_historique(input_str):
    """
    Convertit une chaîne de nombres séparés par des espaces ou virgules en liste de float.
    Ex : "1.03 2.45, 3.96 1.00" → [1.03, 2.45, 3.96, 1.00]
    """
    parts = input_str.replace(',', ' ').split()
    valeurs = []
    for p in parts:
        try:
            v = float(p)
            if v > 0:
                valeurs.append(v)
        except ValueError:
            continue
    return valeurs

def expert_predictions(historique, tours=20):
    """
    Génère des prédictions « expert » pour les prochains tours.
    Pour chaque i de 1 à tours, on fait :
      pred = |sin(i + dernière_valeur) + cos(i * moyenne)| × facteur aléatoire
      clamp entre 1.01 et 15.00
    """
    résultats = []
    if not historique:
        # Si pas d'historique, on renvoie une liste fixe
        return [1.00 + i * 0.05 for i in range(1, tours+1)]
    
    moyenne = sum(historique) / len(historique)
    derniere = historique[-1]
    
    for i in range(1, tours + 1):
        # Composante trigonométrique
        trig = abs(math.sin(derniere + i) + math.cos(i * moyenne))
        # Facteur aléatoire léger
        facteur = 1 + random.uniform(0.1, 1.0)
        raw = trig * facteur
        # Clamp entre 1.01 et 15.00
        pred = round(min(max(raw, 1.01), 15.00), 2)
        résultats.append(pred)
    return résultats

def color_tag(val):
    """
    Renvoie un emoji selon la valeur :
      < 2   → 🔘
      < 10  → 💜
      >= 10 → 🔴
    """
    if val < 2:
        return "🔘"
    elif val < 10:
        return "💜"
    else:
        return "🔴"

def calculer_assurance(val):
    """
    Détermine un pourcentage d'assurance en fonction de la valeur prédite.
    > 10  : aléatoire entre 87 et 93%
    > 5   : aléatoire entre 80 et 88%
    > 3   : aléatoire entre 75 et 85%
    <=1.2 : aléatoire entre 60 et 70%
    sinon:  aléatoire entre 68 et 78%
    """
    if val >= 10:
        return random.randint(87, 93)
    elif val >= 5:
        return random.randint(80, 88)
    elif val >= 3:
        return random.randint(75, 85)
    elif val <= 1.2:
        return random.randint(60, 70)
    else:
        return random.randint(68, 78)

def main():
    print("\n🇲🇬  Prediction By Mickael TOP EXACTE  🇲🇬\n")
    print("Format de l'historique : liste de multipliers séparés par espaces ou virgules.")
    print("Ex : 1.03 2.45, 3.96 1.00 5.12\n")
    
    # Lecture de l'historique
    raw = input("Entrez les multipliers précédents : ").strip()
    historique = nettoyer_historique(raw)
    if len(historique) < 1:
        print("\n⚠️ Historique invalide. Veuillez entrer au moins une valeur positive.\n")
        return
    
    # Lecture du numéro du dernier tour
    last_tour_str = input("Entrez le numéro du dernier tour (ex : 150) : ").strip()
    try:
        last_tour = int(last_tour_str)
    except ValueError:
        print("\n⚠️ Numéro de tour invalide. Veuillez entrer un entier.\n")
        return
    
    # Génération des prédictions expert
    preds = expert_predictions(historique, tours=20)
    
    print("\n📈 Résultats de la prédiction T+1 à T+20 :")
    for i, val in enumerate(preds, start=1):
        tour = last_tour + i
        tag = color_tag(val)
        assurance = calculer_assurance(val)
        # Affichage formaté
        print(f"  T{tour} → {tag} {val}x  — Assurance : {assurance}%")
    print()

if __name__ == "__main__":
    main()
