import streamlit as st
import pandas as pd
import joblib
from src.predict import predict_next_round

# Configuration de la page
st.set_page_config(
    page_title="Aviator Prediction Expert",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Titre
st.title("Aviator Prediction Expert")

# Chargement du modèle entraîné
@st.cache_resource
def load_model(path: str):
    return joblib.load(path)

model = load_model('output/aviator_model.joblib')

# Chargement et traitement des données
@st.cache_data
def load_and_prepare_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Feature engineering minimal (adapter selon votre pipeline)
    df = df[df['multiplier'] > 1.0]
    df['decimal_part'] = (df['multiplier'] % 1) * 100
    df['mod_10'] = df['decimal_part'] % 10
    df['rolling_mean_5'] = df['multiplier'].rolling(window=5).mean()
    df['rolling_std_5'] = df['multiplier'].rolling(window=5).std()
    df['lag'] = df['multiplier'].shift(1)
    return df.dropna()

data = load_and_prepare_data('data/processed/processed_data.csv')

# Sidebar for prediction parameters
st.sidebar.header('Paramètres de prédiction')
window = st.sidebar.slider('Fenêtre rolling (rounds)', 5, 20, 10)
threshold = st.sidebar.slider('Seuil probabilité X5+', 0.5, 0.9, 0.7)
st.sidebar.markdown(
    "---
"
    "**Instructions**: Déplacez les sliders pour ajuster la fenêtre de calcul rolling et le seuil de décision."
)

# Bouton pour lancer la prédiction
if st.sidebar.button('Lancer prédiction'):
    proba, decision = predict_next_round(
        model=model,
        df=data,
        window=window,
        threshold=threshold
    )
    st.metric('Probabilité X5+ (%)', f"{proba*100:.1f}", delta=None)
    if decision:
        st.success('✅ Recommandation: Parier X5+')
    else:
        st.warning('❌ Recommandation: Ne pas parier')

# Affichage des dernières données
st.header('Chronique des dernières multiplications')
st.dataframe(data.tail(20)[['multiplier', 'decimal_part', 'mod_10']])
