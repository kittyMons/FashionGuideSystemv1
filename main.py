import streamlit as st
import openai
import base64
import requests
import google.generativeai as genai

# Configure API keys
genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
client = openai.OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

st.title("What's your outfit today?")

def ai_suggestion(items, occasion):
    prompt = f"You are a fashion assistant. Based on the following items and the occasion ({occasion}), suggest an outfit and provide feedback on the uploaded outfits:"

    # Call Gemini API for outfit suggestion
    gemini_response = genai.image2text(
        input=f"Based on the following items: {', '.join(items)} and the occasion: {occasion}, suggest an outfit.",
        model="gemini",
        max_length=200
    )

    response = gemini_response['text']
    return response

def encode_image(file_path):
    with open(file_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

uploaded_files = st.file_uploader("Upload pictures of clothes or accessories", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Display uploaded images in a horizontal row
if uploaded_files:
    columns = st.columns(len(uploaded_files))
    for column, uploaded_file in zip(columns, uploaded_files):
        bytes_data = uploaded_file.read()
        column.image(bytes_data, use_column_width=True)

occasion = st.text_input("Enter the occasion for which you need an outfit suggestion (e.g., coffee date)")

if st.button("Get Suggestion"):
    if uploaded_files and occasion:
        image_urls = [f"data:image/png;base64,{encode_image(file)}" for file in uploaded_files]
        suggestion = ai_suggestion(image_urls, occasion)
        st.write(suggestion)
    else:
        st.write("Please upload images and enter an occasion.")
