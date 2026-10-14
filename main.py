import streamlit as st
import random
import base64
import html
from io import BytesIO
from openai import OpenAI
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader

st.set_page_config(page_title="Flashcard Generator", layout="wide")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Christmas Flashcard Generator")

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


def generate_image(word):
    prompt = f"""
    Create a cute cartoon illustration of "{word}"
    for a 5-year-old ESL student.

    Give the illustration a clear Christmas theme while
    keeping "{word}" immediately recognisable.

    Add simple festive details appropriate to the subject,
    such as a Santa hat, a red Christmas bow, or red and
    green decorations attached to the subject.

    Preserve the subject's main shape and defining features.
    Do not replace it with a different Christmas object.
    Avoid decorations that hide or confuse its meaning.

    One main subject only.
    No separate props.
    Transparent background.
    No background scene.

    No text.
    No letters.
    No words.
    No flashcard.
    No border.
    No frame.

    Centered composition.
    Entire subject visible.
    Bright festive colours.
    Cute kindergarten style.
    Simple, clean vector cartoon.
    """

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    return result.data[0].b64_json


def create_pdf(cards):
    buffer = BytesIO()
    page_width, page_height = landscape(A4)

    pdf = canvas.Canvas(
        buffer,
        pagesize=(page_width, page_height)
    )
    pdf.setTitle("Christmas Flashcards")

    margin = 28
    gap = 28
    card_width = (page_width - 2 * margin - gap) / 2
    card_height = page_height - 2 * margin

    for start in range(0, len(cards), 2):
        for index, card in enumerate(cards[start:start + 2]):
            x = margin + index * (card_width + gap)
            y = margin

            pdf.setStrokeColor(HexColor(card["color"]))
            pdf.setLineWidth(5)
            pdf.roundRect(
                x, y, card_width, card_height,
                radius=20,
                stroke=1,
                fill=0
            )

            image_bytes = base64.b64decode(card["image"])
            image = ImageReader(BytesIO(image_bytes))

            pdf.drawImage(
                image,
                x + 18,
                y + 110,
                width=card_width - 36,
                height=card_height - 130,
                preserveAspectRatio=True,
                anchor="c",
                mask="auto"
            )

            # Reduce the font size for longer words.
            font_size = 80
            while (
                pdf.stringWidth(
                    card["word"], "Helvetica-Bold", font_size
                ) > card_width - 36
                and font_size > 8
            ):
                font_size -= 1

            pdf.setFont("Helvetica-Bold", font_size)
            pdf.setFillColor(HexColor("#222222"))
            pdf.drawCentredString(
                x + card_width / 2,
                y + 42,
                card["word"]
            )

        pdf.showPage()

    pdf.save()
    return buffer.getvalue()


st.markdown("""
<style>
.a4-page {
    width: 100%;
    max-width: 1123px;
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
}
.image-area img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}
.word-area {
    width: 100%;
    text-align: center;
    font-size: clamp(24px, 5vw, 70px);
    font-weight: 900;
    font-family: 'Mountains of Christmas', cursive;
    color: #222;
    padding-bottom: 20px;
    overflow-wrap: anywhere;
}
</style>
""", unsafe_allow_html=True)


if generate:
    words = [
        word.strip()
        for word in word_input.splitlines()
        if word.strip()
    ]

    if not words:
        st.warning("Please enter at least one word.")
    else:
        new_cards = []
        progress = st.progress(0)

        try:
            with st.spinner("Creating your Christmas flashcards..."):
                palette = colors.copy()
                random.shuffle(palette)

                for index, word in enumerate(words):
                    new_cards.append({
                        "word": word,
                        "color": palette[index % len(palette)],
                        "image": generate_image(word)
                    })

                    progress.progress((index + 1) / len(words))

                pdf_bytes = create_pdf(new_cards)

            # Save completed results so downloading does not
            # trigger another round of image generation.
            st.session_state["cards"] = new_cards
            st.session_state["pdf_bytes"] = pdf_bytes

            st.success("Your flashcards are ready!")

        except Exception as error:
            st.error(f"Could not create the flashcards: {error}")

        finally:
            progress.empty()


if st.session_state.get("cards"):
    st.download_button(
        label="📥 Download Flashcards PDF",
        data=st.session_state["pdf_bytes"],
        file_name="christmas_flashcards.pdf",
        mime="application/pdf"
    )

    cards = st.session_state["cards"]

    for start in range(0, len(cards), 2):
        cards_html = ""

        for card in cards[start:start + 2]:
            safe_word = html.escape(card["word"])

            cards_html += (
                f'<div class="flash-card" '
                f'style="border-color:{card["color"]};">'
                '<div class="image-area">'
                f'<img src="data:image/png;base64,{card["image"]}" '
                f'alt="{safe_word}">'
                '</div>'
                f'<div class="word-area">{safe_word}</div>'
                '</div>'
            )

        st.markdown(
            '<div class="a4-page"><div class="card-grid">'
            + cards_html
            + '</div></div>',
            unsafe_allow_html=True
        )
          
