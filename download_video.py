import mimetypes
import re
import tempfile
import requests
import os
from urllib.parse import urlparse
from pytube import YouTube
from config import DOWNLOAD_DIR


def download_video_from_url(url, output_dir=DOWNLOAD_DIR):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        content_type = response.headers.get("content-type")
        if "video" not in content_type:
            print("The given URL is not a valid video")
            return None
        file_extension = mimetypes.guess_extension(content_type)

        os.makedirs(output_dir, exist_ok=True)

        temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=file_extension, dir=output_dir
        )
        temp_file_path = temp_file.name

        with open(temp_file_path, "wb") as file:
            file.write(response.content)
        return temp_file_path

    except requests.exceptions.RequestException as e:
        print("An error occurred while downloading the video:", str(e))
        return None


def download_video_from_youtube(url, output_dir=DOWNLOAD_DIR):
    try:
        yt = YouTube(url)
        video = (
            yt.streams.filter(progressive=True, file_extension="mp4")
            .order_by("resolution")
            .desc()
            .first()
        )

        os.makedirs(output_dir, exist_ok=True)

        video_path = video.download(output_dir)
        return video_path

    except Exception as e:
        print("An error occurred while downloading the video:", str(e))
        return None


def download_video(url, output_dir=DOWNLOAD_DIR):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    domain = re.sub(r"\.", "", domain) # Match for both youtube and youtu.be

    print("---" * 5, "Downloading video file", "---" * 5)

    if "youtube" in domain:
        video_path = download_video_from_youtube(url, output_dir)
    else:
        video_path = download_video_from_url(url, output_dir)

    if video_path:
        print(f"Saving file at: {video_path}")
        print("---" * 10)
    return video_path


if __name__ == "__main__":
    youtube_link = "https://www.youtube.com/watch?v=2OTq15A5s0Y"
    temp_video_path = download_video_from_youtube(youtube_link)

    if temp_video_path is not None:
        print("Video downloaded successfully to:", temp_video_path)
    else:
        print("Failed to download the video.")
