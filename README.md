# ANI.PY

**Main.py** is a versatile Python script for converting video frames to JSON format and playing animations using various character sets. This project is ideal for developers and enthusiasts interested in multimedia processing and character-based animations.

## Features

- **Frame Extraction:** Extract frames from MP4 videos and save them as JPG files.
- **JSON Conversion:** Convert JPG frames to base64-encoded JSON format.
- **Character-based Animations:** Render animations using various character sets including Chinese, Russian, Japanese, Korean, Greek, French, and Italian.
- **Audio Playback:** Play accompanying audio files during the animation.

## Requirements

Ensure you have the following dependencies installed. You can use the provided `requirements.txt` for easy installation.

```sh
pip install -r requirements.txt
```

## Usage

Run the script and follow the prompts to perform various tasks.

```sh
python Main.py
```

### Main Menu Options

1. **Convert MP4 to JPG**
   - Enter the name of the video file (without extension). The frames will be saved in the `JPG` folder.
2. **Convert JPG to JSON**
   - Enter the folder name inside `JPG`. The converted JSON will be saved in the `Json` folder.
3. **Play Animation**
   - Enter the subfolder name inside `Json`. The script will load frames from the JSON file and display the animation.

## Detailed Instructions

### Extract Frames from MP4

1. Select option `[1] Use MP4 to JPG`.
2. Enter the video file name (without extension). The script will extract frames and save them in the `JPG` folder.

### Convert JPG to JSON

1. Select option `[2] Use JPG to Json`.
2. Enter the folder name inside `JPG`. The script will convert JPG frames to a JSON file in the `Json` folder.

### Play Animation

1. Select option `[3] Play Animation`.
2. Enter the subfolder name inside `Json` where the JSON file is located.
3. Choose whether to play sound and provide the sound file name if applicable.
4. Select the animation mode from various character sets.
5. Enter the desired FPS for the animation.

## Example

```sh
# Convert MP4 to JPG
Enter the name of the video file (without extension): example_video

# Convert JPG to JSON
Enter the folder name inside 'JPG': example_folder

# Play Animation
Enter the subfolder name inside 'Json': example_folder
Do you want sound? (Y/N): Y
Enter the full sound file name: example_sound.mp3
Select Animation Mode:
[1] Default
[2] Chinese
[3] Russian
[4] Japanese
[5] Korean
[6] Greek
[7] French
[8] Italian
Enter your choice: 1
Enter the FPS to run the animation: 15
```

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for more details.

---

This `README.md` should provide clear, professional documentation for your `Main.py` script. If you need further adjustments, feel free to let me know!
