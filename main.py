import cv2
import mediapipe as mp
import os


def process_img(img, face_detection, blur_strength):
    """Aplica desenfoque a las caras detectadas en una imagen."""
    H, W, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    out = face_detection.process(img_rgb)

    if out.detections:
        for detection in out.detections:
            bbox = detection.location_data.relative_bounding_box

            x1 = max(0, int(bbox.xmin * W))
            y1 = max(0, int(bbox.ymin * H))
            w = max(0, int(bbox.width * W))
            h = max(0, int(bbox.height * H))

            img[y1:y1 + h, x1:x1 + w, :] = cv2.blur(img[y1:y1 + h, x1:x1 + w], (blur_strength, blur_strength))

    return img


def process_image(file_path, output_dir, blur_strength):
    """Procesa una imagen y guarda el resultado."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    mp_face_detection = mp.solutions.face_detection
    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        img = cv2.imread(file_path)
        img = process_img(img, face_detection, blur_strength)

        output_path = os.path.join(output_dir, os.path.basename(file_path))
        cv2.imwrite(output_path, img)

    return output_path


def process_video(file_path, output_dir, blur_strength):
    """Procesa un video y guarda el resultado."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    mp_face_detection = mp.solutions.face_detection
    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        cap = cv2.VideoCapture(file_path)
        ret, frame = cap.read()

        if not ret:
            raise ValueError("Could not read the video.")

        frame_height = frame.shape[0] - (frame.shape[0] % 2)
        frame_width = frame.shape[1] - (frame.shape[1] % 2)
        output_path = os.path.join(output_dir, os.path.basename(file_path))
        output_video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MP4V'), 25, (frame_width, frame_height))

        while ret:
            frame = process_img(frame, face_detection, blur_strength)
            output_video.write(frame)
            ret, frame = cap.read()

        cap.release()
        output_video.release()

    return output_path

def process_webcam(blur_strength):
    """Inicia la webcam y aplica desenfoque en tiempo real a los rostros detectados."""
    mp_face_detection = mp.solutions.face_detection
    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open the camera")
            return

        print("Starting live camera detection. Press 'q' to exit.")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not capture a frame from the camera.")
                break

            frame = process_img(frame, face_detection, blur_strength)
            cv2.imshow('Live Webcam - Press Q to Exit', frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        print("Camera closed.")

