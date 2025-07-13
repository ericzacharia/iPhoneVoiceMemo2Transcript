import os
import subprocess
import streamlit as st
from pydub import AudioSegment
import openai
from langchain_community.llms import Ollama
from io import BytesIO
from fpdf import FPDF
import markdown2

from llm_api_token import openai_api_key

# Function to save uploaded file
def save_uploaded_file(uploaded_file):
    if not os.path.exists("tempDir"):
        os.makedirs("tempDir", exist_ok=True)
    file_name = uploaded_file.name.replace(" ", "_")  # Replace spaces with underscores
    file_path = os.path.join("tempDir", file_name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def transcribe(wav_file_path):
    try:
        model_path = "./whisper.cpp/models/ggml-medium.en.bin"
        command = ["./whisper.cpp/main", "-m", model_path, "-f", wav_file_path, "-otxt"]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception(f"Error running whisper.cpp: {result.stderr.decode('utf-8')}")
        transcript_file = wav_file_path.replace(".wav", ".txt")
        fallback_transcript_file = wav_file_path + ".txt"
        if not os.path.exists(transcript_file):
            if os.path.exists(fallback_transcript_file):
                os.rename(fallback_transcript_file, transcript_file)
            else:
                raise FileNotFoundError(f"Transcript file {transcript_file} not found.")
        with open(transcript_file, "r") as f:
            transcript = f.read()
        return transcript
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


def convert_m4a_to_wav(input_file_path, output_file_path):
    audio = AudioSegment.from_file(input_file_path, format="m4a")
    audio.export(output_file_path, format="wav", bitrate="16k", parameters=["-ar", "16000"])


def summarize_transcript(transcript, style, model):
    openai.api_key = openai_api_key

    prompt = f"Summarize the following transcript in {style} style:\n{transcript}"
    if model == "GPT-4o":
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert financial advisor."},
                {"role": "user", "content": prompt},
            ],
        )
        summary = response["choices"][0]["message"]["content"].strip()
    else:
        if model == "Llama 3.1 8b":
            ollama_model = Ollama(model="llama3.1")
        elif model == "Llama 3.1 70b":
            ollama_model = Ollama(model="llama3.1:70b")
        response = ollama_model.invoke(prompt)
        summary = response.strip()
    return summary


def generate_download_file(content, file_format):
    if file_format == "pdf":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in content.split('\n'):
            pdf.cell(200, 10, txt=line, ln=True)
        pdf_output = BytesIO()
        pdf.output(pdf_output)
        return pdf_output.getvalue(), "application/pdf"
    
    elif file_format == "md":
        markdown_content = markdown2.markdown(content)
        return markdown_content.encode("utf-8"), "text/markdown"
    
    elif file_format == "doc":
        return content.encode("utf-8"), "application/msword"

    else:  # txt as default
        return content.encode("utf-8"), "text/plain"


# Streamlit App UI
st.title("Transcription and Summarization App")
st.write("Upload an audio (.m4a) or video (.mp4, .mov) file to get a transcript and summary.")

uploaded_file = st.file_uploader("Choose a file", type=["m4a", "mp4", "mov"])
model = st.radio("Select a Model", ("GPT-4o", "Llama 3.1 8b", "Llama 3.1 70b"))

if uploaded_file:
    input_file_path = save_uploaded_file(uploaded_file)
    wav_file_path = input_file_path.rsplit(".", 1)[0] + ".wav"
    convert_m4a_to_wav(input_file_path, wav_file_path)
    st.write("Transcribing audio...")
    transcript = transcribe(wav_file_path)

    if transcript:
        st.text_area("Transcript", transcript, height=300)
        summary_style = st.selectbox("Summary Style", ["Outline", "Paragraph"])
        summary = summarize_transcript(transcript, summary_style, model)
        st.text_area("Summary", summary, height=200)

        # File format selection
        transcript_download_format = st.selectbox("Download transcript as", ["txt", "md", "pdf", "doc"])
        summary_download_format = st.selectbox("Download summary as", ["txt", "md", "pdf", "doc"])

        # Generate download data for transcript
        transcript_data, transcript_mime = generate_download_file(transcript, transcript_download_format)
        st.download_button(
            label=f"Download Transcript as {transcript_download_format}",
            data=transcript_data,
            file_name=f"transcript.{transcript_download_format}",
            mime=transcript_mime
        )

        # Generate download data for summary
        summary_data, summary_mime = generate_download_file(summary, summary_download_format)
        st.download_button(
            label=f"Download Summary as {summary_download_format}",
            data=summary_data,
            file_name=f"summary.{summary_download_format}",
            mime=summary_mime
        )


# Add functionality to work with .mp4 files.
#  these were my terminal commands:
# ffmpeg -i TooLong.mp4 -q:a 0 -map a -ar 16000 TooLong.wav # combined command (.mp4 or .mov)
# ./main -m models/ggml-large-v3.bin -f TooLong.wav > TooLong_large.srt # transcribe the audio file
# ./main -m models/ggml-medium.en.bin -f TooLong.wav > TooLong_medium.srt # transcribe the audio file

"""
import re

def remove_srt_formatting(srt_file, output_file):
    with open(srt_file, 'r') as file:
        srt_content = file.read()

    # Remove SRT numbering, timestamps, and newlines between blocks
    cleaned_text = re.sub(r'\d+\n', '', srt_content)  # Remove block numbers
    cleaned_text = re.sub(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n', '', cleaned_text)  # Remove timestamps
    cleaned_text = re.sub(r'\n{2,}', '\n', cleaned_text)  # Remove extra newlines

    # Write the cleaned text to a file
    with open(output_file, 'w') as output:
        output.write(cleaned_text)

# Example usage
remove_srt_formatting('TooLong_large.srt', 'TooLong_large_transcript.txt')
"""
