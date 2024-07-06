import streamlit as st
import pathlib as Path
import google.generativeai as genai

genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])


# Set up the model
generation_config = {
  "temperature": 0.7,  # Increased for more creative suggestions
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 2048,  # Reduced for concise fashion advice
}

# Set page configuration
st.set_page_config(
    page_title="Outfit Suggestion App",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #C9A9A6;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Fashion Guider Prompt
system_prompt = """
As a seasoned fashion stylist with a keen eye for trends, you are tasked with analyzing an image and providing style advice considering the occasion provided by the user. Consider the following aspects:

  1. Garment Analysis: Describe the clothing items in the image (style, color, etc.).
  2. Style Suggestions: Offer recommendations for complementary pieces or alternative outfits based on current trends, the user's potential preferences, and the occasion.
  3. Occasion Suitability: Analyze the outfit's suitability for the provided occasion and suggest adjustments if necessary.
  4. Confidence Boost: End with a positive and encouraging statement that empowers the user's personal style.

  Important Notes:

  1. User Preferences: While analyzing the image, consider incorporating any style preferences the user may have provided (e.g., favorite colors, preferred formality).
  2. Image Clarity: If image quality hinders analysis, acknowledge any limitations.
 

  Please provide a response with these 4 headings and tailor your advice to the user's potential preferences and the occasion.
"""

model = genai.GenerativeModel(model_name="gemini-pro-vision", generation_config=generation_config)

# Title
st.title("Fashion Advisor ")

st.subheader("Get Styling Inspiration for Your Next Look!")

uploaded_file = st.file_uploader("Upload an image of your outfit or desired style", type=["png", "jpg", "jpeg"])
if uploaded_file:
  st.image(uploaded_file)

  # Get user input for occasion
  occasion_options = ("Casual", "Formal", "Work", "Party", "Date","Other")
  selected_occasion = st.selectbox("Select the occasion for this outfit:", occasion_options)

  submit_button = st.button("Get Styling Advice")

  if submit_button:
    image_data = uploaded_file.getvalue()

    image_parts = [
      {
        "mime_type": "image/jpeg",
        "data": image_data
      },
    ]

    prompt_parts = [
      image_parts[0],
      f"The occasion for this outfit is {selected_occasion}. ",
      system_prompt,
    ]

    response = model.generate_content(prompt_parts)
    if response:
      st.title("Here's some styling advice based on your image and occasion: ")
      st.write(response.text)
