import streamlit as st
import os
from ocr_engine import extract_text
from image_utils import preprocess_image
from document_generator import create_word

st.set_page_config(page_title="Handwritten OCR to Word")
st.title("Handwritten Chemistry Notes to Word")

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

        st.image(path, caption=file.name, use_container_width=True)

        with st.spinner(f"Extracting text from {file.name}..."):
            processed = preprocess_image(path)
            text = extract_text(processed)

        extracted_texts.append(text)
        image_paths.append(path)

        st.subheader(f"Extracted text — {file.name}")
        st.text_area("", value=text, height=200, key=file.name)

    if st.button("Generate Word Document"):
        output_file = "chemistry_notes.docx"
        with st.spinner("Creating Word document..."):
            create_word(extracted_texts, image_paths, output_file)

        with open(output_file, "rb") as f:
            st.download_button(
                label="Download Word File",
                data=f,
                file_name=output_file
            )
