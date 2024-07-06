import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Configure API keys
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
    page_title="Fashion Advisor",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for background color and other styles
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f8f5f2;
        color: #2c3e50;
    }
    .title {
        font-size: 3em;
        color: #34495e;
        text-align: center;
        margin-top: 20px;
    }
    .subheader {
        font-size: 1.5em;
        color: #7f8c8d;
        text-align: center;
        margin-top: -10px;
    }
    .file-uploader {
        margin-top: 20px;
    }
    .selectbox {
        margin-top: 20px;
    }
    .button {
        margin-top: 20px;
        display: flex;
        justify-content: center;
    }
    .result {
        margin-top: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Fashion Guider Prompt
system_prompt = """
As a seasoned fashion stylist with a keen eye for trends, you are tasked with analyzing an image and providing style advice considering the occasion provided by the user. Consider the following aspects:

  1. Garment Analysis: Describe the clothing items in the image (style, color, etc.). Discuss the quality and fit of each piece, highlighting how well it complements the wearer.
  2. Style Suggestions: Offer recommendations for complementary pieces or alternative outfits based on current trends, the user's potential preferences, and the occasion.
  3. Occasion Suitability: Analyze the outfit's suitability for the provided occasion and suggest adjustments if necessary. Offer recommendations for adjustments to better suit the event's formality or theme.
  4. Confidence Boost: End with a positive and encouraging statement that empowers the user's personal style.

  Please provide a response with these 4 headings and tailor your advice to the user's potential preferences and the occasion.
"""

model = genai.GenerativeModel(model_name="gemini-pro-vision", generation_config=generation_config)

# Title
st.markdown('<div class="title">Fashion Advisor</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Get Styling Inspiration for Your Next Look!</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload an image of your outfit or desired style", type=["png", "jpg", "jpeg"], className="file-uploader")
if uploaded_file:
    # Display uploaded image
    image = Image.open(io.BytesIO(uploaded_file.getvalue()))
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Get user input for occasion
    occasion_options = ("Casual", "Formal", "Work", "Party", "Date", "Other")
    selected_occasion = st.selectbox("Select the occasion for this outfit:", occasion_options, className="selectbox")

    submit_button = st.button("Get Styling Advice", className="button")

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
            st.markdown('<div class="result"><h2>Here\'s some styling advice based on your image and occasion:</h2></div>', unsafe_allow_html=True)
            st.write(response.text)

