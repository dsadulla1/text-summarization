import streamlit as st
from summarizer import Summarizer
from bs4 import BeautifulSoup
from bs4.element import Comment
import requests, gc, re
from requests.exceptions import MissingSchema

st.title("Text Summarization")
st.write("This application can perform extractive text summariztion.")

def get_model():
    model = Summarizer('bert-base-uncased')
    return model

model = get_model()

Ratio = st.sidebar.slider("The ratio of sentences that you want for the final summary", min_value = 0.0, max_value = 1.0, value = 0.2)
Min_Length = st.sidebar.number_input("Remove sentences that are less than Min_Length", min_value = 20, max_value = 10000, value = 40)
Max_Length = st.sidebar.number_input("Remove sentences greater than the Max_length", min_value = 20, max_value = 10000, value = 1000)

url_link = st.text_input("Paste URL here..")
if url_link is not None:
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def text_from_html(body):
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)
        return " ".join(t.strip() for t in visible_texts)

    try:
        webpage = requests.get(url_link).text
    except MissingSchema as ms:
        webpage = None
    
    if webpage is not None:
        url_text = str(text_from_html(webpage))
        output = model(body = url_text, ratio = Ratio, min_length = Min_Length, max_length = Max_Length)
        st.markdown(output)

st.subheader("OR")

uploaded_file = st.file_uploader("Choose a file you would like to summarize", type=['txt'])
if uploaded_file is not None:
    file_input = uploaded_file.getvalue()
    output = model(body = file_input, ratio = Ratio, min_length = Min_Length, max_length = Max_Length)
    st.markdown(output)

st.subheader("OR")

inputtext = st.text_input("Paste text you would like to summarize.")
if inputtext is not None:
    output = model(body = inputtext, ratio = Ratio, min_length = Min_Length, max_length = Max_Length)
    st.markdown(output)

del model
gc.collect()