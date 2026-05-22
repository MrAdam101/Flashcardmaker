import streamlit as st
import random

st.set_page_config(page_title="Flashcard Generator", layout="wide")

# --------------------------------
# TITLE
# --------------------------------
st.title("Flashcard Generator")

# --------------------------------
# INPUT BOX
# --------------------------------
word_input = st.text_area(
    "Enter words (one word per line)",
    height=150,
    placeholder="Bread\nWater"
)

# --------------------------------
# GENERATE BUTTON
# --------------------------------
generate = st.button("Generate")

# --------------------------------
# COLORS
# --------------------------------
colors = [
    "#ff7a00",
    "#168ed4",
    "#2ecc71",
    "#e84393",
    "#9b59b6",
    "#f1c40f",
    "#e74c3c",
    "#00cec9",
]

# --------------------------------
# WORD LIST
# --------------------------------
words = []

if word_input.strip():
    words = [
        word.strip()
        for word in word_input.split("\n")
        if word.strip()
    ]

# --------------------------------
# RANDOM UNIQUE COLORS
# --------------------------------
if generate and len(words) > 0:
    card_colors = random.sample(colors, len(words))
else:
    card_colors = colors[:len(words)]

# --------------------------------
# CSS
# --------------------------------
st.markdown("""
<style>

.a4-page {
    width: 1123px;
    height: 794px;
    background: white;
    margin: 30px auto;
    padding: 40px;
    box-sizing: border-box;
}

.card-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 40px;
}

.flash-card {
    height: 620px;

    border: 8px solid;
    border-radius: 35px;

    background: white;
    box-sizing: border-box;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 55px;
    font-weight: bold;
    font-family: Arial;

    color: #222;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# SHOW 2 CARDS PER PAGE
# --------------------------------
for i in range(0, len(words), 2):

    html = '<div class="a4-page">'
    html += '<div class="card-grid">'

    page_words = words[i:i+2]
    page_colors = card_colors[i:i+2]

    for word, color in zip(page_words, page_colors):

        html += f"""
        <div class="flash-card" style="border-color:{color};">
            {word}
        </div>
        """

    html += "</div></div>"

    st.markdown(html, unsafe_allow_html=True)
