import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load the variables from the .env file
load_dotenv()

# Grab the key from the environment
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube_examples(search_query, max_results=3):
    print(f"Searching YouTube for: {search_query}...")
    
    # Check if the key loaded properly
    if not YOUTUBE_API_KEY:
        return "Error: YOUTUBE_API_KEY not found in .env file."

    # Initialize the YouTube API client
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    try:
        # Step 1: Search for the videos
        search_response = youtube.search().list(
            q=search_query,
            part='id',
            maxResults=max_results,
            type='video'
        ).execute()

        # Extract the Video IDs
        video_ids = []
        for item in search_response.get('items', []):
            video_ids.append(item['id']['videoId'])

        if not video_ids:
            return "No videos found."

        # Step 2: Fetch the full descriptions using the Video IDs
        video_response = youtube.videos().list(
            id=','.join(video_ids),
            part='snippet'
        ).execute()

        descriptions = []
        for i, item in enumerate(video_response.get('items', [])):
            desc = item['snippet']['description']
            descriptions.append(f"--- Example {i+1} ---\n{desc}\n")

        print("Successfully grabbed example descriptions!")
        return "\n".join(descriptions)

    except Exception as e:
        return f"An error occurred: {e}"

# --- Test Block ---
if __name__ == "__main__":
    # A test search to see if the key works
    test_query = "Grayzone Warfare update spearhead gameplay"
    print(get_youtube_examples(test_query))