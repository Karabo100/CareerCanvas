# execution instructions
# 1. terminal prompt: uvicorn main:app --reload --port 8001
# 2. go to http://localhost:8001/docs
# 3. upload audio from user and execute
# 4. should get response audio
# 5. if web application doesn't work use postman to send request


from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import os
import openai
import json
import requests

load_dotenv()  # take environment variables from .env.

openai.api_key = os.getenv("OPEN_AI_KEY")
openai.organization = os.getenv("OPEN_AI_ORG")
elevenlabs_key = os.getenv("ELEVENLABS_KEY")

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/talk")
async def post_audio(file: UploadFile):
    user_message = transcribe_audio(file)
    #print(user_message)
    chat_response = get_chat_response(user_message)
    #print(chat_response)
    audio_output = text_to_speech(chat_response)

    def iterfile():
        yield audio_output
    
    return StreamingResponse(iterfile(), media_type="audio/mpeg")



#Functions
def transcribe_audio(file):
    audio_file= open(file.filename, "rb")
    transcription = openai.audio.transcriptions.create(model="whisper-1",file= audio_file)
    #transcription = {"role": "user", "content": "Who won the world series in 2020?"}
    print(transcription)
    return transcription

def get_chat_response(user_message):
    messages = load_messages()
    messages.append( {"role": "user", "content": user_message.text})

    #send to chatgpt/openAI
    gpt_response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
        )
    
    parsed_gpt_response = gpt_response.choices[0].message.content

    #print(user_message)
    print(gpt_response)
    #save messages
    save_messages(user_message.text, parsed_gpt_response)

    return parsed_gpt_response

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
        messages.append({"role": "system", "content": "You are interviewing the user for a system designer position. Ask short questions that are relevant to a entry level system designer. Your name is Ben. The user is Angela. Keep responses under 50 words."})
    return messages

def save_messages(user_message, gpt_response):
    file = 'database.json'
    messages = load_messages()
    messages.append({"role": "user", "content": user_message})
    messages.append({"role": "assistant", "content": gpt_response})
    with open(file, 'w') as f:
        json.dump(messages, f)

def text_to_speech(text):
    #voice_id = 'bVMeCyTHy58xNoL34h3p'
    voice_id = 'CYw3kZ02Hs0563khs1Fj'
    body = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "similarity_boost": 0,
            "stability": 0,
            "style":0.5,
            "use_speaker_boost": True
        }
    }

    headers= {
        "Content-Type": "application/json",
        "accept": "audio/mpeg",
        "xi-api-key": elevenlabs_key
    }

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    try:
        response = requests.post(url, json=body, headers= headers)
        #print(response)
        #print("Response code:", response.status)
        if response.status_code == 200:
            return response.content
        else:
            print("text to speech went wrong")
    except Exception as e:
        print(e)

#Send in audio, and have it transcribed

#sent it to chatgpt and get response