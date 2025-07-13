import sys

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
#  check the input file extension is .m4a
extension = input_file_path.split(".")[-1]
filename = input_file_path[:-(len(extension) + 1)]
print(f'filename: {input_file_path}')

if extension != "m4a":
    print("Error: input file must be a .m4a file")
    sys.exit()
else:
    output_file_path = f"{filename}.wav"
    convert_m4a_to_wav(input_file_path, output_file_path)
