from pytube import YouTube


def download_youtube_video(video_url):
    try:
        # Create a YouTube object
        yt = YouTube(video_url)

        # Get all available streams
        video_streams = yt.streams.order_by("resolution").desc()
        audio_streams = (
            yt.streams.filter(only_audio=True)
            .filter(mime_type="audio/mp4")
            .order_by("abr")
            .desc()
        )

        # Choose the highest resolution stream
        print("streams available are: ")
        for i, stream in enumerate(video_streams):
            print(
                f"{i+1}. {stream.resolution} {stream.mime_type} {stream.is_progressive}"
            )

        print("audio streams available are: ")
        for i, stream in enumerate(audio_streams):
            print(f"{i+1}. {stream.abr} {stream.mime_type} {stream.is_progressive}")

        audio_stream = audio_streams[0]
        stream = video_streams[0]

        # Download the video
        print(f"Downloading {yt.title} in {stream.resolution} quality...")
        # stream.download(
        #     output_path="/Users/shubhamdamkondwar/Documents/yt_auto/downloads"
        # )
        print(f"Video {yt.title} downloaded successfully!")
        # audio_stream.download(
        #     output_path="/Users/shubhamdamkondwar/Documents/yt_auto/downloads"
        # )
        print(f"Audio for {yt.title} downloaded successfully!")
    except Exception as e:
        print("Error:", e)


# Example usage
if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    download_youtube_video(video_url)
