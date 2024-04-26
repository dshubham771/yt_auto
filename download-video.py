import os
import shutil
import uuid

from pytube import YouTube
import ffmpeg

from utils.common_utils import move_file

base_download_path = "downloads"


def get_video_filename(download_path, yt, video_stream):
    video_path = os.path.join(download_path, f"{yt.title}")
    if video_stream.mime_type.split("/")[-1] == "webm":
        video_path = video_path + "_raw"
    return video_path + "." + video_stream.mime_type.split("/")[-1]


def download_youtube_video(video_url):
    try:
        print(f"Downloading video for {video_url}...")
        download_path = os.path.join(os.getcwd(), base_download_path, "temp", uuid.uuid4().hex)
        os.makedirs(download_path, exist_ok=True)
        yt = YouTube(video_url)

        video_streams = yt.streams.order_by("resolution").desc()
        print("video streams available are: ")
        for i, stream in enumerate(video_streams):
            print(f"{i + 1}. {stream.resolution} {stream.mime_type} {stream.is_progressive}")

        video_stream = video_streams[0]
        video_filename = get_video_filename(download_path, yt, video_stream)
        final_video_file_name = os.path.join(download_path, f"{yt.title}.{video_stream.mime_type.split('/')[-1]}")

        print(f"Downloading {yt.title} in {video_stream.resolution} quality...")
        video_stream.download(filename=video_filename)
        print(f"Video {yt.title} downloaded successfully!")

        if video_stream.mime_type.split("/")[-1] == "webm":
            print("Downloading audio separately as the video is in webm format...")
            audio_streams = yt.streams.filter(only_audio=True).filter(mime_type="audio/mp4").order_by("abr").desc()

            print("audio streams available are: ")
            for i, stream in enumerate(audio_streams):
                print(f"{i + 1}. {stream.abr} {stream.mime_type} {stream.is_progressive}")

            audio_stream = audio_streams[0]
            audio_filename = os.path.join(download_path, f"{yt.title}_audio." + audio_stream.mime_type.split("/")[-1])
            audio_stream.download(filename=audio_filename)
            print(f"Audio for {yt.title} downloaded successfully!")
            stream1 = ffmpeg.input(video_filename)
            stream2 = ffmpeg.input(audio_filename)
            final_video_file_name = os.path.join(download_path, f"{yt.title}.mp4")
            combined_stream = ffmpeg.output(stream1, stream2, final_video_file_name, vcodec="copy", acodec="copy")
            ffmpeg.run(combined_stream, overwrite_output=True)

        move_file(final_video_file_name, os.path.join(os.getcwd(), base_download_path, "final", final_video_file_name.split("/")[-1]))
        shutil.rmtree(download_path)
        print(f"deleted {download_path} folder")

    except Exception as e:
        print("Error:", e)


# Example usage
if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    download_youtube_video(video_url)
