
import os
from googleapiclient.discovery import build
from datetime import datetime
from config import YOUTUBE_API_KEY

# Konfigurasi
KEYWORD = "lagu nias"
MAX_RESULTS = 10

# Inisialisasi YouTube API
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def fetch_videos():
    request = youtube.search().list(
        q=KEYWORD,
        part="snippet",
        type="video",
        maxResults=MAX_RESULTS,
        order="viewCount"
    )
    response = request.execute()

    results = []
    for item in response["items"]:
        video_id = item["id"]["videoId"]
        video_title = item["snippet"]["title"]
        channel_title = item["snippet"]["channelTitle"]
        published_at = item["snippet"]["publishedAt"]

        # Ambil statistik view
        stats = youtube.videos().list(
            part="statistics",
            id=video_id
        ).execute()

        view_count = int(stats["items"][0]["statistics"].get("viewCount", 0))

        results.append({
            "judul": video_title,
            "penyanyi": channel_title,
            "views": view_count,
            "rilis": published_at.split("T")[0]
        })

    return results

if __name__ == "__main__":
    videos = fetch_videos()

    # Pastikan folder data ada
    os.makedirs("data", exist_ok=True)

    # Simpan ke JSON
    import json
    with open("data/top_lagu_nias.json", "w", encoding="utf-8") as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)

    # Simpan ke Markdown
    with open("data/top_lagu_nias.md", "w", encoding="utf-8") as f:
        f.write("# Daftar Lagu Nias Populer Minggu Ini\n\n")
        for v in videos:
            f.write(f"- **{v['judul']}** oleh *{v['penyanyi']}* ({v['views']} views, rilis {v['rilis']})\n")
