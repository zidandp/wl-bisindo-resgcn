# Panduan kode penelitian

| Notebook | Fungsi |
|---|---|
| `01_pose_extraction.ipynb` | Membaca video, membuat inventaris, mengekstraksi 65 keypoint, dan mencatat kualitas pose |
| `02_resgcn_loso_e0_e7.ipynb` | Membaca pose dan inventaris, membentuk fold LOSO, menerapkan preprocessing, melatih ResGCN, dan merekap evaluasi |

- Kedua notebook harus memakai `PROJECT_ROOT` yang sama. Folder ini tidak harus berada di Google Drive.
- Video boleh disimpan di folder terpisah. Hasil dan cache disimpan di bawah `PROJECT_ROOT`.
- Untuk mereproduksi angka secara persis, dibutuhkan metadata dan lingkungan asli yang tidak disertakan. Inventaris baru memungkinkan pipeline dijalankan ulang dari video, tetapi hasil pelatihan ulang belum diverifikasi.

Langkah lengkap: [metode dan cara menjalankan](methods_and_reproduction.md).
