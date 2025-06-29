
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import YOUTUBE_API_KEY
from googleapiclient.discovery import build

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def fetch_chord_videos(keyword, jumlah):
    request = youtube.search().list(
        q=f"{keyword} chord",
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

    chord_nias = fetch_chord_videos("lagu nias", 15)
    chord_batak = fetch_chord_videos("lagu batak", 15)

    with open("data/top_chord_lagu_nias.json", "w", encoding="utf-8") as f:
        json.dump(chord_nias, f, indent=2, ensure_ascii=False)

    with open("data/top_chord_lagu_nias.md", "w", encoding="utf-8") as f:
        f.write("# Lagu Nias yang Dicari Chord-nya\n\n")
        for v in chord_nias:
            f.write(f"- **{v['judul']}** oleh *{v['penyanyi']}* ({v['views']} views, rilis {v['rilis']})\n")

    with open("data/top_chord_lagu_batak.json", "w", encoding="utf-8") as f:
        json.dump(chord_batak, f, indent=2, ensure_ascii=False)

    with open("data/top_chord_lagu_batak.md", "w", encoding="utf-8") as f:
        f.write("# Lagu Batak yang Dicari Chord-nya\n\n")
        for v in chord_batak:
            f.write(f"- **{v['judul']}** oleh *{v['penyanyi']}* ({v['views']} views, rilis {v['rilis']})\n")
