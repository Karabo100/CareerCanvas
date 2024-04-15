from openai import OpenAI
import streamlit as st
import fitz  # PyMuPDF
from fpdf import FPDF

# Initialize OpenAI client
client = OpenAI(api_key=("OPENAI_API_KEY"))

#create a wrapper function
def get_completion(prompt, model="gpt-3.5-turbo",):
    completion = client.chat.completions.create(
      model=model,
      messages=[
      {"role": "system", "content": "You are a skilled resume critique. Your task is to provide feedback on the resume. Highlight the strengths and weaknesses of the resume. Provide suggestions on how to improve the resume with examples."},
      {"role": "user", "content": prompt},
      ]
    )
    return completion.choices[0].message.content

#Using the function with user input
print("Welcome! This feature serves as your resume writing guide. Be specific with your prompt. Highlight your Education, Skills, Experience and Projects you have worked on. Our system will provide feedback on your resume.")
prompt = input("Enter a prompt: ")
response = get_completion(prompt)
print(response)

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size = 15)

pdf.cell(200, 10, txt = response, 
         ln = 1, align = 'L')

line = ""
cursor = 0
line_number = 1
line_size = 60
for char in response:
    if cursor < line_size:
        line+=char
        cursor+=1
    elif(cursor == line_size):
        print(f"{line_number}: {len(line)} {line}")
        pdf.cell(200, 10, txt = line, 
         ln = line_number, align = 'L')
        line = ""
        cursor = 0
        line_number+=1

    else:
        line = ""
        cursor = 0
print(f"{line_number}: {len(line)} {line}")
pdf.cell(200, 10, txt = line, 
         ln = line_number, align = 'L')
# create a cell
pdf.output("response.pdf") 

# Create a file uploader
uploaded_file = st.file_uploader("Please choose your pdf.", type="pdf")
pdf_text = ""
if uploaded_file is not None:
    #Load the PDF
    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    
    # Analyze the PDF
    for i in range(len(pdf)):
        page = pdf.load_page(i)
        text = page.get_text("text")
        pdf_text+=f"Content of Page {i+1}:"
        pdf_text+=text

    # Display the PDF text
    st.write(pdf_text)
    st.write(get_completion(pdf_text))




