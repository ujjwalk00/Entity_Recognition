import streamlit as st
from spacy import displacy
import streamlit.components.v1 as components
import pandas as pd
import en_core_web_lg
nlp = en_core_web_lg.load()



# Create a page dropdown 
#page = st.selectbox("Choose your page", ["Page 1", "Page 2", "Page 3"]) 
    # Display details of page 1elif page == "Page 2":
    # Display details of page 2elif page == "Page 3":
    # Display details of page 3


#if page == "Page 1":
label = "select a file please"
uploaded_file = st.file_uploader(label, type=None, accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None)
if uploaded_file:
    st.write("Filename: ", uploaded_file.name)
    filetype = uploaded_file.name.split(".")[-1]
    st.write("Filetype: ",filetype)
    if filetype == "xlsx":
        df = pd.read_excel("Assets//"+uploaded_file.name)
        st.dataframe(df)
        sentence = st.text_input('Input your sentence here:') 
        article = nlp(sentence)
        html_text = displacy.render(article, style='ent')
        components.html(html_text,
        height=600
        )


    
