import os
from googleapiclient.discovery import build

# Ambil API key dari environment
api_key = os.getenv("YOUTUBE_API_KEY")
if not api_key:
    raise ValueError("❌ API Key tidak ditemukan. Pastikan YOUTUBE_API_KEY sudah di-set.")

# Inisialisasi YouTube API client
youtube = build("youtube", "v3", developerKey=api_key)

# Contoh pencarian: Lagu Nias populer minggu ini
request = youtube.search().list(
    q="lagu nias populer minggu ini",
    part="snippet",
    maxResults=10,
    type="video"
)
response = request.execute()

# Tampilkan hasil
for item in response.get("items", []):
    print(f"[Mingguan] 🎵 {item['snippet']['title']}")
