import streamlit as st
import base64
import google.generativeai as genai
from openai import OpenAI

client = OpenAI(api_key= st.secrets['OPENAI_API_KEY'])

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("What's your outfit today?")

def ai_suggestion(occasion,sysprompt):
  fashion_response = client.chat.completions.create(
      model="gpt-4o",
      messages=[{
          "role": "system",
          "content":sysprompt

      },
       {
          "role": "user",
          "content": occasion
      }],

      max_tokens=50

  )
 
  fashion = fashion_response.choices[0].message.content
  return fashion

def ai_suggestion(occasion, uploaded_images):
    prompt = f"You are a fashion assistant. Based on the following items and the occasion ({occasion}), suggest an outfit and provide feedback on the uploaded outfits ({uploaded_images}):"
    # Call Gemini API for outfit suggestion
    gemini_response = genai.chat(
        messages=[{"role": "user", "content": prompt}],
        model="gemini",
        max_tokens=40
    )

    response = gemini_response['choices'][0]['message']['content']
    return response

def encode_image(file):
    bytes_data = file.read()
    return base64.b64encode(bytes_data).decode('utf-8')

uploaded_files = st.file_uploader("Upload pictures of clothes or accessories", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Display uploaded images in a horizontal row
uploaded_images = []
if uploaded_files:
    columns = st.columns(len(uploaded_files))
    for column, uploaded_file in zip(columns, uploaded_files):
        bytes_data = uploaded_file.read()
        column.image(bytes_data, use_column_width=True)
        uploaded_images.append(f"data:image/png;base64,{encode_image(uploaded_file)}")

occasion = st.text_input("Enter the occasion for which you need an outfit suggestion (e.g., restaurant date)")

if st.button("Get Suggestion"):
    if occasion:
        suggestion = ai_suggestion(occasion, uploaded_images)
        st.markdown(suggestion)  # Display suggestion formatted with markdown
    else:
        st.write("Please enter an occasion.")
