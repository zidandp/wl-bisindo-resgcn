# Metode dan cara menjalankan

Rujukan arsitektur dan preprocessing dijelaskan dalam [daftar referensi](references.md).

## Pengolahan pose

Video diproses dengan MediaPipe Pose Landmarker dan Hand Landmarker secara terpisah. Setiap video menghasilkan sekuens `(T,65,2)`, dengan T sebagai jumlah frame. Keypoint yang tidak terdeteksi disimpan sebagai `(0,0)`.

Interpolasi linear mengisi titik hilang di tengah sekuens apabila terdapat pengamatan valid sebelum dan sesudahnya. Titik hilang pada batas awal atau akhir tidak diekstrapolasi. Normalisasi menggunakan pusat mid-hip; jika tidak tersedia, digunakan pusat pinggul, bahu, atau rata-rata keypoint valid. Skala dibagi dengan rata-rata jarak bahu valid. Titik yang tetap tidak valid dikembalikan ke nol.

Semua konfigurasi distandardisasi menjadi 64 frame. Koordinat di-resample secara linear dan mask validitas menggunakan nearest neighbor. Proses ini berbeda dari interpolasi titik hilang yang menjadi faktor eksperimen.

Augmentasi berupa rotasi ±10 derajat dan Gaussian jitter dengan sigma 0,015, masing-masing berpeluang 0,5. Augmentasi hanya diterapkan pada data latih. Logika model dan preprocessing pada notebook tidak diubah untuk paket ini.

## Pengaturan pelatihan

| Pengaturan | Nilai |
|---|---|
| Optimizer | Adam |
| Learning rate awal | 0,01 |
| Scheduler | CyclicLR |
| Fungsi loss | Cross-entropy |
| Batch size | 32 |
| Maksimum epoch | 350 |
| Pemilihan checkpoint terbaik | Validation loss |
| Warm-up early stopping | 25 epoch |
| Patience | 60 epoch |
| Minimum improvement | 1e-4 |
| Seed | 42, 123, 456 |

Strict determinism dinonaktifkan secara default.

## Menjalankan notebook

1. Unduh dataset dari sumber Kaggle yang ditautkan pada README.
2. Siapkan struktur Google Drive dalam [panduan asli](original_source_guide.md): `MyDrive/Skripsi/model/data/videos/*.mp4` dan `data/splits/*.csv`.
3. Sediakan metadata dengan kolom `video_id`, misalnya `signer1_label0_sample0` tanpa ekstensi `.mp4`. **Metadata asli belum disertakan.** Notebook menggabungkan ID unik dari CSV tersebut, kemudian membentuk pembagian LOSO dan validasi internal. Untuk mereproduksi penelitian asli, gunakan metadata aslinya.
4. Buka `notebooks/01_pose_extraction.ipynb` di Colab. Sesuaikan `PROJECT_ROOT`, lalu jalankan sel berurutan untuk menghasilkan pose dan laporan kualitas. Notebook mengunduh aset model MediaPipe yang dibutuhkan.
5. Buka `notebooks/02_resgcn_loso_e0_e7.ipynb`. Periksa `ROOT`, `RUN_SEED`, `ACTIVE_EXPERIMENTS`, dan `AUTO_TRAIN`. Konfigurasi aktif default adalah E0; ulangi untuk konfigurasi dan seed lain sesuai kebutuhan.
6. Simpan catatan lingkungan, pembagian data, prediksi, metrik, dan checkpoint setiap proses pelatihan. Pastikan cache yang dipakai sesuai konfigurasi aktif.

`requirements.txt` memuat dependency asli tanpa penguncian versi. URL model MediaPipe menggunakan `latest`; perubahan versi package dan aset model dapat memengaruhi hasil. Catatan versi lingkungan dan hash aset asli diperlukan untuk reproduksi yang lebih ketat.

## Ketersediaan berkas

| Berkas | Status |
|---|---|
| Dua notebook penelitian | Tersedia, sama dengan arsip sumber |
| CSV hasil agregat | Tersedia, disalin dari tabel skripsi final |
| Skrip pembuatan grafik | Tersedia |
| Video dataset | Diunduh terpisah dari pemilik dataset |
| Metadata CSV asli | Belum disertakan; dibutuhkan kedua notebook |
| Cache pose dan laporan kualitas | Belum disertakan |
| Checkpoint, prediksi, dan log | Belum disertakan |
| Catatan versi lingkungan asli | Belum disertakan |
| Kode hand-anchor dan CLAHE | Belum disertakan |

## Pemeriksaan paket

Struktur JSON dan sintaks sel Python diperiksa tanpa menjalankan pelatihan. Hash notebook dicatat dalam `source_manifest.json`. Perhitungan rekap dari nilai seed diperiksa dengan toleransi pembulatan. Grafik ditinjau secara visual. Belum dilakukan pelatihan GPU, validasi seluruh dataset, pengukuran inferensi, atau reproduksi penuh pipeline.
