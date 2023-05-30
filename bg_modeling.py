import cv2
import os
import sys
from tqdm import tqdm
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

    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    prog_bar = tqdm(total=num_frames)

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
            cv2.imwrite(out_file_path, orig_frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
            prog_bar.set_postfix_str(f"Total Screenshots: {screenshots_count}")

        # p_non_zero >= MIN_PERCENT_THRESH, indicates motion/animations.
        # Hence wait till the motion across subsequent frames has settled down.
        elif capture_frame and p_non_zero >= MIN_PERCENT_THRESH:
            capture_frame = False
        
        prog_bar.update(1)

    # Release progress bar and video capture object.
    prog_bar.close()
    cap.release()
