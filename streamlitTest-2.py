import streamlit as st 
from openai import OpenAI

client = OpenAI(api_key="MY-API-KEY-HERE") 

# create a wrapper function
def get_completion(prompt, model="gpt-3.5-turbo"):
  completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role": "system", "content": "You are an assistant in helping graduate students search for entry-level jobs and rotational programs"},
        {"role": "user", "content": "As a graduate student what are some rotational programs and entry-level jobs I can apply too?"},
        ]
      )
  return completion.choices[0].message.content

# create our streamlit app
with st.form(key = "chat"):
    prompt = st.text_input("What can I help you with today?") # TODO!
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write(get_completion(prompt))