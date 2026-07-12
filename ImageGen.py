import time
import base64
from io import BytesIO

import streamlit as st
from PIL import Image
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file to get the Google API key
load_dotenv()

st.subheader("Image Generator")

prompt = st.text_input("Enter the prompt:")
uploaded_file = st.file_uploader("Upload an image (optional for image-to-image)", type=["png", "jpg", "jpeg"])

if st.button("Generate Image"):
    prompt_text = prompt.strip()
    if not prompt_text:
        st.warning("Please enter a prompt.")
        st.stop()

    start_time = time.time()
    timer_placeholder = st.empty()
    timer_placeholder.write("Processing...")

    try:
        client = genai.Client()
        
        inputs = [
            {
                "type": "text",
                "text": prompt_text
            }
        ]
        
        # If the user uploads an image, include it in the input array as per the snippet
        if uploaded_file is not None:
            image_bytes = uploaded_file.read()
            mime_type = "image/png" if uploaded_file.name.lower().endswith("png") else "image/jpeg"
            inputs.append({
                "type": "image",
                "data": base64.b64encode(image_bytes).decode('utf-8'),
                "mime_type": mime_type
            })

        interaction = client.interactions.create(
            # model="gemini-3.1-flash-image",
            model="gemini-3.1-flash-lite-image",
            input=inputs,
        )

        generated_image_bytes = base64.b64decode(interaction.output_image.data)
        generated_image = Image.open(BytesIO(generated_image_bytes))

        elapsed_time = time.time() - start_time
        timer_placeholder.write(f"Total time taken: {elapsed_time:.2f} seconds")

        st.image(generated_image, caption="Generated Image", use_container_width=True)
    except Exception as e:
        elapsed_time = time.time() - start_time
        timer_placeholder.write(f"Total time taken: {elapsed_time:.2f} seconds")
        st.error(f"Failed to generate image. Please try again. Error: {e}")
