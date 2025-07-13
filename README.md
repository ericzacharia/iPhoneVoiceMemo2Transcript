# iPhone Voice Memo to Transcript

A command-line tool to convert iPhone voice memos (m4a files) to text transcriptions using OpenAI's Whisper model.

## Features

- Converts m4a audio files to wav format (16kHz sample rate)
- Transcribes audio using Whisper.cpp with multiple model options
- Organized output structure with separate folders for inputs and outputs
- Support for different Whisper models (medium.en, large-v3, large-v3-q5_0)
- Preserves original audio files in `audio_inputs/`
- Saves transcriptions with timestamps in `transcriptions/`

## Prerequisites

- Python 3.x with `pydub` installed
- [whisper.cpp](https://github.com/ggerganov/whisper.cpp) compiled and available at `/Users/eric/Desktop/2-Career/Projects/whisper.cpp/`
- At least one Whisper model downloaded in the whisper.cpp models directory

## Installation

1. Clone this repository:
```bash
git clone git@github.com:ericzacharia/iPhoneVoiceMemo2Transcript.git
cd iPhoneVoiceMemo2Transcript
```

2. Install Python dependencies:
```bash
pip install pydub
```

3. Ensure whisper.cpp is installed and compiled at the expected location

## Usage

Basic usage (uses medium.en model by default):
```bash
./create_transcript.sh "path/to/your/audio.m4a"
```

Using a specific model:
```bash
./create_transcript.sh "path/to/your/audio.m4a" large-v3
```

Available models:
- `medium.en` (default) - English-only, balanced speed/accuracy
- `large-v3` - Multilingual, highest accuracy
- `large-v3-q5_0` - Quantized large model, good balance

## Project Structure

```
iPhoneVoiceMemo2Transcript/
├── create_transcript.sh      # Main script
├── src/                      # Source code
│   ├── convert_m4a_to_wav.py # Audio converter
│   ├── app.py               # Application utilities
│   └── remove_timestamps.ipynb # Jupyter notebook for timestamp removal
├── audio_inputs/            # Input audio files (.m4a, .wav)
├── transcriptions/          # Output transcription files (.txt)
├── docs/                    # Documentation
└── whisper.cpp/            # Whisper.cpp installation (gitignored)
```

## Output

- Audio files are copied to `audio_inputs/` for preservation
- WAV conversions are saved alongside the original files
- Transcriptions are saved in `transcriptions/` with the same base filename
- Each transcription includes timestamps in the format `[HH:MM:SS.mmm --> HH:MM:SS.mmm]`

## Tips

- Drag and drop audio files onto the terminal to automatically paste the file path
- For best results with English audio, use the `medium.en` model
- For non-English or mixed language audio, use `large-v3`
- Longer audio files will take proportionally longer to process

## Troubleshooting

If you encounter errors:

1. Check that all file paths in the script match your system setup
2. Ensure whisper.cpp is properly compiled with your desired models downloaded
3. Verify that pydub is installed: `pip install pydub`
4. Make sure the script has execute permissions: `chmod +x create_transcript.sh`

## License

This project is open source. Feel free to modify and distribute as needed.