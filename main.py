import streamlit as st
import pathlib as Path
import google.generativeai as genai

genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])


# Set up the model
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Fashion Guider Prompt
system_prompt = """
As a seasoned fashion stylist with a keen eye for trends, you are tasked with analyzing a user's outfit choices and recommending the most suitable one for a specific occasion. Consider the following aspects:

  1. Outfit Analysis: Describe the clothing items in each uploaded image (style, color, etc.).
  2. Occasion Suitability: Analyze the formality of the occasion provided by the user and suggest the outfit that best aligns with it. Provide reasoning for your recommendation.
  3. Enhancement Suggestions: Offer recommendations for complementary pieces or adjustments to enhance the chosen outfit.
  4. Confidence Boost: End with a positive and encouraging statement that empowers the user's personal style.

  Important Notes:
  
  1. User Preferences: While analyzing the images, consider incorporating any style preferences the user may have provided (e.g., favorite colors, preferred formality).
  2. Image Clarity: If image quality hinders analysis, acknowledge any limitations. 
  3. Disclaimer: Include a disclaimer stating, "This is for informational purposes only. Experiment and have fun expressing your unique style!"

  Please provide a response with these 4 headings and tailor your advice to the user's potential preferences and the chosen occasion. 
"""

model = genai.GenerativeModel(model_name="gemini-pro-vision", generation_config=generation_config, safety_settings=safety_settings)


# Page configuration
st.set_page_config(page_title="Outfit Advisor ", page_icon=":sunglasses:")

# Title
st.title("Outfit Advisor ")

st.subheader("Get Styling Inspiration and Pick the Perfect Outfit!")

# Upload multiple images
uploaded_images = st.file_uploader("Upload images of your outfit options", type=["png", "jpg", "jpeg"], accept_multiple=True)
if uploaded_images:
    for image in uploaded_images:
        st.image(image, caption=image.name)

# Occasion selection
occasion_options = ("Select Occasion", "Casual", "Formal", "Business Casual", "Special Event")
selected_occasion = st.selectbox("Select the occasion for your outfit:", occasion_options)

if uploaded_images and selected_occasion != "Select Occasion":
    submit_button = st.button("Get Styling Advice")

    if submit_button:
        image_data = []
        for image in uploaded_images:
            image_data.append({"mime_type": "image/jpeg", "data": image.getvalue()})

        prompt_parts = [
            image_data,
            system_prompt.format(occasion=selected_occasion.lower()),
        ]

        response = model.generate_content(prompt_parts)
        if response:
            st.title("Here's some styling advice based on your images: ")
            st.write(response.text)
