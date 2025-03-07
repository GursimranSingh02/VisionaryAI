import streamlit as st

st.set_page_config(page_title='VisionaryAI', page_icon='🤖')
st.title('VisionaryAI 🤖')

pages = {
    "Options": [
        st.Page("Chat.py", title="Start Chat 🤖"),
        st.Page("ImageGen.py", title="Generate Image 🖼️"),
    ]}

pg = st.navigation(pages)
pg.run()