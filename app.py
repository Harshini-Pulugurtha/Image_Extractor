import streamlit as st
from PIL import Image
import pytesseract
import openai
import os

st.set_page_config(page_title="📝 Handwriting Explainer", layout="centered")
st.title("📷 Handwritten Image Explainer")


openai.api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Upload a handwritten note image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("🧠 Reading handwriting..."):
        extracted_text = pytesseract.image_to_string(image)

    st.subheader("📝 Extracted Text:")
    st.code(extracted_text)

    if extracted_text.strip():
        st.subheader("💬 Explanation:")
        with st.spinner("Thinking..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You explain handwritten text in a clear and simple way."},
                        {"role": "user", "content": f"Explain this handwritten note:\n\n{extracted_text}"}
                    ]
                )
                explanation = response["choices"][0]["message"]["content"]
                st.success(explanation)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Couldn't extract any text from the image. Try a clearer image.")
