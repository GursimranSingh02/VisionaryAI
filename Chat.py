import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Gemini client (API key from .env)
client = genai.Client()

MODEL = "gemini-3-flash-preview"

# Streamlit UI
st.title("Chatbot with Image Analysis 🔍")

# User input
user_question = st.text_input("Enter your question:")

# Upload multiple images (max 5)
uploaded_files = st.file_uploader(
    "Upload up to 5 images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Store image parts
image_parts = []

# Display images and prepare them for Gemini
if uploaded_files:
    if len(uploaded_files) > 5:
        st.warning("You can only upload up to 5 images.")
    else:
        for file in uploaded_files:
            image_bytes = file.read()

            # Convert to Gemini Part
            image_part = types.Part.from_bytes(
                data=image_bytes,
                mime_type=file.type
            )

            image_parts.append(image_part)

            # Show image
            st.image(file, use_container_width=True)

# Button
if st.button("Get Response"):

    if not user_question and not image_parts:
        st.warning("Please enter a question or upload at least one image.")

    else:
        try:
            # Prepare contents
            contents = []

            if user_question:
                contents.append(user_question)

            if image_parts:
                contents.extend(image_parts)

            # Call Gemini API
            response = client.models.generate_content(
                model=MODEL,
                contents=contents
            )

            # Display response
            if response and response.text:
                st.subheader("Response:")
                st.write(response.text)
            else:
                st.error("No response received.")

        except Exception as e:
            st.error(f"Error: {str(e)}")