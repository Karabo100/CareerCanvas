import io
import streamlit as st
import openai
from PyPDF2 import PdfReader

# Set up OpenAI API
openai.api_key = "OPENAI_API_KEY"

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to provide feedback using ChatGPT
def provide_feedback(text):
    prompt = "Review the following resume and provide feedback by improving it to meet ATS standards:\n" + text + "\n\nFeedback:"
    response = openai.Completion.create(
        engine="davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def main():
    st.title("Resume Feedback Tool")

    uploaded_file = st.file_uploader("Upload your resume in PDF format", type=["pdf"])

    if uploaded_file is not None:
        resume_text = extract_text_from_pdf(uploaded_file)
        st.write("Resume Content:")
        st.write(resume_text)

        if st.button("Get Feedback"):
            feedback = provide_feedback(resume_text)
            st.write("Feedback:")
            st.write(feedback)

if __name__ == "__main__":
    main()
