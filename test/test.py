import os
import cv2
import pytest
from processor import process_image_file, process_video_file

# Paths for test files
TEST_IMAGE_PATH = "./test_data/test_image.png"
TEST_IMAGE_NO_FACE_PATH = "./test_data/test_no_face.jpg"
TEST_VIDEO_PATH = "./test_data/test_video.mp4"
OUTPUT_DIR = "./test_output"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


@pytest.fixture
def blur_strength():
    return 40


def test_process_image_file(blur_strength):
    """Test if image processing works correctly."""
    output_path = process_image_file(TEST_IMAGE_PATH, OUTPUT_DIR, blur_strength)

    # Check if the file was created
    assert os.path.exists(output_path), "Processed image was not saved."

    # Check if the output image can be read
    processed_img = cv2.imread(output_path)
    assert processed_img is not None, "Failed to read processed image."


def test_process_video_file(blur_strength):
    """Test if video processing works correctly."""
    output_path = process_video_file(TEST_VIDEO_PATH, OUTPUT_DIR, blur_strength)

    # Check if the file was created
    assert os.path.exists(output_path), "Processed video was not saved."

    # Check if the output video can be read
    cap = cv2.VideoCapture(output_path)
    ret, frame = cap.read()
    cap.release()

    assert ret, "Processed video cannot be read."


def test_process_image_no_face(blur_strength):
    """Test if image processing works correctly for images without faces."""
    output_path = process_image_file(TEST_IMAGE_NO_FACE_PATH, OUTPUT_DIR, blur_strength)

    # Check if the file was created
    assert os.path.exists(output_path), "Processed image was not save"
