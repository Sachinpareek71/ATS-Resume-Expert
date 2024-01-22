import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
from google import generativeai as genai

load_dotenv()  # Load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
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
Hey! Act like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of the tech field, software engineering, data science, 
data analysis, and big data engineering. Your task is to evaluate the resume based 
on the given job description. Consider that the job market is very competitive, 
and you should provide the best assistance for improving the resumes. 
Assign the percentage matching based on JD and the missing keywords with high accuracy.
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
"""

# Streamlit app
st.title("Smart ATS - Resume Evaluation Tool")
st.markdown("This tool helps you evaluate your resume using an advanced ATS model.")

# Project Description
st.header("Project Description")
st.markdown("""
The Smart ATS - Resume Evaluation Tool leverages Google's generative model (Gemini) to assess resumes based on a provided job description. 
It acts as an Application Tracking System (ATS), considering the competitive job market and providing valuable insights to improve resumes.

Upload your resume, paste the job description, and click 'Submit' to get a detailed evaluation, including percentage matching, missing keywords, and a profile summary.

Feel free to experiment with different job descriptions and resumes!
""")

# Input Fields
st.header("Resume Evaluation")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

# Display Results
if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        prompt = input_prompt.format(text=text, jd=jd)
        response = get_gemini_response(prompt)
        st.subheader("Gemini Response:")
        st.json(response)
