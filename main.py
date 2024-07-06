import streamlit as st
import pathlib as Path
import google.generativeai as genai

# Configure the API key
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

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F8F4F4;
        font-family: 'Arial', sans-serif;
    }
    .main-title {
        color: #3E3D3D;
        font-size: 3em;
        text-align: center;
        margin-bottom: 0.5em;
    }
    .sub-title {
        color: #3E3D3D;
        font-size: 1.5em;
        text-align: center;
        margin-bottom: 1em;
    }
    .upload-section {
        text-align: center;
        margin-bottom: 1.5em;
    }
    .occasion-section {
        text-align: center;
        margin-bottom: 1.5em;
    }
    .button-section {
        text-align: center;
    }
    .response-section {
        margin-top: 2em;
        padding: 1em;
        background-color: #FFF;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Fashion Guider Prompt
system_prompt = """
As a seasoned fashion stylist with a keen eye for trends, you are tasked with analyzing an image and providing style advice considering the occasion provided by the user. Consider the following aspects:

  1. Garment Analysis: Describe the clothing items in the image (style, color, etc.). Discuss the quality and fit of each piece, highlighting how well it complements the wearer.
  2. Style Suggestions: Offer recommendations for complementary pieces or alternative outfits based on current trends, the user's potential preferences, and the occasion. Include also what type of footwear that suitable.
  3. Occasion Suitability: Analyze the outfit's suitability for the provided occasion and suggest adjustments if necessary. Offer recommendations for adjustments to better suit the event's formality or theme.
  4. Confidence Boost: End with a positive and encouraging statement that empowers the user's personal style.
  5. Accessories: Analyze the outfit and suggest some accessories that can be wear to enhance user's preference. (belt / earrings / bangle / necklace etc)

The images that will upload is just the image of the cloths without the model. So only tell the user the aspects without saying about the model. Focus on the outfits.
"""

model = genai.GenerativeModel(model_name="gemini-pro-vision", generation_config=generation_config)

# Title
st.markdown('<h1 class="main-title">Fashion Advisor 👗</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="sub-title">Get Styling Inspiration for Your Next Look!</h2>', unsafe_allow_html=True)

# Upload Image
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload an image of your outfit or desired style", type=["png", "jpg", "jpeg"])
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    st.image(uploaded_file, use_column_width=True)

    # Get user input for occasion
    st.markdown('<div class="occasion-section">', unsafe_allow_html=True)
    occasion_options = ("Casual", "Formal", "Work", "Party", "Date", "Other")
    selected_occasion = st.selectbox("Select the occasion for this outfit:", occasion_options)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="button-section">', unsafe_allow_html=True)
    submit_button = st.button("Get Styling Advice")
    st.markdown('</div>', unsafe_allow_html=True)

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
            st.markdown('<div class="response-section">', unsafe_allow_html=True)
            st.markdown('<h2>Here\'s some styling advice based on your image and occasion:</h2>', unsafe_allow_html=True)
                st.write(response.text)
            st.markdown('</div>', unsafe_allow_html=True)

