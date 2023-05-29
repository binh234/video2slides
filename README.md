# Video to Slides Converter: Transform Video Lectures into Slide Presentations

This is a simple video-to-slide converter application that aims to obtain slide images (or pdf) given slide or lecture videos.

This is highly useful when one wishes to have a video lecture(with or without animations) in the form of slides – either a ppt or pdf. However, more often than not, slides are not provided when such video lectures are hosted on platforms like YouTube. This project aims to build a robust application that can convert video lectures into corresponding slides using techniques such as basic frame differencing and statistical background subtraction models such as **KNN** or **GMG**.

**Notes**:

- It will take some time to complete (about half of the original video length), so stay tuned!
- If the YouTube video link doesn't work, you can try again later or download the video and process it locally
- For slide videos with full background animation similar to [this video](https://www.youtube.com/watch?v=YxlDoz_P4kc), the algorithm cannot extract the right frames after tthe animation ends. In that case, using Frame Differencing (`--type Frame_Diff`) will yield better results, but the results are still decent.
- You may want to trim the video before processing it for better results.

## Dependencies

1. Install OpenCV
    **If you already have opencv installed, skip this step**

    ```bash
    pip install opencv-contrib-python==4.7.0.72
    ```

2. Install other packages

    ```bash
    pip install -r requirements.txt
    ```

3. Install gradio (optional)
   **If you don't use the GUI version, skip this step**

   ```bash
    pip install gradio
    ```

## Command-Line Options

```bash
usage: video_2_slides.py [-h] [-v VIDEO_FILE_PATH] [-o OUT_DIR] [--type {Frame_Diff,GMG,KNN}] [-hf {dhash,phash,ahash}] [-hs {8,12,16}]
                         [--threshold {90,91,92,93,94,95,96,97,98,99,100}] [-q QUEUE_LEN] [--no_post_process] [--convert_to_pdf]

This script is used to convert video frames into slide PDF.

optional arguments:
  -h, --help            show this help message and exit
  -v VIDEO_PATH, --video_path VIDEO_FILE_PATH
                        Path to the video file, video url, or YouTube video link
  -o OUT_DIR, --out_dir OUT_DIR
                        Path to the output directory
  --type {Frame_Diff,GMG,KNN}
                        type of background subtraction to be used
  -hf {dhash,phash,ahash}, --hash-func {dhash,phash,ahash}
                        Hash function to use for image hashing. Only effective if post-processing is enabled
  -hs {8,12,16}, --hash-size {8,12,16}
                        Hash size to use for image hashing. Only effective if post-processing is enabled
  --threshold {90,91,92,93,94,95,96,97,98,99,100}
                        Minimum similarity threshold (in percent) to consider 2 images to be similar. Only effective if post-processing is enabled
  -q QUEUE_LEN, --queue-len QUEUE_LEN
                        Number of history images used to find out duplicate image. Only effective if post-processing is enabled
  --no_post_process     flag to apply post processing or not
  --convert_to_pdf      flag to convert the entire image set to pdf or not
```

If you want to manually remove some images before generating final PDF file, you can use the `convert_to_pdf.py` script later to convert the entire image set to pdf

```bash
usage: convert_to_pdf.py [-h] [-f FOLDER] [-o OUT_PATH]

This script is used to convert video frames into slide PDFs.

optional arguments:
  -h, --help            show this help message and exit
  -f FOLDER, --folder FOLDER
                        Path to the image folder
  -o OUT_PATH, --out_path OUT_PATH
                        Path to the output PDF file. If None, the image
                        directory will be used to store the output file.
```

## Gradio App

```bash
gradio app.py
```

The application will be available at [http://localhost:7680](http://localhost:7680)

## Sample outputs

| Video file | Output |
|---|---|
| [https://www.youtube.com/watch?v=bfmFfD2RIcg](https://www.youtube.com/watch?v=bfmFfD2RIcg) | output_results/Neural Network In 5 Minutes.pdf  |
| [https://www.youtube.com/watch?v=rQijrDj1wCQ](https://www.youtube.com/watch?v=rQijrDj1wCQ) | output_results/What is Docker Container Docker explained in 5 minutes.pdf  |
| [https://www.youtube.com/watch?v=YxlDoz_P4kc](https://www.youtube.com/watch?v=YxlDoz_P4kc) | output_results/Introduction to Stable Diffusion.pdf  |
| sample_vids/react-in-5-minutes.mp4 | output_results/react-in-5-minutes.pdf |

## References

1. [OpenCV blog](https://learnopencv.com/video-to-slides-converter-using-background-subtraction/)
2. [Simple Background Estimation in Videos using OpenCV](https://learnopencv.com/simple-background-estimation-in-videos-using-opencv-c-python/)
3. [Image Hashing](https://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html)
