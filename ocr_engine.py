import base64
import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["QWEN_API_KEY"],
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)

PROMPT = (
    "Extract all the handwritten text from this image exactly as written. "
    "Preserve the structure, headings, bullet points, and layout as much as possible. "
    "Do not summarize or interpret — just transcribe the text faithfully."
)

def extract_text(image_path):
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    ext = image_path.rsplit(".", 1)[-1].lower()
    mime = "image/png" if ext == "png" else "image/jpeg"

    response = client.chat.completions.create(
        model="qwen-vl-max",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{image_data}"}},
                    {"type": "text", "text": PROMPT},
                ],
            }
        ],
    )
    return response.choices[0].message.content
