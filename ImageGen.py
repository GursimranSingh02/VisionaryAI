import random
import time
from io import BytesIO
from urllib.parse import quote

import requests
import streamlit as st
from PIL import Image


def fetch_image(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        st.error(f"Error fetching image: {e}")
        return None


width = 1024
height = 1024
seed = random.randint(0, 100)
model = "flux"

st.subheader("Image Generator")

prompt = st.text_input("Enter the prompt:")

if st.button("Generate Image"):
    prompt_text = prompt.strip()
    if not prompt_text:
        st.warning("Please enter a prompt.")
        st.stop()

    encoded_prompt = quote(prompt_text)
    url = (
        f"https://pollinations.ai/p/{encoded_prompt}"
        f"?width={width}&height={height}&seed={seed}&model={model}"
    )

    start_time = time.time()
    timer_placeholder = st.empty()

    image = None
    for _ in range(3):
        elapsed_time = time.time() - start_time
        timer_placeholder.write(f"Time elapsed: {elapsed_time:.2f} seconds")

        image = fetch_image(url)
        if image:
            break

        time.sleep(1)

    elapsed_time = time.time() - start_time
    timer_placeholder.write(f"Total time taken: {elapsed_time:.2f} seconds")

    if image:
        st.image(image, caption="Generated Image", use_container_width=True)
    else:
        st.error("Failed to generate image. Please try again.")
