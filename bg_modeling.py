import os
import time
import sys
import cv2
from utils import resize_image_frame


def capture_slides_bg_modeling(
    video_path,
    output_dir_path,
    type_bgsub,
    history,
    threshold,
    MIN_PERCENT_THRESH,
    MAX_PERCENT_THRESH,
):
    print(f"Using {type_bgsub} for Background Modeling...")
    print("---" * 10)

    if type_bgsub == "GMG":
        bg_sub = cv2.bgsegm.createBackgroundSubtractorGMG(
            initializationFrames=history, decisionThreshold=threshold
        )
    elif type_bgsub == "KNN":
        bg_sub = cv2.createBackgroundSubtractorKNN(
            history=history, dist2Threshold=threshold, detectShadows=False
        )
    else:
        raise ValueError("Please choose GMG or KNN as background subtraction method")

    capture_frame = False
    screenshots_count = 0

    # Capture video frames.
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Unable to open video file: ", video_path)
        sys.exit()

    start = time.time()
    # Loop over subsequent frames.
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # Create a copy of the original frame.
        orig_frame = frame.copy()
        # Resize the frame keeping aspect ratio.
        frame = resize_image_frame(frame, resize_width=640)

        # Apply each frame through the background subtractor.
        fg_mask = bg_sub.apply(frame)

        # Compute the percentage of the Foreground mask."
        p_non_zero = (cv2.countNonZero(fg_mask) / (1.0 * fg_mask.size)) * 100

        # %age of non-zero pixels < MAX_PERCENT_THRESH, implies motion has stopped.
        # Therefore, capture the frame.
        if p_non_zero < MAX_PERCENT_THRESH and not capture_frame:
            capture_frame = True

            screenshots_count += 1

            png_filename = f"{screenshots_count:03}.jpg"
            out_file_path = os.path.join(output_dir_path, png_filename)
            print(f"Saving file at: {out_file_path}")
            cv2.imwrite(out_file_path, orig_frame, [cv2.IMWRITE_JPEG_QUALITY, 75])

        # p_non_zero >= MIN_PERCENT_THRESH, indicates motion/animations.
        # Hence wait till the motion across subsequent frames has settled down.
        elif capture_frame and p_non_zero >= MIN_PERCENT_THRESH:
            capture_frame = False

    end_time = time.time()
    print("***" * 10, "\n")
    print("Statistics:")
    print("---" * 10)
    print(f"Total Time taken: {round(end_time-start, 3)} secs")
    print(f"Total Screenshots captured: {screenshots_count}")
    print("---" * 10, "\n")

    # Release Video Capture object.
    cap.release()
