#This feature helps Peter craft his resume using Open AI API for text generation. The role of the system is to act as a resume writer specialized in resume for recent graduates.

from openai import OpenAI
client = OpenAI(api_key="OPENAI_API_KEY")

# Generate a text completion
def get_completion(prompt, model="gpt-3.5-turbo"):
  completion = client.chat.completions.create(
      model=model,
      messages=[
      {"role": "system", "content": "You are a talented resume writer specifically for recent graduates. Write a resume with the correct format that passes the Applicant Tracking System. There will be 4 sections: Education, Skills, Experience, and Projects. Craft the best resume."},
      {"role": "user", "content": prompt},
      ]
  )
  return completion.choices[0].message.content

#Using the function with user input
print("Welcome! This feature serves as your resume writing guide. Be specific with your prompt. Highlight your Education, Skills, Experience and Projects you have worked on. ")
prompt = input("Enter a prompt: ")
response = get_completion(prompt)
print(response)