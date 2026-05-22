import streamlit as st
import random

st.set_page_config(page_title="Flashcard Generator", layout="wide")

st.title("Flashcard Generator")

word_input = st.text_area(
    "Enter words (one word per line)",
    height=150,
    placeholder="bread\nwater\ndog\ncat"
)

generate = st.button("Generate")

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

words = []

if word_input.strip():
    words = [word.strip() for word in word_input.split("\n") if word.strip()]

if generate and words:
    card_colors = random.sample(colors, len(words))
else:
    card_colors = colors[:len(words)]

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
    grid-template-columns: 1fr 1fr;
    gap: 40px;
}

.flash-card {
    height: 620px;
    border: 8px solid;
    border-radius: 35px;
    background: white;
    box-sizing: border-box;
    padding: 25px;

    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
}

.image-area {
    width: 100%;
    height: 470px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 80px;
    color: #ddd;
}

.word-area {
    width: 100%;
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    font-family: Arial;
    color: #222;
    padding-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

for i in range(0, len(words), 2):
    page_words = words[i:i + 2]
    page_colors = card_colors[i:i + 2]

    cards_html = ""

    for index in range(len(page_words)):
        word = page_words[index]
        color = page_colors[index]

        cards_html += (
            '<div class="flash-card" style="border-color:'
            + color
            + ';">'
            + word
            + '</div>'
        )

    page_html = (
        '<div class="a4-page">'
        '<div class="card-grid">'
        + cards_html +
        '</div>'
        '</div>'
    )

    st.markdown(page_html, unsafe_allow_html=True)
