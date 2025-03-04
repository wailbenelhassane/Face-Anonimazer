import cv2
import mediapipe as mp
import argparse
import os

def process_img(img, face_detection):
    H, W, _ = img.shape

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    out = face_detection.process(img_rgb)

    if out.detections is not None:
        for detection in out.detections:
            location_data = detection.location_data
            bbox = location_data.relative_bounding_box

            x1, y1, w, h = bbox.xmin, bbox.ymin, bbox.width, bbox.height

            x1 = int(x1 * W)
            y1 = int(y1 * H)
            w = int(w * W)
            h = int(h * H)

            # blur faces
            img[y1:y1 + h, x1:x1 + w, :] = cv2.blur(img[y1:y1 + h, x1:x1 + w], (50, 50))
    return img

args = argparse.ArgumentParser()
args.add_argument("--mode", default="image")
args.add_argument("--filePath", default="./data/testImg2.jpg")

args = args.parse_args()

output_dir = './output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Detect faces
mp_face_detection = mp.solutions.face_detection

with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:

    if args.mode in ["image"]:
        # Read image
        img_path = args.filePath
        img = cv2.imread(img_path)
        file_name = os.path.basename(img_path)

        img = process_img(img, face_detection)

        #save image
        output_path = os.path.join(output_dir, file_name)
        cv2.imwrite(output_path, img)

    elif args.mode in ['video']:
        video_path = args.filePath
        file_name = os.path.basename(video_path)
        output_path = os.path.join(output_dir, file_name)

        cap = cv2.VideoCapture(args.filePath)
        ret, frame = cap.read()

        output_video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MP4V'), 25, (frame.shape[1],frame.shape[0]))

        while ret:
            frame = process_img(frame, face_detection)
            output_video.write(frame)
            ret, frame = cap.read()

        cap.release()
        output_video.release()

    elif args.mode in ['webcam']:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: No se pudo abrir la cámara")
            exit()

        ret, frame = cap.read()
        while ret:
            frame = process_img(frame, face_detection)
            cv2.imshow('frame', frame)
            cv2.waitKey(25)
            ret, frame = cap.read()

        cap.release()