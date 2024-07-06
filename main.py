import streamlit as st
import pathlib as Path
import google.generativeai as genai
import base64  # Import the base64 module for encoding

# Configure the API key (replace with your actual API key)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Set up the model configuration
generation_config = {
    "temperature": 0.7,  # Increased for more creative suggestions
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 2048,  # Reduced for concise fashion advice
}

def encode_image(file):
  """
  This function encodes an uploaded image file to base64 format.

  Args:
    file: A Streamlit file uploader object containing the image data.

  Returns:
    A string containing the base64 encoded image data.
  """
  bytes_data = file.read()
  return base64.b64encode(bytes_data).decode('utf-8')

# Fashion Guider Prompt
system_prompt = """
As a seasoned fashion stylist with a keen eye for trends, you are tasked with analyzing an image and providing style advice. Consider the following aspects:

  1. Garment Analysis: Describe the clothing items in the image (style, color, etc.).
  2. Style Suggestions: Offer recommendations for complementary pieces or alternative outfits based on current trends and the user's potential preferences. 
  3. Occasion Suitability: Consider the formality of the event or situation depicted in the image and suggest appropriate attire if applicable.
  4. Confidence Boost: End with a positive and encouraging statement that empowers the user's personal style.

  Important Notes:
  
  1. User Preferences: While analyzing the image, consider incorporating any style preferences the user may have provided (e.g., favorite colors, preferred formality).
  2. Image Clarity: If image quality hinders analysis, acknowledge any limitations. 
  3. Disclaimer: Include a disclaimer stating, "This is for informational purposes only. Experiment and have fun expressing your unique style!"

  Please provide a response with these 4 headings and tailor your advice to the user's potential preferences. 
"""

# Create the Generative Model object
model = genai.GenerativeModel(
    model_name="gemini-pro-vision", generation_config=generation_config
)

# Page configuration
st.set_page_config(page_title="Fashion Advisor", page_icon=":dress:")

# Title
st.title("Fashion Advisor")

st.subheader("Get Styling Inspiration for Your Next Look!")

# Upload images section
uploaded_file = st.file_uploader(
    "Upload an image of your outfit or desired style",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True,
)

# Process uploaded images and generate styling advice (if any)
if uploaded_file:
    image_data = []
    for image in uploaded_file:
        # Encode image to base64 format using the encode_image function
        encoded_image = encode_image(image)
        image_data.append(encoded_image)

    submit_button = st.button("Get Styling Advice")

    if submit_button:
        image_parts = [
            {"mime_type": "image/jpeg", "data": data} for data in image_data
        ]

        prompt_parts = [image_parts, system_prompt]

        response = model.generate_content(prompt_parts)
        if response:
            st.title("Here's some styling advice based on your image(s):")
            st.write(response.text)
            st.write(
                "Disclaimer: This is for informational purposes only. Experiment and have fun expressing your unique style!"
            )

