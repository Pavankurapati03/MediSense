import re
import os
from dotenv import load_dotenv
from PIL import Image
from phi.agent import Agent
from phi.model.google import Gemini
import streamlit as st
from phi.tools.duckduckgo import DuckDuckGo
from io import BytesIO
from pdf_generator import generate_pdf  # Import the PDF generation function
from text_to_speech import text_to_speech  # Import the new module
from translation import translate_text  # Import translation module


# Load environment variables from .env file
load_dotenv()

# Initialize session state for GOOGLE_API_KEY
if "GOOGLE_API_KEY" not in st.session_state:
    st.session_state.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Language mapping
LANGUAGE_MAPPING = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "French": "fr",
    "Spanish": "es"
}

with st.sidebar:
    st.title("Configuration")
    
    if not st.session_state.GOOGLE_API_KEY:
        st.error("API key not found. Please set it in the .env file.")
    else:
        st.success("API Key loaded successfully!")

    st.info(
        "This tool provides AI-powered analysis of medical imaging data using "
        "advanced computer vision and radiological expertise."
    )

    # Language selection dropdown for translation
    selected_language = st.selectbox(
        "Select Language for Translation",
        list(LANGUAGE_MAPPING.keys()),
        help="Choose the language for the output, speech, and PDF generation"
    )
    target_language = LANGUAGE_MAPPING[selected_language]

medical_agent = Agent(
    model=Gemini(
        api_key=st.session_state.GOOGLE_API_KEY,
        id="gemini-2.0-flash-exp"
    ),
    tools=[DuckDuckGo()],
    markdown=True
) if st.session_state.GOOGLE_API_KEY else None

if not medical_agent:
    st.warning("Please configure your API key in the sidebar to continue")

# Medical Analysis Query
query = """
You are a highly skilled medical imaging expert with extensive knowledge in radiology and diagnostic imaging. Analyze the patient's medical image and structure your response as follows:

### 1. Image Type & Region
- Specify imaging modality (X-ray/MRI/CT/Ultrasound/etc.)
- Identify the patient's anatomical region and positioning
- Comment on image quality and technical adequacy

### 2. Key Findings
- List primary observations systematically
- Note any abnormalities in the patient's imaging with precise descriptions
- Include measurements and densities where relevant
- Describe location, size, shape, and characteristics
- Rate severity: Normal/Mild/Moderate/Severe

### 3. Diagnostic Assessment
- Provide primary diagnosis with confidence level
- List differential diagnoses in order of likelihood
- Support each diagnosis with observed evidence from the patient's imaging
- Note any critical or urgent findings

### 4. Patient-Friendly Explanation
- Explain the findings in simple, clear language that the patient can understand
- Avoid medical jargon or provide clear definitions
- Include visual analogies if helpful
- Address common patient concerns related to these findings

### 5. Research Context
IMPORTANT: Use the DuckDuckGo search tool to:
- Find recent medical literature about similar cases
- Search for standard treatment protocols
- Provide a list of relevant medical links of them too
- Research any relevant technological advances
- Include 2-3 key references to support your analysis

Format your response using clear markdown headers and bullet points. Be concise yet thorough.
"""

def clean_analysis_text(text):
    preamble_pattern = r"^(Okay|I will|Let's|Analyzing).+"
    lines = text.split("\n")
    cleaned_lines = [line for line in lines if not re.match(preamble_pattern, line.strip())]
    return "\n".join(cleaned_lines)



# Frontend Style Customization
st.markdown(""" 
    <style> 
    .custom-title { 
        font-size: 46px; 
        text-align: center; 
        font-weight:bold; 
        font-family: Open Sans; 
        background: -webkit-linear-gradient(rgb(188, 12, 241), rgb(212, 4, 4)); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
    } 
    .title-container {
        text-align: center;
    }
    .span { 
        font-size: 42px; 
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div class="title-container">
        <p class='span'>🏥<span class='custom-title'>MediSense </span></p>
    </div>
    """, 
    unsafe_allow_html=True
)
st.write("Upload a medical image for professional analysis")

# Create containers for better organization
upload_container = st.container()
image_container = st.container()
analysis_container = st.container()
pdf_container = st.container()
audio_container = st.container()

with upload_container:
    uploaded_file = st.file_uploader(
        "Upload Medical Image",
        type=["jpg", "jpeg", "png", "dicom"],
        help="Supported formats: JPG, JPEG, PNG, DICOM"
    )

if uploaded_file is not None:
    with image_container:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            image = Image.open(uploaded_file)
            width, height = image.size
            aspect_ratio = width / height
            new_width = 500
            new_height = int(new_width / aspect_ratio)
            resized_image = image.resize((new_width, new_height))
            
            st.image(
                resized_image,
                caption="Uploaded Medical Image",
                use_container_width=True
            )
            
            analyze_button = st.button(
                "🔍 Analyze Image",
                type="primary",
                use_container_width=True
            )

    with analysis_container:
        if analyze_button:
            image_path = "temp_medical_image.png"
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("🔄 Analyzing image... Please wait."):
                try:
                    response = medical_agent.run(query, images=[image_path])
                    translated_text = translate_text(response.content, target_language)
                    st.markdown("### 📋 Analysis Results")
                    st.markdown("---")
                    st.caption(
                        "This AI-generated analysis provides informational insights based on the uploaded medical image. It is not a substitute for professional medical advice, diagnosis, or treatment. Because an AI can make mistakes.."
                    )

                    st.markdown(translated_text)
                    st.session_state.analysis_text = translated_text
                except Exception as e:
                    st.error(f"Analysis error: {e}")

    with pdf_container:
        if "analysis_text" in st.session_state:
            pdf_buffer = generate_pdf(st.session_state.analysis_text)
            st.download_button("📄 Download Analysis as PDF", data=pdf_buffer, file_name="Medical_Analysis_Report.pdf", mime="application/pdf")

    with audio_container:
        if "analysis_text" in st.session_state:
            audio_file = text_to_speech(st.session_state.analysis_text, target_language)
            st.markdown("### 🔊 Listen to the Analysis")
            st.audio(audio_file, format="audio/mp3")
            with open(audio_file, "rb") as f:
                st.download_button("🎙️ Download Speech", f, file_name="analysis_audio.mp3", mime="audio/mp3")

    

else:
    st.info("👆 Please upload a medical image to begin analysis")
