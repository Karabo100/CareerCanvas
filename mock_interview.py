import streamlit as st 
from openai import OpenAI
import openai
import json
import os

openai.api_key = "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"

def load_messages():
    messages = []
    file = 'database.json'
    #if file is empty add context
    empty = os.stat(file).st_size == 0
    #if not empty loop through history and add to messages
    if not empty:
        with open(file) as db_file:
            data = json.load(db_file)
            for item in data:
                messages.append(item)
    else:
        messages.append({"role": "system", "content": "You are acting as an interviewer in order for users to do mock interviews. Give one question at a time and ask follow-up questions occasionally. Please ask what position the user is interviewing for at the start of the interview."})
    return messages

def save_messages(user_message, gpt_response):
    file = 'database.json'
    messages = load_messages()
    messages.append({"role": "user", "content": user_message})
    messages.append({"role": "assistant", "content": gpt_response})
    with open(file, 'w') as f:
        json.dump(messages, f)

def get_response(user_message, model="gpt-3.5-turbo"):
    messages = load_messages()
    messages.append( {"role": "user", "content": user_message})

    #send to chatgpt/openAI
    gpt_response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
        )
    
    parsed_gpt_response = gpt_response.choices[0].message.content

    #print(user_message)
    print(gpt_response)
    #save messages
    save_messages(user_message, parsed_gpt_response)

    return parsed_gpt_response


st.title('Mock Interview Chatbot')
st.write("Hi! I am a mock interview bot to help you practice on your future interviews.")
st.write("Please start with telling me your name!")

with st.form(key = "chat"):
    if 'widget' in st.session_state:
        st.session_state.my_text = st.session_state.widget
        st.session_state.widget = ""
    st.text_input("Enter your response:", key="widget")
    submitted = st.form_submit_button("Submit")
    if submitted:
        response = get_response(st.session_state.my_text)
        st.write(response)