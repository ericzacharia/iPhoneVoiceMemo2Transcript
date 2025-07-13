#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check for input file argument
if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
    echo "Instructions: Drag and drop the .m4a file onto the terminal, which will paste the path for you"
    echo ""
    echo "Usage: $0 <input_file_path.m4a> [model_name]"
    echo ""
    echo "Available models:"
    echo "  medium.en (default)"
    echo "  large-v3"
    echo "  large-v3-q5_0"
    echo ""
    echo "Example: $0 audio.m4a large-v3"

    exit 1
fi

input_file_path=$1
input_filename=$(basename "$input_file_path")
input_basename="${input_filename%.m4a}"

# Set model name - default to medium.en if not specified
if [ "$#" -eq 2 ]; then
    model_name=$2
else
    model_name="medium.en"
fi

projects_path="/Users/eric/Desktop/2-Career/Projects"

# echo the files this script will use and where they should be located
echo "This script will use the following files:"
echo "    Input: $1"
echo "    Converter: $SCRIPT_DIR/src/convert_m4a_to_wav.py"
echo "    Whisper: $projects_path/whisper.cpp/main"
echo "    Model: $projects_path/whisper.cpp/models/ggml-${model_name}.bin"
echo ""

# Create output directories if they don't exist
mkdir -p "$SCRIPT_DIR/audio_inputs"
mkdir -p "$SCRIPT_DIR/transcriptions"

# Copy input file to audio_inputs if it's not already there
if [[ "$input_file_path" != "$SCRIPT_DIR/audio_inputs/"* ]]; then
    cp "$input_file_path" "$SCRIPT_DIR/audio_inputs/"
    echo "Copied input file to audio_inputs/"
fi

# Set paths for processing
wav_file_path="$SCRIPT_DIR/audio_inputs/${input_basename}.wav"
txt_output_path="$SCRIPT_DIR/transcriptions/${input_basename}.txt"

# Step 1: Run python convert_m4a_to_wav.py 
python "$SCRIPT_DIR/src/convert_m4a_to_wav.py" "$input_file_path"

# Check if wav_file was created
if [ ! -f "$wav_file_path" ]; then
    echo "Error: $wav_file_path was not created."
    exit 1
fi

# Step 2: Run whisper.cpp/main and output to transcriptions folder
"$projects_path"/whisper.cpp/main -m "$projects_path"/whisper.cpp/models/ggml-${model_name}.bin -f "$wav_file_path" -of "$SCRIPT_DIR/transcriptions/${input_basename}"

echo ""
echo "Transcription completed! Output saved to: transcriptions/${input_basename}.txt"

