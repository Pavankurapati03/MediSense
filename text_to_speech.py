from gtts import gTTS
import re

def clean_text_for_speech(text):
    """
    Remove markdown special characters and symbols from the text 
    before converting to speech.
    """
    text = re.sub(r'[*#_`\-]', '', text)  # Remove *, #, _, `, -
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)  # Remove Markdown links [text](url)
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

def text_to_speech(text, filename="analysis_audio.mp3"):
    """
    Convert cleaned text to speech and save as an MP3 file.
    """
    cleaned_text = clean_text_for_speech(text)
    tts = gTTS(text=cleaned_text, lang="en")
    tts.save(filename)
    return filename
