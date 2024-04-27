import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def upload_video_with_thumbnail(video_file_path, title, description, tags, thumbnail_path):
    try:
        with open("config/credentials.pickle", "rb") as token:
            creds = pickle.load(token)
    except FileNotFoundError:
        print("Credentials not found")
        return
    print("Credentials loaded successfully!")
    youtube = build("youtube", "v3", credentials=creds)

    # Prepare request body
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "10",  # Music category
        },
        "status": {
            "privacyStatus": "public"
        },
    }

    print("Uploading video...")
    media_file = MediaFileUpload(video_file_path, chunksize=-1, resumable=True)
    upload_request = youtube.videos().insert(
        part="snippet,status", body=request_body, media_body=media_file
    )

    response = None
    while response is None:
        status, response = upload_request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    video_id = response["id"]
    (youtube.thumbnails().set(videoId=video_id,
                              media_body=MediaFileUpload(thumbnail_path, mimetype='image/jpeg', resumable=True))
     .execute())

    print(f'Video uploaded! Video ID: {response["id"]}')


# Usage example
video_path = "/Users/shubhamdamkondwar/Documents/PycharmProjects/yt_auto/downloads/final/Tum Se.mp4"
thumbnail_path = "/Users/shubhamdamkondwar/Documents/PycharmProjects/yt_auto/downloads/final/tum_se_thumbnail.jpg"
title = "Testing Upload with API"
description = "This was a test"
tags = ["music", "bollywood", "bollywood music", "bollywood songs", "hindi songs", "hindi music", "hindi gaane"]

upload_video_with_thumbnail(video_path, title, description, tags, thumbnail_path)
