import csv
import requests
import datetime

def get_current_time_as_filename():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    return formatted_time

def search_videos(query, api_key):
    url = "https://www.googleapis.com/youtube/v3/search"
    
    params = {
        'part': 'id,snippet',
        'q': query,
        'key': api_key,
        'maxResults': 100
    }

    response = requests.get(url, params=params)
    data = response.json()

    videos = []
    
    if 'items' in data:
        for item in data['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append({'Video ID': video_id, 'Title': title, 'URL': video_url})
    
    return videos

# Set your API key here
API_KEY = "API_KEY"

# Search for videos with the query 'car'
search_results = search_videos("car", API_KEY)

# Save the results to a CSV file
csv_file = "yt.csv"

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['Video ID', 'Title', 'URL']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(search_results)

print(f"Results saved to {csv_file}.")
