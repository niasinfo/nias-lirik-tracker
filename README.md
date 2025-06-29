
# Nias Lirik Tracker

Sistem otomatis untuk mendeteksi lagu-lagu Nias yang sedang populer di YouTube setiap minggu.

## Cara Pakai

1. Upload semua file ini ke GitHub repository Anda.
2. Pastikan `GitHub Actions` aktif (lihat tab "Actions").
3. Setiap minggu, file `data/top_lagu_nias.json` dan `data/top_lagu_nias.md` akan terupdate otomatis.
4. Gunakan hasilnya untuk membuat konten di situs lirik Anda.

## File Penting

- `scripts/fetch_youtube_data.py`: Script utama.
- `data/top_lagu_nias.json`: Data lagu dalam format JSON.
- `data/top_lagu_nias.md`: Versi siap posting.

API YouTube digunakan untuk mengambil data secara real-time.
