
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import YOUTUBE_API_KEY
from googleapiclient.discovery import build

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def fetch_videos(keyword, jumlah, mode="relevance"):
    request = youtube.search().list(
        q=keyword,
        part="snippet",
        type="video",
        maxResults=jumlah,
        order=mode
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

def save_results(results, base_filename, title):
    with open(f"data/{base_filename}.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    with open(f"data/{base_filename}.md", "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        for v in results:
            f.write(f"- **{v['judul']}** oleh *{v['penyanyi']}* ({v['views']} views, rilis {v['rilis']})\n")

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    kategori = {
        # Lagu Anak
        "lagu anak nias": "lagu_anak_nias",
        "lagu anak batak": "lagu_anak_batak",
        # Lagu Lawas
        "lagu nias lawas": "lagu_lawas_nias",
        "lagu batak lawas": "lagu_lawas_batak",
        # Lagu Rohani
        "lagu rohani nias": "lagu_rohani_nias",
        "lagu rohani batak": "lagu_rohani_batak",
        # Chord
        "lagu rohani nias chord": "chord_rohani_nias",
        "lagu rohani batak chord": "chord_rohani_batak",
        "lagu anak nias chord": "chord_anak_nias",
        "lagu anak batak chord": "chord_anak_batak",
        "lagu nias lawas chord": "chord_lawas_nias",
        "lagu batak lawas chord": "chord_lawas_batak",
        # Karaoke
        "lagu anak nias karaoke": "karaoke_anak_nias",
        "lagu anak batak karaoke": "karaoke_anak_batak",
        "lagu rohani nias karaoke": "karaoke_rohani_nias",
        "lagu rohani batak karaoke": "karaoke_rohani_batak",
        "lagu nias lawas karaoke": "karaoke_lawas_nias",
        "lagu batak lawas karaoke": "karaoke_lawas_batak"
    }

    for key, filename in kategori.items():
        hasil = fetch_videos(key, 15)
        title = filename.replace("_", " ").title()
        save_results(hasil, f"top_{filename}", title)
