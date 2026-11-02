# Panduan kode penelitian

Mulai dari [metode dan cara menjalankan](methods_and_reproduction.md) untuk mengatur workspace milikmu.

- `01_pose_extraction.ipynb`: membaca video, membentuk inventaris, mengekstraksi 65 keypoint, dan mencatat kualitas pose.
- `02_resgcn_loso_e0_e7.ipynb`: membaca pose dan inventaris, membentuk fold LOSO, menerapkan preprocessing, melatih ResGCN, dan merekap evaluasi.

Folder kerja tidak harus berada di Google Drive. Input video dapat berada di folder terpisah; hasil dan cache berada di bawah `PROJECT_ROOT`. Kedua notebook harus menunjuk workspace yang sama.

Reproduksi hasil persis membutuhkan metadata dan lingkungan historis yang belum disertakan. Inventaris baru memungkinkan penyusunan ulang pipeline dari video, namun hasil training ulang belum diverifikasi dalam paket ini.
