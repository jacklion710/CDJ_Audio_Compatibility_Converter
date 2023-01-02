CDJ Audio Compatibility Converter
This is a Python script that converts audio files to the WAV format, removes non-WAV files, checks the validity of WAV files, converts the bit depth of audio files, and splits and trims audio files.

Requirements
Python 3
soundfile
pydub
struct
wave
subprocess

Usage
Set the directory containing the audio files by modifying the root_dir variable.
Run the desired functions in the script.

1) convert_to_wav() converts audio files to WAV format.
2) delete_non_wav_files() deletes all non-WAV files in the directory.
3) check_files() checks the validity of WAV files and returns a list of corrupt or damaged files.
4) convert_bit_depth() converts the bit depth of all audio files to the specified target_bit_depth.
5) downsample_audio() converts the sample rate to a target value
6) check_bit_depth() returns the bitdepth of every file
7) check_sample_rate() returns the sample rate of every file

Notes
The changes made by the script are destructive and cannot be undone. It is recommended to make backups of the audio files before using the script.
The script has been tested and is known to work correctly, but the author cannot accept responsibility for any lost or damaged data.
The script is licensed under the MIT License. Do not redistribute as your own work.
If you have any questions or issues, feel free to contact the author at jack.lion710@gmail.com.

Installation Download Python Download the latest version of Python from https://www.python.org/downloads/.

Install PyCharm (optional) We recommend downloading PyCharm from www.jetbrains.com/pycharm/download/.
