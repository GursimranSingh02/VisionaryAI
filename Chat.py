import streamlit as st
from google import genai
import PIL.Image

# Set up Gemini API client (Replace with your actual API key)
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.subheader("Chatbot with Image Analysis 🔍")


# User input for question
user_question = st.text_input("Enter your question:", "")

# File uploader for images (Max 5 images)
uploaded_files = st.file_uploader("Upload up to 5 images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# Display uploaded images
images = []
if uploaded_files:
    if len(uploaded_files) > 5:
        st.warning("You can only upload up to 5 images.")
    else:
        for file in uploaded_files:  # Limit to 5 images
            img = PIL.Image.open(file)
            images.append(img)
            st.image(file, use_container_width=True)




# Button to process input
if st.button("Get Response"):
    if not user_question and not uploaded_files:
        st.warning("Please enter a question or upload at least one image.")
    else:
        # Call Gemini API
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[user_question] + images
        )

        # Display API Response
        if response and response.text:
            st.subheader("Response:")
            st.write(response.text)
        else:
            st.error("Failed to get a response from Gemini API.")

    
    



