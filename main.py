'''
Title: CDJ Audio Compatibility Converter
Author: Jacob Leone aka Jack.lion - @jack.lion710@gmail.com
Linktree: linktr.ee/Jack.Lion

This work is licensed under the Creative Commons Attribution-NoDerivatives 4.0 International License. To view a copy of
this license, visit http://creativecommons.org/licenses/by-nd/4.0/.

PLEASE READ BEFORE USE!!
This is a destructive process meaning the changes it makes can not be undone. I would HIGHLY recommend making duplicates
of your target directory before using this to avoid unwanted changes or lost data. The code has been tested on my system
and works well for me but I can not accept responsibility for any lost or damaged data. Once you try the functions out
and are comfortable with the configuration you have, then you may feel free to commit your changes.

Description: The goal of this script is to prepare a directory tree of audio files for compatibility with Pioneer CDJ
Equipment. Each function is designed to work independently so feel free to comment out functions you don't wish to use
in the main program. You can even reorder them if you prefer. The default state is biased towards my preferences and the
full script is as conservative as possible meaning it reduces the data such as bitdepth and samplerate as much as
possible without affecting the audio quality. It is only compatible with WAV files currently. Any other types of audio
files will be converted into WAV types.

Functionality:
1) convert_to_wav() converts audio files to WAV format.
2) delete_non_wav_files() deletes all non-WAV files in the directory.
3) check_files() checks the validity of WAV files and returns a list of corrupt or damaged files.
4) convert_bit_depth() converts the bit depth of all audio files to the specified target_bit_depth.
5) downsample_audio() converts the sample rate to a target value
6) check_bit_depth() returns the bitdepth of every file
7) check_sample_rate() returns the sample rate of every file

Further instructions are listed in the main program
Feel free to modify this code to fit your needs or make contributions if you feel, Just don't redistribute as your own.
If you feel like your special case warrants attention, feel free to reach out at jack.lion710@gmail.com
'''

import os
import soundfile as sf
from pydub import AudioSegment
import struct
import wave
import subprocess

# Converts audio files into WAV type
def convert_to_wav(root_dir, verbose_permission=True):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file_path)[1]
            try:
                sf.SoundFile(file_path)
            except Exception as e:
                if isinstance(e, sf.SoundFileError):
                    # File is not a valid audio file
                    if file_extension in [".asd", ".alc", ".DS_Store"]:
                        # Automatically delete these file types
                        os.remove(file_path)
                    elif verbose_permission:
                        # Prompt user for permission to delete other file types
                        print(f"{file_path} is not a valid audio file. Do you want to delete it? (y/n)")
                        user_input = input()
                        if user_input.lower() == "y":
                            os.remove(file_path)
                    else:
                        # Automatically delete other file types without prompting
                        os.remove(file_path)
            else:
                if file_extension not in [".wav"]:
                    # Convert file to WAV
                    print(f"Converting {file_path} to WAV...")
                    sound = AudioSegment.from_file(file_path)
                    new_file_path = os.path.splitext(file_path)[0] + ".wav"
                    sound.export(new_file_path, format="wav")
                    os.remove(file_path)

# Delete all non-WAV files
def delete_non_wav_files(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if not file.endswith('.wav'):
                file_path = os.path.join(root, file)
                os.remove(file_path)

# Confirms whether the files are WAV, another type, or corrupt
def check_files(root_dir):
    corrupt_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if not file.endswith('.wav'):
                print(f'{file_path} is not a WAV file')
            else:
                try:
                    sf.SoundFile(file_path)
                except Exception as e:
                    print(f'{file_path} is corrupt or damaged: {e}')
                    corrupt_files.append(file_path)
    return corrupt_files

# Traverse the directory tree and convert all audio files bitdepth
def convert_bit_depth(root_dir, target_bit_depth):
    # Use os.walk() to loop through all the subdirectories in the tree
    for root, dirs, files in os.walk(root_dir):
        # Loop through all the files in the current directory
        for filename in files:
            # Check if the file is an audio file
            if filename.endswith(".mp3") or filename.endswith(".wav"):
                # Set the input and output filenames
                input_filename = os.path.join(root, filename)
                print(f"Converting {input_filename} to {target_bit_depth} bits")
                # Get the base name and extension of the input file
                filename, file_extension = os.path.splitext(input_filename)
                output_path = os.path.dirname(input_filename)
                output_filename = os.path.join(output_path, filename + "_converted" + file_extension)
                # Read the audio data from the input file
                data, samplerate = sf.read(input_filename)
                try:
                    # Write the audio data to the output file with the desired bit depth
                    sf.write(output_filename, data, samplerate, subtype=f'PCM_{target_bit_depth}')
                except TypeError as e:
                    if "No format specified" in str(e):
                        print(
                            f"Unable to write file {output_filename} because the format could not be determined from the file extension")
                        # Print an error message and continue with the next file
                        continue
                    else:
                        # If the error is not related to the format not being specified, re-raise the error
                        raise e
                # Delete the original file and rename the new file
                os.remove(input_filename)
                os.rename(output_filename, input_filename)

# Convert sample rate to a target value
def downsample_audio(root_dir, target_sample_rate):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.wav'):
                file_path = os.path.join(root, file)
                # Generate a new file name for the resampled file
                resampled_file_path = file_path + '.downsampled.wav'
                if os.path.exists(resampled_file_path):
                    os.remove(resampled_file_path)
                    print(f'Removed {resampled_file_path}')
                # Call the Sox command with the stderr stream redirected to the null device
                if subprocess.call(f'sox -r {target_sample_rate} -e unsigned -b 16 -c 1 "{file_path}" "{resampled_file_path}"', stderr=subprocess.DEVNULL) == 0:
                    os.replace(resampled_file_path, file_path)
                    print(f'Downsampled {file_path} to {target_sample_rate} Hz')
                else:
                    print(f'Error downsampling {file_path}')

# Check the bit depth of all WAV files in the root_dir directory
def check_bit_depth(root_dir):
    all_files_32bit = True
    failing_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.wav'):
                file_path = os.path.join(root, file)
                with sf.SoundFile(file_path) as f:
                    # Check the subtype of the WAV file
                    if f.subtype in ["PCM_32", "FLOAT"]:
                        all_files_32bit = False
                        failing_files.append(file_path)
    if all_files_32bit:
        print('All files are less than 32 bits')
    else:
        print('The following files have a bit depth of at least 32 bits:')
        for file in failing_files:
            print(file)

# Check the sample rate of all WAV files in the root_dir directory
def check_sample_rate(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.wav'):
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    # Read the RIFF header
                    riff_header = f.read(12)
                    if riff_header[:4] != b'RIFF':
                        raise ValueError('Not a RIFF file')
                    if riff_header[8:12] != b'WAVE':
                        raise ValueError('Not a WAVE file')

                    # Read the format chunk
                    fmt_chunk_header = f.read(8)
                    if fmt_chunk_header[:4] != b'fmt ':
                        raise ValueError('Not a format chunk')
                    fmt_chunk_size = struct.unpack('<I', fmt_chunk_header[4:8])[0]
                    fmt_chunk_data = f.read(fmt_chunk_size)
                    wFormatTag, nChannels, nSamplesPerSec, nAvgBytesPerSec, nBlockAlign, wBitsPerSample = struct.unpack('<HHIIHH', fmt_chunk_data[:16])

                    # Print the file name and its sample rate
                    print(f'{file}: {nSamplesPerSec} Hz')

'''
Main program
you can rearrange these functions below into any order you prefer, delete or comment our functions don't wish to use and
even add your own functionality.
'''
if __name__ == '__main__':

    # Set the directory where the audio files are located
    root_dir = r"C:/Users/Jake/Desktop/Breaks"

    # Set Variables
    target_bit_depth = 16  # Set desired bitdepth, CDJs support bit depths less than 32bits but 16bit is recommended
    target_sample_rate = 441000 # Set desired sample rate, 441000 is recommended

    # Operations convert the audio files to CDJ-compatible format
    convert_to_wav(root_dir)

    delete_non_wav_files(root_dir)

    check_files(root_dir)

    convert_bit_depth(root_dir, target_bit_depth)

    downsample_audio(root_dir, target_sample_rate)

    check_bit_depth(root_dir)

    check_sample_rate(root_dir)

    print("done")