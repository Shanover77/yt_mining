import requests
import os
import csv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def getvideostats(video_ids, api_key):
    # Setting up the YouTube Data API v3 client
    url = "https://www.googleapis.com/youtube/v3/videos"

    params = {
        'part': 'statistics',
        'id': video_ids,
        'key': api_key,
    }

    response = requests.get(url, params=params)
    data = response.json()
    
    return data

api_key = os.getenv("API_KEY")

# Repalce this with the required Youtube video ids.
video_ids = ["toh1cNK_pHw", "I1qbOlzZwvA"]

video_datas = getvideostats(video_ids, api_key)["items"]

video_stats = []

for video_data in video_datas:
    statistics = video_data["statistics"]
    likes = statistics["likeCount"]
    views = statistics["viewCount"]
    commentcounts = statistics["commentCount"]
    
    video_stats.append({"VideoId": video_data["id"], "Likes": likes, "Views": views, "CommentCounts": commentcounts})

# Save the results to a CSV file
csv_file = "data/videostats.csv"

os.makedirs(os.path.dirname(csv_file), exist_ok=True)

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['VideoId', 'Likes', 'Views', 'CommentCounts']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(video_stats)

print(f"Results saved to {csv_file}.")