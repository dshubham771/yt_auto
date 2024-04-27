import pickle

from google_auth_oauthlib.flow import InstalledAppFlow

# Constants
CLIENT_SECRET_FILE = "config/client_secret.json"
API_NAME = "youtube"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Authenticate and get credentials
try:
    with open("config/credentials.pickle", "rb") as token:
        creds = pickle.load(token)
except FileNotFoundError:
    print("Authenticating and saving credentials...")
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    with open("config/credentials.pickle", "wb") as token:
        pickle.dump(creds, token)
    print("Authenticated and credentials saved successfully!")