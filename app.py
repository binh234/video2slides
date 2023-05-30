import gradio as gr
import os
import validators
from imutils import paths
from config import *
from download_video import download_video
from bg_modeling import capture_slides_bg_modeling
from frame_differencing import capture_slides_frame_diff
from post_process import remove_duplicates
from utils import create_output_directory, convert_slides_to_pdf


def process(
    video_path,
    bg_type,
    frame_buffer_history,
    hash_size,
    hash_func,
    hash_queue_len,
    sim_threshold,
):
    output_dir_path = "output_results"
    output_dir_path = create_output_directory(video_path, output_dir_path, bg_type)

    if bg_type.lower() == "Frame Diff":
        capture_slides_frame_diff(video_path, output_dir_path)
    else:
        if bg_type.lower() == "gmg":
            thresh = DEC_THRESH
        elif bg_type.lower() == "knn":
            thresh = DIST_THRESH

        capture_slides_bg_modeling(
            video_path,
            output_dir_path,
            type_bgsub=bg_type,
            history=frame_buffer_history,
            threshold=thresh,
            MIN_PERCENT_THRESH=MIN_PERCENT,
            MAX_PERCENT_THRESH=MAX_PERCENT,
        )

    # Perform post-processing using difference hashing technique to remove duplicate slides.
    hash_func = HASH_FUNC_DICT.get(hash_func.lower())

    diff_threshold = int(hash_size * hash_size * (100 - sim_threshold) / 100)
    remove_duplicates(
        output_dir_path, hash_size, hash_func, hash_queue_len, diff_threshold
    )

    pdf_path = convert_slides_to_pdf(output_dir_path)

    # Remove unneccessary files
    os.remove(video_path)
    for image_path in paths.list_images(output_dir_path):
        os.remove(image_path)
    return pdf_path


def process_file(
    file_obj,
    bg_type,
    frame_buffer_history,
    hash_size,
    hash_func,
    hash_queue_len,
    sim_threshold,
):
    return process(
        file_obj.name,
        bg_type,
        frame_buffer_history,
        hash_size,
        hash_func,
        hash_queue_len,
        sim_threshold,
    )


def process_via_url(
    url,
    bg_type,
    frame_buffer_history,
    hash_size,
    hash_func,
    hash_queue_len,
    sim_threshold,
):
    if validators.url(url):
        video_path = download_video(url)
        if video_path is None:
            raise gr.Error("An error occurred while downloading the video, please try again later")
        return process(
            video_path,
            bg_type,
            frame_buffer_history,
            hash_size,
            hash_func,
            hash_queue_len,
            sim_threshold,
        )
    else:
        raise gr.Error("Please enter a valid video URL")


with gr.Blocks(css="style.css") as demo:
    with gr.Row(elem_classes=["container"]):
        gr.Markdown(
            """
        # Video 2 Slides Converter
        
        Convert your video presentation into PDF slides with one click.

        You can browse your video from the local file system, or enter a video URL/YouTube video link to start processing.

        **Note**: 
        - It will take some time to complete (~ half of the original video length), so stay tuned!
        - If the YouTube video link doesn't work, you can try again later or download video to your computer and then upload it to the app
        - Remember to press Enter if you are using an external URL
        """,
            elem_id="container",
        )

    with gr.Row(elem_classes=["container"]):
        with gr.Column(scale=1):
            with gr.Accordion("Advanced parameters"):
                bg_type = gr.Dropdown(
                    ["Frame Diff", "GMG", "KNN"],
                    value="GMG",
                    label="Background subtraction",
                    info="Type of background subtraction to be used",
                )
                frame_buffer_history = gr.Slider(
                    minimum=5,
                    maximum=20,
                    value=FRAME_BUFFER_HISTORY,
                    step=5,
                    label="Frame buffer history",
                    info="Length of the frame buffer history to model background.",
                )
                # Post process
                hash_func = gr.Dropdown(
                    ["Difference hashing", "Perceptual hashing", "Average hashing"],
                    value="Difference hashing",
                    label="Background subtraction",
                    info="Hash function to use for image hashing",
                )
                hash_size = gr.Slider(
                    minimum=8,
                    maximum=16,
                    value=HASH_SIZE,
                    step=2,
                    label="Hash size",
                    info="Hash size to use for image hashing",
                )
                hash_queue_len = gr.Slider(
                    minimum=5,
                    maximum=15,
                    value=HASH_BUFFER_HISTORY,
                    step=5,
                    label="Hash queue len",
                    info="Number of history images used to find out duplicate image",
                )
                sim_threshold = gr.Slider(
                    minimum=90,
                    maximum=100,
                    value=SIM_THRESHOLD,
                    step=1,
                    label="Similarity threshold",
                    info="Minimum similarity threshold (in percent) to consider 2 images to be similar",
                )

        with gr.Column(scale=2):
            with gr.Row(elem_id="row-flex"):
                with gr.Column(scale=3):
                    file_url = gr.Textbox(
                        value="",
                        label="Upload your file",
                        placeholder="Enter a video url or YouTube video link",
                        show_label=False,
                    )
                with gr.Column(scale=1, min_width=160):
                    upload_button = gr.UploadButton("Browse File", file_types=["video"])
            file_output = gr.File(file_types=[".pdf"], label="Output PDF")
            gr.Examples(
                [
                    [
                        "https://www.youtube.com/watch?v=bfmFfD2RIcg",
                        "output_results/Neural Network In 5 Minutes.pdf",
                    ],
                    [
                        "https://www.youtube.com/watch?v=EEo10bgsh0k",
                        "output_results/react-in-5-minutes.pdf",
                    ],
                ],
                [file_url, file_output],
            )

    file_url.submit(
        process_via_url,
        [
            file_url,
            bg_type,
            frame_buffer_history,
            hash_size,
            hash_func,
            hash_queue_len,
            sim_threshold,
        ],
        file_output,
    )
    upload_button.upload(
        process_file,
        [
            upload_button,
            bg_type,
            frame_buffer_history,
            hash_size,
            hash_func,
            hash_queue_len,
            sim_threshold,
        ],
        file_output,
    )

demo.queue(concurrency_count=4).launch()
