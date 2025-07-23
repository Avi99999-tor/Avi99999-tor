import streamlit as st
from PIL import Image
import pytesseract
import re

# Function to extract the last digit after the decimal
def extract_decimal_digit(odd_str):
    match = re.search(r"\d+\.(\d)", odd_str)
    if match:
        return match.group(1)
    return None

# OCR processing for Over & Under
def process_image(image):
    text = pytesseract.image_to_string(image)
    odds = re.findall(r"\d+\.\d+", text)
    if len(odds) >= 2:
        over = extract_decimal_digit(odds[0])
        under = extract_decimal_digit(odds[1])
        return over, under
    return None, None

# Streamlit Interface
st.set_page_config(page_title="Mod 10 Matcher", layout="centered")
st.title("⚽️ Match Comparator — Mod 10 stratégie")
st.markdown("**Ampidiro captures d'écran match 1 sy match 2 misy Over sy Under 1.5.**")

col1, col2 = st.columns(2)
with col1:
    img1 = st.file_uploader("📥 Capture Match 1", type=["png", "jpg", "jpeg"])
with col2:
    img2 = st.file_uploader("📥 Capture Match 2", type=["png", "jpg", "jpeg"])

if img1 and img2:
    over1, under1 = process_image(Image.open(img1))
    over2, under2 = process_image(Image.open(img2))

    if over1 and under1 and over2 and under2:
        mod1 = over1 + under1
        mod2 = over2 + under2

        st.markdown("---")
        st.subheader("🔎 Résultats")
        st.write(f"🎯 Match 1 Mod10 : {mod1}")
        st.write(f"🎯 Match 2 Mod10 : {mod2}")

        if mod1 == mod2:
            st.success(f"✅ Résultat ==== {mod1} match 1, {mod2} match 2")
            st.markdown("➡️ *Ohatra*: Fulham vs Chelsea = Arsenal vs Brighton")
        else:
            st.error("❌ Tsy mitovy ny résultat — Mampidira match hafa azafady.")
    else:
        st.warning("⚠️ Tsy nahazo tsara Over/Under ny OCR. Hamarino ny sary.")
else:
    st.info("🔄 Miandry ny sary roa ho alefa...")
