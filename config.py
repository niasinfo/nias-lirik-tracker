
import os

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY:
    raise ValueError("❌ API Key tidak ditemukan. Harap set YOUTUBE_API_KEY di GitHub Secrets.")
