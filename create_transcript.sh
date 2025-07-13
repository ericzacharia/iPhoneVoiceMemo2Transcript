#!/bin/bash

# Check for input file argument
if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
    echo "Instructions: Drag and drop the .m4a file (from downloads folder?) onto the terminal, which will paste the path for you"
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

# Set model name - default to medium.en if not specified
if [ "$#" -eq 2 ]; then
    model_name=$2
else
    model_name="medium.en"
fi

projects_path="/Users/eric/Desktop/2-Career/Projects"

# echo the files this script will use and where they should be located
echo "This script will use the following files:"
echo "    $1"
echo "    /Users/eric/Desktop/2-Career/Projects/m4a2wav/convert_m4a_to_wav.py"
echo "    /Users/eric/Desktop/2-Career/Projects/whisper.cpp/main"
echo "    /Users/eric/Desktop/2-Career/Projects/whisper.cpp/models/ggml-${model_name}.bin"
echo "If these files are not in the correct location, please move them and try again."
echo ""

# Replace .m4a with .wav for output filename
wav_file_path="${input_file_path%.m4a}.wav"

# Step 1: Run python convert_m4a_to_wav.py 
python convert_m4a_to_wav.py "$input_file_path"

# Check if wav_file was created
if [ ! -f "$wav_file_path" ]; then
    echo "Error: $wav_file_path was not created."
    exit 1
fi

# Step 2: Run whisper.cpp/main from projects_path
"$projects_path"/whisper.cpp/main -m "$projects_path"/whisper.cpp/models/ggml-${model_name}.bin -f "$wav_file_path" -otxt

