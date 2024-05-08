#Done by Karabo Osenoneng
import io
import streamlit as st
import openai
from openai import OpenAI
from PyPDF2 import PdfReader
import re

# Set up OpenAI API
 
client = OpenAI(api_key="OPEN_AI_KEY")

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to provide feedback using ChatGPT
def get_completion(prompt, model="gpt-3.5-turbo"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role": "system", "content": "You are a talent career coach providing feedback on a resume. Please provide feedback on the resume as well as give recommendations on different career paths suited for that resume."}, 
        {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content


def resume_feedback():
    st.title("Resume Advice Tool")
    st.write("Welcome! This feature serves as your resume writing guide using AI. PLEASE BE CAUTIOUS: Remember to exclude sensitive and personal information on the PDF file you upload.")

    uploaded_file = st.file_uploader("Upload your resume in PDF format", type=["pdf"])

    if uploaded_file is not None:
        resume_text = extract_text_from_pdf(uploaded_file)
        st.write("Resume Content:")
        st.write(resume_text)
        
        # Check for personal information in the resume
        if re.search(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', resume_text) or re.search(r'\b[A-Za-z\s]+\b', resume_text) or re.search(r'\b\d{5}\b', resume_text) or "@" in resume_text:
            st.warning("Personal information detected in the resume. Please remove any emails, names, addresses, and @ symbols before uploading.")
        else:
            st.success("No personal information detected in the resume.")
        if st.button("Get Feedback"):
            feedback = get_completion(resume_text)  # Replaced provide_feedback with get_completion
            st.write("Feedback:")
            st.write(feedback)



if __name__ == "__main__":
    resume_feedback()

