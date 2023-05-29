import os
import re
import cv2
import shutil
import img2pdf
from imutils import paths

# PIL can also be used to convert the image set into PDFs.
# However, using PIL requires opening each of the images in the set.
# Hence img2pdf package was used, which is able to convert the entire image set into a PDF
# without opening at once.


def sanitize_file_name(string):
    sanitized_string = re.sub(r'[^\w ]+', '', string)
    sanitized_string = re.sub(r'\s+', ' ', sanitized_string)
    sanitized_string = sanitized_string.strip()

    return sanitized_string


def resize_image_frame(frame, resize_width):
    ht, wd, _ = frame.shape
    new_height = resize_width * ht / wd
    frame = cv2.resize(
        frame, (resize_width, int(new_height)), interpolation=cv2.INTER_AREA
    )

    return frame


def create_output_directory(video_path, output_path, type_bgsub):
    vid_file_name = video_path.rsplit(os.sep)[-1].split(".")[0]
    output_dir_path = os.path.join(output_path, vid_file_name, type_bgsub)

    # Remove the output directory if there is already one.
    if os.path.exists(output_dir_path):
        shutil.rmtree(output_dir_path)

    # Create output directory.
    os.makedirs(output_dir_path, exist_ok=True)
    print("Output directory created...")
    print("Path:", output_dir_path)
    print("***" * 10, "\n")

    return output_dir_path


def convert_slides_to_pdf(img_dir, output_path=None):
    if not os.path.isdir(img_dir):
        print("The image directory doesn't exist!")
        return
    
    if output_path == None:
        pdf_file_name = os.path.basename(img_dir) + ".pdf"
        output_path = os.path.join(img_dir, pdf_file_name)
        print("Output PDF Path:", output_path)

    print("Converting captured slide images to PDF...")
    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(sorted(paths.list_images(img_dir))))

    print("PDF Created!")
    print("***" * 10, "\n")

    return output_path
