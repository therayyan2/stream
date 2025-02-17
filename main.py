import google.generativeai as genai
import streamlit as st
import docx
import PyPDF2
import pandas as pd
# Set Your API-KEY into the variable
api_key = "AIzaSyAhE6JlMJSVkjyG2626_Sb39qvPJ2siiiw"
st.set_page_config("AI Chatbot")
st.header("Hey there! How can I help you?")
st.title("Chat with AI")

# Gemini API Key Set Karna
genai.configure(api_key=api_key)

# Model Initialize Karna
model = genai.GenerativeModel("gemini-pro")

# Sidebar me file uploader
uploaded_file = st.sidebar.file_uploader("Upload a file for summarization [PDF,Docx,txt,csv,etc] formats supported.")

# Prompt input lena
prompt = st.chat_input("Enter your prompt here...")
# if prompt has been given so generate response of prompt.
if prompt is not None:
    response = model.generate_content(prompt)
    st.subheader("AI Response:")
    st.write(response.text)

if uploaded_file is not None:
    text = None
    if uploaded_file:
        ext = uploaded_file.name.split(".")[-1].lower()
        if ext == "txt":
            text = uploaded_file.read().decode("utf-8", errors="ignore")
        elif ext == "pdf":
            text = "".join([p.extract_text() or "" for p in PyPDF2.PdfReader(uploaded_file).pages])
        elif ext == "docx":
            text = "".join(p.text for p in docx.Document(uploaded_file).paragraphs)
        elif ext == "csv":
            text = pd.read_csv(uploaded_file).to_string()
        else:
            st.error("⚠ Unsupported file format!")

        if text:
            st.subheader("File Summary")
            st.write(model.generate_content(f"Summarize this:\n\n{text}").text)