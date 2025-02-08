# MediSense - AI-Powered Medical Image Analysis 🏥

MediSense is an AI-driven medical image analysis tool that provides professional insights on uploaded medical images. It utilizes **Gemini AI** for detailed analysis, supports **multi-language translations**, and offers **text-to-speech** functionality for improved accessibility. The project is designed to assist in **radiology-based diagnostics** and make medical insights more accessible to users.

---

## 🚀 Features

✅ **Medical Image Analysis** - Uses **Gemini AI** to analyze X-ray, MRI, CT, and ultrasound images.
✅ **Multi-Language Support** - Translates reports into multiple languages (English, Telugu, Hindi, Tamil, etc.).
✅ **PDF Report Generation** - Converts AI-generated medical insights into a downloadable PDF.
✅ **Text-to-Speech** - Converts analysis results into speech for better accessibility.
✅ **Real-Time Medical Research** - Fetches relevant research papers and diagnostic references via DuckDuckGo.
✅ **Streamlit Web App** - User-friendly interface for uploading images and receiving AI-powered insights.

---

## 📌 Tech Stack

- **Python** - Core programming language.
- **Streamlit** - For building the interactive web interface.
- **Gemini AI API** - For medical image analysis.
- **DuckDuckGo API** - For retrieving real-time medical research references.
- **Pillow (PIL)** - For image processing.
- **Google Translate API** - For multi-language translation.
- **Text-to-Speech API** - For voice-based output.
- **ReportLab** - For generating PDF reports.

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/MediSense.git
   cd MediSense
   ```

2. **Create a virtual environment (optional but recommended):**
   ```sh
   python -m venv env
   source env/bin/activate  # For Linux/macOS
   env\Scripts\activate  # For Windows
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Create a `.env` file in the root directory and add your Google API key:
     ```sh
     GOOGLE_API_KEY=your_google_api_key_here
     ```

5. **Run the Streamlit app:**
   ```sh
   streamlit run app.py
   ```

---

## 📸 How to Use

1. Upload a **medical image** (JPG, PNG, JPEG, DICOM).
2. Click **"Analyze Image"** to generate insights.
3. View the structured **AI-generated analysis**.
4. Download the report as a **PDF**.
5. Listen to the analysis via **text-to-speech**.
6. Optionally, translate results into your preferred language.

---

## 📜 File Structure

```
MediSense/
│-- app.py                # Main Streamlit application
│-- pdf_generator.py      # PDF report generation module
│-- text_to_speech.py     # Text-to-speech conversion module
│-- translation.py        # Language translation module
│-- requirements.txt      # Dependencies list
│-- .env                  # API keys
│-- README.md             # Documentation
```

---

## 🔗 Future Enhancements

- ✅ **Integration of more AI models** for enhanced diagnostics.
- ✅ **Speech recognition** for voice-based interactions.
- ✅ **Better UI/UX** improvements for a smoother experience.
- ✅ **Improved OCR support** for scanned medical documents.

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 📧 Contact

For any queries or collaborations, reach out at **pavankurapati0105@gmail.com** or connect on [LinkedIn](https://www.linkedin.com/in/pavankumar-kurapati/).

---

Give a ⭐ if you find this useful! 🚀

