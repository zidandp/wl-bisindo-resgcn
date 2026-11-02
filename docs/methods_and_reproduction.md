# Metode dan cara menjalankan

Rujukan arsitektur dan preprocessing dijelaskan dalam [daftar referensi](references.md).

## Pengolahan pose

Video diproses dengan MediaPipe Pose Landmarker dan Hand Landmarker secara terpisah. Setiap video menghasilkan sekuens `(T,65,2)`, dengan T sebagai jumlah frame. Keypoint yang tidak terdeteksi disimpan sebagai `(0,0)`.

Interpolasi linear mengisi titik hilang di tengah sekuens apabila terdapat pengamatan valid sebelum dan sesudahnya. Titik hilang pada batas awal atau akhir tidak diekstrapolasi. Normalisasi menggunakan pusat mid-hip; jika tidak tersedia, digunakan pusat pinggul, bahu, atau rata-rata keypoint valid. Skala dibagi dengan rata-rata jarak bahu valid. Titik yang tetap tidak valid dikembalikan ke nol.

Semua konfigurasi distandardisasi menjadi 64 frame. Koordinat di-resample secara linear dan mask validitas menggunakan nearest neighbor. Proses ini berbeda dari interpolasi titik hilang yang menjadi faktor eksperimen.

Augmentasi berupa rotasi ±10 derajat dan Gaussian jitter dengan sigma 0,015, masing-masing berpeluang 0,5. Augmentasi hanya diterapkan pada data latih. Perubahan portabilitas mencakup lokasi penyimpanan dan inventaris video; perhitungan model dan preprocessing dipertahankan.

## Pengaturan pelatihan

| Pengaturan | Nilai |
|---|---|
| Optimizer | Adam |
| Rentang learning rate | 0,001–0,01 |
| Scheduler | CyclicLR; diperbarui setiap batch, fase naik sepanjang 5 epoch |
| Fungsi loss | Cross-entropy |
| Batch size | 32 |
| Maksimum epoch | 350 |
| Pemilihan checkpoint terbaik | Validation loss |
| Warm-up early stopping | 25 epoch |
| Patience | 60 epoch |
| Minimum improvement | 1e-4 |
| Seed | 42, 123, 456 |

Optimizer dibuat dengan `lr=0.01`, lalu `CyclicLR` mengatur learning rate mulai dari `base_lr=0.001` hingga `max_lr=0.01`. Jadi, 0,01 merupakan batas atas siklus, bukan learning rate efektif pada awal pelatihan.

Seed juga memengaruhi pembagian validasi internal. Variasi hasil antar-seed mencakup perubahan pembagian tersebut serta proses pelatihan. Strict determinism dinonaktifkan secara default.

## Menjalankan notebook

1. Unduh dan ekstrak dataset. Simpan video dalam folder pilihanmu; subfolder didukung.
2. Pada sel konfigurasi kedua notebook, atur `PROJECT_ROOT` ke folder kerja yang sama. Contoh: `D:/penelitian/wl-bisindo-workspace` untuk Windows atau `/content/drive/MyDrive/wl-bisindo-workspace` untuk Drive di Colab. Nilai default adalah `~/wl-bisindo-workspace`. Environment variable `WLBISINDO_ROOT` juga dapat digunakan.
3. Pada notebook ekstraksi, atur `VIDEO_DIR` ke folder video. Default: `PROJECT_ROOT/data/videos`. Aktifkan `USE_GOOGLE_DRIVE` hanya jika memakai Drive pada Colab.
4. Jalankan notebook ekstraksi berurutan. Jika belum ada CSV di `data/splits`, notebook membuat `video_inventory.csv` dari nama video. Pola nama harus `signerN_labelK_sampleI.mp4`; nama tidak valid dan ID duplikat ditolak. Inventaris baru tidak menjamin kesamaan dengan metadata historis penelitian.
5. Jalankan notebook pelatihan dengan `PROJECT_ROOT` yang sama. Periksa `RUN_SEED`, `ACTIVE_EXPERIMENTS`, dan `AUTO_TRAIN`. Notebook membentuk pembagian LOSO serta validasi internal dari inventaris tersebut.
6. Hasil ekstraksi tersimpan di `data/data_pose_raw`, laporan di `data/reports`, artefak preprocessing di `data/experiments_e0_e7_multiseed`, dan hasil pelatihan di `runs/loso_e0_e7_multiseed`. Cache kerja berada di `cache`, semuanya di bawah `PROJECT_ROOT`.

Gunakan workspace baru jika mengganti dataset. Di Colab, penyimpanan lokal bersifat sementara; pilih folder Drive atau salin hasil sebelum runtime berakhir. Path pada contoh bukan akses ke Drive penulis.

`requirements.txt` memuat dependency asli tanpa penguncian versi. URL model MediaPipe menggunakan `latest`; perubahan versi package dan aset model dapat memengaruhi hasil. Catatan versi lingkungan dan hash aset asli diperlukan untuk reproduksi yang lebih ketat.

## Ketersediaan berkas

| Berkas | Status |
|---|---|
| Dua notebook penelitian | Tersedia, konfigurasi lokasi dan inventaris input telah disesuaikan |
| CSV hasil agregat | Tersedia sebagai rekap hasil eksperimen |
| Skrip pembuatan grafik | Tersedia |
| Video dataset | Diunduh terpisah dari pemilik dataset |
| Metadata CSV asli | Metadata historis belum disertakan; inventaris baru dapat dibuat dari video |
| Cache pose dan laporan kualitas | Belum disertakan |
| Checkpoint, prediksi, dan log | Belum disertakan |
| Catatan versi lingkungan asli | Belum disertakan |
| Kode hand-anchor dan CLAHE | Belum disertakan |

## Pemeriksaan paket

Struktur JSON dan sintaks sel Python diperiksa tanpa menjalankan pelatihan. Hash sumber asli dan notebook hasil penyesuaian dicatat dalam `source_manifest.json`. Perhitungan rekap dari nilai seed diperiksa dengan toleransi pembulatan. Grafik ditinjau secara visual. Belum dilakukan pelatihan GPU, validasi seluruh dataset, pengukuran inferensi, atau reproduksi penuh pipeline.
