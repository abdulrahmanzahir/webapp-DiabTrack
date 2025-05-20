import datetime
import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Load your credentials.json (OAuth 2.0 file from Google Cloud)
CLIENT_SECRETS_FILE = "client_secret.json"  # <-- Rename your .json to this or update path

SCOPES = ['https://www.googleapis.com/auth/fitness.activity.read',
          'https://www.googleapis.com/auth/fitness.heart_rate.read']

def get_fitness_service():
    flow = InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    SCOPES,
    redirect_uri='http://localhost:8080/'
)
    creds = flow.run_local_server(port=0)
    service = build('fitness', 'v1', credentials=creds)
    return service

def nanoseconds(dt):
    return int(dt.timestamp() * 1e9)

def fetch_data():
    service = get_fitness_service()

    # Time range: last 24 hours
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=1)

    dataset = f"{nanoseconds(start_time)}-{nanoseconds(end_time)}"

    data_sources = {
        'step_count': 'derived:com.google.step_count.delta:com.google.android.gms:estimated_steps',
        'heart_rate': 'derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm'
    }

    for key, data_source in data_sources.items():
        result = service.users().dataSources(). \
            datasets().get(userId='me', dataSourceId=data_source, datasetId=dataset).execute()
        
        print(f"\n🔹 {key.replace('_', ' ').title()} Data:")
        for point in result.get("point", []):
            for field in point["value"]:
                print(field["fpVal"] if "fpVal" in field else field["intVal"])

if __name__ == '__main__':
    fetch_data()
