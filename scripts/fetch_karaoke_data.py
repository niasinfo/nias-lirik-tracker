
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import YOUTUBE_API_KEY
from googleapiclient.discovery import build

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def fetch_karaoke_videos(keyword, jumlah):
    request = youtube.search().list(
        q=f"{keyword} karaoke",
        part="snippet",
        type="video",
        maxResults=jumlah,
        order="relevance"
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

    karaoke_nias = fetch_karaoke_videos("lagu nias", 15)
    karaoke_batak = fetch_karaoke_videos("lagu batak", 15)

    with open("data/top_karaoke_lagu_nias.json", "w", encoding="utf-8") as f:
        json.dump(karaoke_nias, f, indent=2, ensure_ascii=False)

    with open("data/top_karaoke_lagu_nias.md", "w", encoding="utf-8") as f:
        f.write("# Karaoke Lagu Nias yang Sedang Dicari Hari Ini\n\n")
        for v in karaoke_nias:
            f.write(f"- **{v['judul']}** oleh *{v['penyanyi']}* ({v['views']} views, rilis {v['rilis']})\n")

    with open("data/top_karaoke_lagu_batak.json", "w", encoding="utf-8") as f:
        json.dump(karaoke_batak, f, indent=2, ensure_ascii=False)

    with open("data/top_karaoke_lagu_batak.md", "w", encoding="utf-8") as f:
        f.write("# Karaoke Lagu Batak yang Sedang Dicari Hari Ini\n\n")
        for v in karaoke_batak:
            f.write(f"- **{v['judul']}** oleh *{v['penyanyi']}* ({v['views']} views, rilis {v['rilis']})\n")
