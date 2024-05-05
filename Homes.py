import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Home'
)
image = Image.open('logo.jpg')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# India Delivery')
st.sidebar.markdown('## Best delivery in town')
st.sidebar.markdown("""___""")

st.header('India Delivery Growth Dashboard')