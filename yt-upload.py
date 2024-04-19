import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Constants
CLIENT_SECRET_FILE = "client_secret.json"
API_NAME = "youtube"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Authenticate and get credentials
creds = None
token_file = "token.json"

if os.path.exists(token_file):
    creds = Credentials.from_authorized_user_file(token_file)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=0)

    with open(token_file, "w") as token:
        token.write(creds.to_json())

# Create YouTube API service
youtube = build(API_NAME, API_VERSION, credentials=creds)

# Upload video
video_file_path = "sample_video.mp4"  # Replace with the path to your video file
title = "Testing Upload with API"
description = "This was a test"
tags = ["tag1", "tag2"]

request_body = {
    "snippet": {
        "title": title,
        "description": description,
        "tags": tags,
        "categoryId": "22",  # You can find the category ID for your video category
    },
    "status": {
        "privacyStatus": "public"  # You can set the privacy status (private, public, unlisted)
    },
}

media_file = MediaFileUpload(video_file_path, chunksize=-1, resumable=True)
upload_request = youtube.videos().insert(
    part="snippet,status", body=request_body, media_body=media_file
)

response = None
while response is None:
    status, response = upload_request.next_chunk()
    if status:
        print(f"Uploaded {int(status.progress() * 100)}%")

print(f'Video uploaded! Video ID: {response["id"]}')
