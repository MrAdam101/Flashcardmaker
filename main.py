import streamlit as st
import random

st.set_page_config(page_title="Flashcard Generator", layout="wide")

# -----------------------------
# PAGE TITLE
# -----------------------------
st.title("Flashcard Generator")

# -----------------------------
# WORD INPUT
# -----------------------------
word_input = st.text_area(
    "Enter words (one word per line)",
    height=150,
    placeholder="Bread\nWater\nApple\nCar"
)

# -----------------------------
# COLORS
# -----------------------------
colors = [
    "#ff7a00",
    "#168ed4",
    "#2ecc71",
    "#e84393",
    "#9b59b6",
    "#f1c40f",
    "#e74c3c",
    "#00cec9",
    "#6c5ce7",
    "#fd79a8",
    "#00b894",
    "#e17055"
]

# -----------------------------
# GENERATE BUTTON
# -----------------------------
generate = st.button("Generate")

# -----------------------------
# GET WORDS
# -----------------------------
words = []

if word_input.strip() != "":
    words = [word.strip() for word in word_input.split("\n") if word.strip()]

# -----------------------------
# RANDOM COLORS
# -----------------------------
if generate and len(words) > 0:
    card_colors = random.sample(colors, len(words))
else:
    card_colors = colors[:len(words)]

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>

.a4-page {
    width: 1123px;
    min-height: 794px;
    background: white;
    margin: 20px auto;
    padding: 35px;
    box-sizing: border-box;
}

.card-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 35px;
}

.flash-card {
    height: 340px;
    border: 8px solid;
    border-radius: 35px;
    background: white;
    box-sizing: border-box;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 48px;
    font-weight: bold;
    color: #222;
    font-family: Arial;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HTML
# -----------------------------
html = '<div class="a4-page"><div class="card-grid">'

for word, color in zip(words, card_colors):

    html += f"""
    <div class="flash-card" style="border-color:{color};">
        {word}
    </div>
    """

html += "</div></div>"

st.markdown(html, unsafe_allow_html=True)