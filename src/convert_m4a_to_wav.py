import sys
import os

from pydub import AudioSegment

def convert_m4a_to_wav(input_file_path, output_file_path):
    # Load the .m4a file
    audio = AudioSegment.from_file(input_file_path, format="m4a")

    # Export the audio to .wav format with 16kHz sample rate
    audio.export(output_file_path, format="wav", bitrate="16k", parameters=["-ar", "16000"])

# create usage function for --help and --h flags or incorrect input
def usage():
    print('This converts m4a files to wav files with a 16kHz sample rate')
    print("Usage: python convert_m4a_to_wav.py <input_file_path>")
    print("Example: python convert_m4a_to_wav.py input.m4a")
    sys.exit()

# check the number of arguments
if len(sys.argv) != 2:
    usage()

# get the input from the command line
input_file_path = sys.argv[1]

# Get the script directory (parent of src/)
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
audio_dir = os.path.join(script_dir, "audio_inputs")

# Extract filename components
basename = os.path.basename(input_file_path)
name_without_ext = os.path.splitext(basename)[0]
extension = os.path.splitext(basename)[1].lower()

print(f'Processing: {basename}')

if extension != ".m4a":
    print("Error: input file must be a .m4a file")
    sys.exit()
else:
    # Create output path in audio_inputs directory
    output_file_path = os.path.join(audio_dir, f"{name_without_ext}.wav")
    convert_m4a_to_wav(input_file_path, output_file_path)
    print(f'Converted to: {output_file_path}')
