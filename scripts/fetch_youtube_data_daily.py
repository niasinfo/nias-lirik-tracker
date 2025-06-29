
import os
import sys
import json
from datetime import datetime

# Tambahkan path root agar bisa import config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import YOUTUBE_API_KEY
from googleapiclient.discovery import build

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def fetch_videos(keyword, jumlah):
    request = youtube.search().list(
        q=keyword,
        part="snippet",
        type="video",
        maxResults=jumlah,
        order="date"
    )
    response = request.execute()

    results = []
    for item in response["items"]:
        video_id = item["id"]["videoId"]
        video_title = item["snippet"]["title"]
        channel_title = item["snippet"]["channelTitle"]
        published_at = item["snippet"]["publishedAt"]

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
    os.makedirs("data", exist_ok=True)

    lagu_nias = fetch_videos("lagu nias", 20)
    lagu_batak = fetch_videos("lagu batak", 20)

    # Simpan Lagu Nias
    with open("data/top_lagu_nias_today.json", "w", encoding="utf-8") as f:
        json.dump(lagu_nias, f, indent=2, ensure_ascii=False)

    with open("data/top_lagu_nias_today.md", "w", encoding="utf-8") as f:
        f.write("# Lagu Nias yang Sedang Dicari Hari Ini\n\n")
        for v in lagu_nias:
            f.write(f"- **{v['judul']}** oleh *{v['penyanyi']}* ({v['views']} views, rilis {v['rilis']})\n")

    # Simpan Lagu Batak
    with open("data/top_lagu_batak_today.json", "w", encoding="utf-8") as f:
        json.dump(lagu_batak, f, indent=2, ensure_ascii=False)

    with open("data/top_lagu_batak_today.md", "w", encoding="utf-8") as f:
        f.write("# Lagu Batak yang Sedang Dicari Hari Ini\n\n")
        for v in lagu_batak:
            f.write(f"- **{v['judul']}** oleh *{v['penyanyi']}* ({v['views']} views, rilis {v['rilis']})\n")
