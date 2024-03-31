import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="OPENAI_API_KEY")

#create a wrapper function
def get_completion(prompt, model="gpt-3.5-turbo"):
  completion = client.chat.completions.create(
      model=model,
      messages=[
      {"role": "system", "content": "You are a talented resume writer specifically for recent graduates. Write a resume with the correct format that passes the Applicant Tracking System. There will be 4 sections: Education, Skills, Experience, and Projects. Craft the best resume."},
      {"role": "user", "content": prompt},
      ]
  )
  return completion.choices[0].message.content

#create out streamlit app
with st.form(key="chat"):
    prompt = st.text_input("Welcome! This feature serves as your resume writing guide. Be specific with your prompt. Highlight your Education, Skills, Experience and Projects you have worked on.")
    
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.write(get_completion(prompt))