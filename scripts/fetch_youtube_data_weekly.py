import os
import json
from googleapiclient.discovery import build
from datetime import datetime

api_key = os.getenv("YOUTUBE_API_KEY")
if not api_key:
    raise ValueError("❌ API Key tidak ditemukan.")

youtube = build("youtube", "v3", developerKey=api_key)

request = youtube.search().list(
    q="lagu nias populer minggu ini",
    part="snippet",
    maxResults=20,
    type="video"
)
response = request.execute()

# Buat folder data jika belum ada
os.makedirs("data", exist_ok=True)

# Format hasil
results = []
for item in response.get("items", []):
    title = item["snippet"]["title"]
    channel = item["snippet"]["channelTitle"]
    video_id = item["id"]["videoId"]
    url = f"https://www.youtube.com/watch?v={video_id}"
    results.append({
        "title": title,
        "channel": channel,
        "url": url
    })

# Simpan ke JSON
with open("data/nias_weekly.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# Simpan ke Markdown
with open("data/nias_weekly.md", "w", encoding="utf-8") as f:
    f.write("# Daftar Lagu Nias Populer Minggu Ini\n\n")
    for i, song in enumerate(results, 1):
        f.write(f"{i}. [{song['title']}]({song['url']}) - {song['channel']}\n")
