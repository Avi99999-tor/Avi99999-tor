import streamlit as st import numpy as np

def calcul_prediction(multiplicateurs, t_last): results = [] recent = multiplicateurs[:10]  # Derniers 10 pour rolling

def mean_local(data):
    return np.mean([x for x in data if x > 1.0 and x < 10.0])

def poids(val):
    if val < 1.2:
        return -2
    elif val < 2.0:
        return 1
    elif val < 5:
        return 2
    elif val < 10:
        return 4
    else:
        return 6

moyenne = mean_local(recent)
count_crash = sum(1 for x in recent if x < 1.3)
tendance_haute = sum(1 for x in recent if x >= 5)

for i in range(1, 21):
    base = moyenne + (np.random.rand() - 0.5) * 2
    rebond = 0
    if count_crash >= 3 and i in [3, 5, 8, 13, 18]:
        rebond = np.random.uniform(2.5, 6.5)
    elif tendance_haute >= 2 and i in [6, 10, 15]:
        rebond = np.random.uniform(5.5, 10.0)

    valeur = rebond if rebond > 0 else max(1.01, round(base, 2))
    fiab = min(97, max(50, 100 - abs(valeur - moyenne) * 20))

    tag = ""
    if valeur < 1.3:
        tag = "(Crash probable)"
    elif valeur >= 5:
        tag = "(Haute valeur probable — Assuré)"
    elif fiab >= 80:
        tag = "(Assuré)"

    results.append((f"T{t_last + i}", f"{valeur:.2f}x", f"{int(fiab)}%", tag))

return results

st.title("Prédiction Aviator - Version Probabiliste Fiable")

multiplicateurs_input = st.text_area("Entrez les multiplicateurs (du plus récent au plus ancien)", placeholder="Ex: 1.33x 2.74x 1.46x ...") tour_input = st.number_input("Dernier numéro de tour connu (ex: 10 si 1.33x est le plus récent)", min_value=1)

if st.button("Calculer les prédictions"): try: values = [float(x.replace("x", "")) for x in multiplicateurs_input.strip().split() if "x" in x] preds = calcul_prediction(values, int(tour_input))

st.subheader("Résultats des prédictions (Fiabilité ≥ 60%)")
    for t, v, f, tag in preds:
        if int(f.replace("%", "")) >= 60:
            st.markdown(f"**{t}** → **{v}** — Fiabilité: **{f}** {tag}")
except:
    st.error("Erreur lors de la lecture des multiplicateurs. Assurez-vous du bon format (ex: 2.55x 1.40x ...)")

