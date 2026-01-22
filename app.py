import streamlit as st
import os
from ocr_engine import extract_text
from image_utils import preprocess_image
from doc_generator import create_word

st.set_page_config(page_title="Handwritten OCR to Word")

st.title("🧪 Handwritten Chemistry Notes → Word")

uploaded_files = st.file_uploader(
    "Upload handwritten images",
    type=["jpg", "png", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    extracted_texts = []
    image_paths = []

    os.makedirs("uploads", exist_ok=True)

    for file in uploaded_files:
        path = f"uploads/{file.name}"
        with open(path, "wb") as f:
            f.write(file.getbuffer())

        processed = preprocess_image(path)
        text = extract_text(processed)

        extracted_texts.append(text)
        image_paths.append(path)

    if st.button("Generate Word Document"):
        output_file = "chemistry_notes.docx"
        create_word(extracted_texts, image_paths, output_file)

        with open(output_file, "rb") as f:
            st.download_button(
                label="📥 Download Word File",
                data=f,
                file_name=output_file
            )
