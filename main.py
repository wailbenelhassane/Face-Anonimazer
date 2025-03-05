import cv2
import mediapipe as mp
import argparse
import os

args = argparse.ArgumentParser()
args.add_argument("--mode", default="image", help="Select Mode")
args.add_argument("--filePath", default="./data/testImg.png", help="File path")
args.add_argument("--output_dir", default="./output", help="Output Directory")
args.add_argument("--blur_strength", type=int, default=40, help="Blur Strength")

args = args.parse_args()

output_dir = args.output_dir
blur_strength = args.blur_strength


def process_img(img, face_detection):
    H, W, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    out = face_detection.process(img_rgb)

    if out.detections is not None:
        for detection in out.detections:
            location_data = detection.location_data
            bbox = location_data.relative_bounding_box

            x1 = max(0, int(bbox.xmin * W))
            y1 = max(0, int(bbox.ymin * H))
            w = max(0, int(bbox.width * W))
            h = max(0, int(bbox.height * H))

            img[y1:y1 + h, x1:x1 + w, :] = cv2.blur(img[y1:y1 + h, x1:x1 + w], (blur_strength, blur_strength))
    return img


if not os.path.exists(args.filePath):
    print(f"Error: The file {args.filePath} does not exist.")
    exit()

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Output directory created: {output_dir}")

mp_face_detection = mp.solutions.face_detection

with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
    if args.mode == "image":
        if os.path.isdir(args.filePath):
            print("Processing images in the directory...")
            for file_name in os.listdir(args.filePath):
                img_path = os.path.join(args.filePath, file_name)
                if img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    print(f"Processing {file_name}...")
                    img = cv2.imread(img_path)
                    img = process_img(img, face_detection)
                    output_path = os.path.join(output_dir, file_name)
                    cv2.imwrite(output_path, img)
            print("Image processing completed.")
        else:
            print(f"Processing image {args.filePath}...")
            img = cv2.imread(args.filePath)
            img = process_img(img, face_detection)
            output_path = os.path.join(output_dir, os.path.basename(args.filePath))
            cv2.imwrite(output_path, img)
            print("Image processed and saved.")

    elif args.mode == "video":
        print(f"Processing video {args.filePath}...")
        cap = cv2.VideoCapture(args.filePath)
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read the video.")
            exit()

        frame_height = frame.shape[0] - (frame.shape[0] % 2)
        frame_width = frame.shape[1] - (frame.shape[1] % 2)
        output_path = os.path.join(output_dir, os.path.basename(args.filePath))
        output_video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MP4V'), 25, (frame_width, frame_height))

        frame_count = 0
        while ret:
            frame = process_img(frame, face_detection)
            output_video.write(frame)
            frame_count += 1
            if frame_count % 10 == 0:
                print(f"Processed {frame_count} frames...")
            ret, frame = cap.read()

        cap.release()
        output_video.release()
        print("Video processed and saved.")

    elif args.mode == "webcam":
        print("Starting live camera detection. Press 'q' to exit.")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open the camera")
            exit()

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not capture a frame from the camera.")
                break

            frame = process_img(frame, face_detection)
            cv2.imshow('frame', frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        print("Camera closed.")
