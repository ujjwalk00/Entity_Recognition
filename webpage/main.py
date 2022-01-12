import streamlit as st
import spacy
from spacy import displacy
import streamlit.components.v1 as components


nlp = spacy.load('en_core_web_lg')


# Create a page dropdown 
page = st.selectbox("Choose your page", ["Page 1", "Page 2", "Page 3"]) 
    # Display details of page 1elif page == "Page 2":
    # Display details of page 2elif page == "Page 3":
    # Display details of page 3


if page == "Page 1":
    st.write("My first app hello")
    sentence = st.text_input('Input your sentence here:') 
    article = nlp(sentence)
    st.write(*[(e.text, e.label_) for e in article.ents])
    html_text = displacy.render(article, style='ent')
    components.html(html_text,
    height=600
)


    


elif page == "Page 2":
    st.write("Page 2")
    label = "select a file please"
    st.file_uploader(label, type=None, accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None)


elif page == "Page 3":
    st.write("Page 3")
    sentence = st.text_input('Input your sentence here:') 
    st.write(sentence)









