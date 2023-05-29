import argparse
from utils import convert_slides_to_pdf

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This script is used to convert video frames into slide PDFs."
    )
    parser.add_argument(
        "-f", "--folder", help="Path to the image folder", type=str
    )
    parser.add_argument(
        "-o",
        "--out_path",
        help="Path to the output PDF file. If None, the image directory will be used to store the output file.",
        type=str,
    )
    args = parser.parse_args()

    img_dir = args.folder
    output_path = args.out_path

    convert_slides_to_pdf(img_dir, output_path)