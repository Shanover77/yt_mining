import csv
import requests
import datetime

def get_current_time_as_filename():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    return formatted_time

def search_videos(query, api_key, page_token=None):
    url = "https://www.googleapis.com/youtube/v3/search"
    
    params = {
        'part': 'id,snippet',
        'q': query,
        'key': api_key,
        'maxResults': 200  # Adjust the maximum number of results per page as needed
    }

    if page_token:
        params['pageToken'] = page_token
    
    response = requests.get(url, params=params)
    data = response.json()

    videos = []
    
    if 'items' in data:
        for item in data['items']:
            if 'videoId' in item['id']:
                video_id = item['id']['videoId']
                title = item['snippet']['title']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                videos.append({'Video ID': video_id, 'Title': title, 'URL': video_url})
    
    next_page_token = data.get('nextPageToken')
    
    return videos, next_page_token

# Set your API key here
API_KEY = "API_KEY"

# Set the query and desired number of pages
query = "english movie trailer 2022"
num_pages = 100

# Search for videos and retrieve multiple pages of results
search_results = []
next_page_token = None

for _ in range(num_pages):
    videos, next_page_token = search_videos(query, API_KEY, next_page_token)
    search_results.extend(videos)
    
    if not next_page_token:
        break

# Save the results to a CSV file
csv_file = 'data/' + query + ".csv"

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['Video ID', 'Title', 'URL']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(search_results)

print(f"Results saved to {csv_file}.")
