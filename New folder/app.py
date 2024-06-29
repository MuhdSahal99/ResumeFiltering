import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv()  # Load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt = """
Hey, act like a skilled ATS (Application Tracking System) with a deep understanding of the tech field,
software engineering, data science, data analyst, and big data engineering. Your task is to evaluate the resume
based on the given job description. You must consider the job market is very competitive and you should provide 
the best assistance for improving the resumes. Assign the percentage matching based on the JD and provide a profile summary.
resume: {text}
description: {jd}

I want the response in the following format:
Job Description  Match: %
Profile Summary: ""
"""

# Streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_files = st.file_uploader("Upload Your Resumes", type="pdf", help="Please upload PDF files", accept_multiple_files=True)

submit = st.button("Submit")

if submit:
    if uploaded_files:
        for uploaded_file in uploaded_files:
            text = input_pdf_text(uploaded_file)
            prompt = input_prompt.format(text=text, jd=jd)
            response = get_gemini_response(prompt)
            st.subheader(f"Resume for {uploaded_file.name}")
            st.text(response)
