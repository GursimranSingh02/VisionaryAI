import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import random
import time

def fetch_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        st.error(f"Error fetching image: {e}")
        return None


# prompt = 'A beautiful landscape'
width = 1024
height = 1024
# seed = 42 # Each seed generates a new image variation
seed = random.randint(0, 100)
model = 'flux' # Using 'flux' as default if model is not provided



st.subheader("Image Generator ✨")

prompt = st.text_input("Enter the prompt:")
url = f"https://pollinations.ai/p/{prompt}?width={width}&height={height}&seed={seed}&model={model}"


if st.button("Generate Image"):
    start_time = time.time()
    timer_placeholder = st.empty()
    
    while True:
        elapsed_time = time.time() - start_time
        timer_placeholder.write(f"Time elapsed: {elapsed_time:.2f} seconds")
        time.sleep(0.1)
        
        image = fetch_image(url)
        if image:
            break
    
    elapsed_time = time.time() - start_time
    timer_placeholder.write(f"Total time taken: {elapsed_time:.2f} seconds")
    # st.image(image, caption="Generated Image", use_column_width=True)
    st.image(image, caption="Generated Image", use_container_width=True)



