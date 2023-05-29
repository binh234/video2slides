import argparse
import os
import validators
from config import *
from download_video import download_video
from bg_modeling import capture_slides_bg_modeling
from frame_differencing import capture_slides_frame_diff
from post_process import remove_duplicates
from utils import create_output_directory, convert_slides_to_pdf


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This script is used to convert video frames into slide PDFs."
    )
    parser.add_argument(
        "-v", "--video_path", help="Path to the video file, video url, or YouTube video link", type=str
    )
    parser.add_argument(
        "-o",
        "--out_dir",
        default="output_results",
        help="Path to the output directory",
        type=str,
    )
    parser.add_argument(
        "--type",
        help="type of background subtraction to be used",
        default="GMG",
        choices=["Frame_Diff", "GMG", "KNN"],
        type=str,
    )
    parser.add_argument(
        "-hf",
        "--hash-func",
        help="Hash function to use for image hashing. Only effective if post-processing is enabled",
        default=HASH_FUNC,
        choices=["dhash", "phash", "ahash"],
        type=str,
    )
    parser.add_argument(
        "-hs",
        "--hash-size",
        help="Hash size to use for image hashing. Only effective if post-processing is enabled",
        default=HASH_SIZE,
        choices=[8, 12, 16],
        type=int,
    )
    parser.add_argument(
        "--threshold",
        help="Minimum similarity threshold (in percent) to consider 2 images to be similar. Only effective if post-processing is enabled",
        default=SIM_THRESHOLD,
        choices=range(90, 101),
        type=int,
    )
    parser.add_argument(
        "-q",
        "--queue-len",
        help="Number of history images used to find out duplicate image. Only effective if post-processing is enabled",
        default=HASH_BUFFER_HISTORY,
        type=int,
    )
    parser.add_argument(
        "--no_post_process",
        action="store_true",
        default=False,
        help="flag to apply post processing or not",
    )
    parser.add_argument(
        "--convert_to_pdf",
        action="store_true",
        default=False,
        help="flag to convert the entire image set to pdf or not",
    )
    args = parser.parse_args()

    queue_len = args.queue_len
    if queue_len <= 0:
        print(
            f"Warnings: queue_len argument must be positive. Fallback to {HASH_BUFFER_HISTORY}"
        )
        queue_len = HASH_BUFFER_HISTORY

    video_path = args.video_path
    output_dir_path = args.out_dir
    type_bg_sub = args.type
    temp_file = False

    if validators.url(video_path):
        video_path = download_video(video_path)
        temp_file = True
        if video_path is None:
            exit(1)
    elif not os.path.exists(video_path):
        raise ValueError(
            "The video doesn't exist or isn't a valid URL. Please check your video path again"
        )

    output_dir_path = create_output_directory(video_path, output_dir_path, type_bg_sub)

    if type_bg_sub.lower() == "frame_diff":
        capture_slides_frame_diff(video_path, output_dir_path)
    else:
        if type_bg_sub.lower() == "gmg":
            thresh = DEC_THRESH
        elif type_bg_sub.lower() == "knn":
            thresh = DIST_THRESH

        capture_slides_bg_modeling(
            video_path,
            output_dir_path,
            type_bgsub=type_bg_sub,
            history=FRAME_BUFFER_HISTORY,
            threshold=thresh,
            MIN_PERCENT_THRESH=MIN_PERCENT,
            MAX_PERCENT_THRESH=MAX_PERCENT,
        )

    # Perform post-processing using difference hashing technique to remove duplicate slides.
    if not args.no_post_process:
        hash_size = args.hash_size
        hash_func = HASH_FUNC_DICT.get(args.hash_func)
        sim_threshold = args.threshold

        diff_threshold = int(hash_size * hash_size * (100 - sim_threshold) / 100)
        remove_duplicates(
            output_dir_path, hash_size, hash_func, queue_len, diff_threshold
        )

    if args.convert_to_pdf:
        convert_slides_to_pdf(output_dir_path)

    # if temp_file:
    #     os.remove(video_path)
