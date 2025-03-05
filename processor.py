import cv2
import mediapipe as mp
import os


def process_image(img, face_detection, blur_strength):
    """Applies blur to detected faces in an image."""
    height, width, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    detections = face_detection.process(img_rgb).detections

    if detections:
        for detection in detections:
            bbox = detection.location_data.relative_bounding_box

            x1 = max(0, int(bbox.xmin * width))
            y1 = max(0, int(bbox.ymin * height))
            w = max(0, int(bbox.width * width))
            h = max(0, int(bbox.height * height))

            img[y1:y1 + h, x1:x1 + w, :] = cv2.blur(img[y1:y1 + h, x1:x1 + w], (blur_strength, blur_strength))

    return img


def process_image_file(input_path, output_dir, blur_strength):
    """Processes a single image file and saves the result."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File {input_path} does not exist.")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    mp_face_detection = mp.solutions.face_detection
    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        img = cv2.imread(input_path)
        img = process_image(img, face_detection, blur_strength)

        output_path = os.path.join(output_dir, os.path.basename(input_path))
        cv2.imwrite(output_path, img)

    return output_path


def get_video_codec(file_extension):
    """Returns the appropriate codec for a given video file extension."""
    codecs = {
        ".mp4": "mp4v",
        ".avi": "XVID",
        ".mov": "avc1",
        ".mkv": "X264",
        ".wmv": "WMV1",
    }
    return codecs.get(file_extension.lower(), "mp4v")


def process_video_file(input_path, output_dir, blur_strength):
    """Processes a video file and saves the result."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File {input_path} does not exist.")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_extension = os.path.splitext(input_path)[1]
    codec = get_video_codec(file_extension)

    mp_face_detection = mp.solutions.face_detection
    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        cap = cv2.VideoCapture(input_path)
        ret, frame = cap.read()

        if not ret:
            raise ValueError("Could not read the video.")

        frame_height, frame_width = frame.shape[:2]
        output_path = os.path.join(output_dir, os.path.basename(input_path))
        fourcc = cv2.VideoWriter_fourcc(*codec)
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 25
        output_video = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        while ret:
            frame = process_image(frame, face_detection, blur_strength)
            output_video.write(frame)
            ret, frame = cap.read()

        cap.release()
        output_video.release()

    return output_path


def process_webcam(blur_strength):
    """Starts the webcam and applies real-time face blurring."""
    mp_face_detection = mp.solutions.face_detection
    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open the camera")
            return

        print("Starting live webcam. Press 'q' to exit.")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not capture a frame.")
                break

            frame = process_image(frame, face_detection, blur_strength)
            cv2.imshow('Live Webcam - Press Q to Exit', frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        print("Camera closed.")
