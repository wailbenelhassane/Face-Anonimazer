# Face-Anonymizer

Face-Anonymizer is an application designed to anonymize faces in images and videos by applying a blur effect. This tool is useful for protecting the privacy of individuals in multimedia content.

## Features

- **Face anonymization in images**: Detects faces in images and applies a blur effect.
- **Face anonymization in videos**: Detects faces in videos and applies a blur effect to each frame.
- **Real-time webcam mode**: Allows for real-time face anonymization using the webcam.

## Requirements

- Python 3.7 or higher
- Libraries specified in `requirements.txt`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/Face-Anonymizer.git
   cd Face-Anonymizer
   Create a virtual environment (optional but recommended):
2. Create a virtual environment (optional but recommended):

source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`

3. Install the required dependencies using pip:

pip install -r requirements.txt

##Usage

1. **Graphical User Interface (GUI)**  
Launch the GUI application:  
`python gui.py`  
This will open a window where you can select an image, video, or start live webcam processing. The tool will automatically detect faces and apply the blur effect.

2. **Command Line Interface (CLI)**  
You can process images, videos, or webcam streams directly from the command line by specifying the appropriate options.

**Example: Image Processing**  
To process an image, use the following command:  
`python main.py --mode image --filePath path_to_image.jpg --output_dir output_directory`

**Example: Video Processing**  
To process a video, use the following command:  
`python main.py --mode video --filePath path_to_video.mp4 --output_dir output_directory`

**Example: Webcam Processing (Real-time)**  
To process live webcam video, use the following command:  
`python main.py --mode webcam --output_dir output_directory`

**Command Line Arguments:**
- `--mode`: Choose between image, video, or webcam modes.
- `--filePath`: Path to the image or video file (not needed for webcam mode).
- `--output_dir`: Directory where the processed file will be saved.
