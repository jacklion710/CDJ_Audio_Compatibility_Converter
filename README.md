CDJ Audio Compatibility Converter
This is a Python script that converts audio files to the WAV format, removes non-WAV files, checks the validity of WAV files, converts the bit depth of audio files, and splits and trims audio files.

Author
Jacob Leone aka Jack.lion - @jack.lion710@gmail.com

Linktree: linktr.ee/Jack.Lion

License
This work is licensed under the Creative Commons Attribution-NoDerivatives 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nd/4.0/

Warning
PLEASE READ BEFORE USE!! This is a destructive process, meaning the changes it makes can not be undone. It is HIGHLY recommended to make duplicates of your target directory before using this to avoid unwanted changes or lost data. The code has been tested on the author's system and works well, but the author cannot accept responsibility for any lost or damaged data. Once you try the functions out and are comfortable with the configuration you have, then you may feel free to commit your changes to the files.

Description
The goal of this script is to prepare a directory tree of audio files for compatibility with Pioneer CDJ
Equipment. Each function is designed to work independently so feel free to comment out functions you don't wish to use
in the main program. You can even reorder them if you prefer. The default state is biased towards my preferences and the
full script is as conservative as possible meaning it reduces the data such as bitdepth and samplerate as much as
possible without affecting the audio quality. It is only compatible with WAV files currently. Any other types of audio
files will be converted into WAV types.

Requirements
Python 3
soundfile
pydub
struct
wave
subprocess

Instructions
Further instructions are listed in the main program.

Usage
Set the directory containing the audio files by modifying the root_dir variable.
Run the desired functions in the script.

Functionality
1) convert_to_wav() converts audio files to WAV format.
2) delete_non_wav_files() deletes all non-WAV files in the directory.
3) check_files() checks the validity of WAV files and returns a list of corrupt or damaged files.
4) convert_bit_depth() converts the bit depth of all audio files to the specified target_bit_depth.
5) downsample_audio() converts the sample rate to a target value
6) check_bit_depth() returns the bitdepth of every file
7) check_sample_rate() returns the sample rate of every file

Modification and Contribution
Feel free to modify this code to fit your needs or make contributions if you feel they are necessary. Just don't redistribute as your own work. If you feel like your special case warrants attention, feel free to contact the author at jack.lion710@gmail.com.

Notes
The changes made by the script are destructive and cannot be undone. It is recommended to make backups of the audio files before using the script.
The script has been tested and is known to work correctly, but the author cannot accept responsibility for any lost or damaged data.
The script is licensed under the MIT License. Do not redistribute as your own work.
If you have any questions or issues, feel free to contact the author at jack.lion710@gmail.com.

Installation
Download Python
Download the latest version of Python from https://www.python.org/downloads/.
Install PyCharm (optional) We recommend downloading PyCharm from www.jetbrains.com/pycharm/download/.










