import streamlit as st
from google import generativeai as genai
from PIL import Image
import tempfile
import os

# 🌐 Initialize Gemini client
genai.configure(api_key="AIzaSyBgFM3UZxZYb5CV6W3EWsA_-DAxsC3AgUs")  # Replace with your actual Gemini API key
model = genai.GenerativeModel('gemini-1.5-flash')  # or 'gemini-pro-vision'

# 🎨 Page Configuration
st.set_page_config(page_title="Travel Advisor", page_icon="🌍", layout="centered")

# 🌟 Custom Style
st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
            padding: 2rem;
            border-radius: 10px;
        }
        .title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1F4E79;
            text-align: center;
        }
        .subtext {
            color: #555;
            text-align: center;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# 🚩 Header
st.markdown('<div class="main"><div class="title">🧭 Travel Advisor</div><div class="subtext">Upload an image of your destination and get a smart travel caption or tip!</div>', unsafe_allow_html=True)

# 📤 File Upload
uploaded_file = st.file_uploader("📸 Upload an image of your travel destination", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display the uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption="Your uploaded image", use_column_width=True)

    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        img.save(tmp.name)
        temp_path = tmp.name

    # Send image to Gemini
    with st.spinner("🧠 Thinking... generating travel advice..."):
        try:
            response = model.generate_content(
                [img, "Give a travel caption or tip for this place. Suggest activities, local food, or cultural insights."]
            )
            st.success("✅ Travel Advice Generated!")
            st.markdown(f"### 📝 Result:\n{response.text}")
        except Exception as e:
            st.error(f"❌ Failed to generate content: {e}")

    # Clean up temp file
    os.remove(temp_path)

# 📌 Footer
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("Made with ❤️ using [Streamlit](https://streamlit.io/) and Google Gemini")

