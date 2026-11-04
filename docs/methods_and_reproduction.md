# Metode dan cara menjalankan

Dokumen ini menjelaskan pengolahan pose, pengaturan pelatihan, dan langkah menjalankan notebook. Dasar pemilihan metode ada di [referensi](references.md).

## 1. Pengolahan pose

### Ekstraksi
- Frame video dibaca dengan OpenCV dan dikonversi dari BGR ke RGB.
- MediaPipe Pose Landmarker dan Hand Landmarker dijalankan secara terpisah, lalu hasilnya digabung menjadi sekuens `(T, 65, 2)` (T = jumlah frame).
- Keypoint yang tidak terdeteksi disimpan sebagai `(0, 0)`.

### Interpolasi (faktor eksperimen)
- Interpolasi linear mengisi keypoint yang hilang **di tengah** sekuens, jika ada pengamatan valid sebelum dan sesudahnya.
- Keypoint yang hilang di awal atau akhir sekuens tidak diekstrapolasi.

### Normalisasi spasial (faktor eksperimen)
- **Pusat:** mid-hip. Jika tidak tersedia, dipakai pusat pinggul, pusat bahu, atau rata-rata keypoint valid, sesuai urutan tersebut.
- **Skala:** rata-rata jarak bahu yang valid.
- Titik yang tetap tidak valid dikembalikan ke nol.

### Augmentasi (faktor eksperimen, hanya data latih)
- Rotasi ±10 derajat, peluang 0,5.
- Gaussian jitter sigma 0,015, peluang 0,5.

### Standardisasi temporal (semua konfigurasi)
- Setiap sekuens diubah menjadi 64 frame. Koordinat di-resample secara linear; mask validitas memakai nearest neighbor.
- Langkah ini **bukan** faktor eksperimen dan berbeda dari interpolasi keypoint yang hilang.

## 2. Pengaturan pelatihan

| Pengaturan | Nilai |
|---|---|
| Model | `ResGCN_N39_R4` (460.276 parameter, dilaporkan di skripsi) |
| Optimizer | Adam |
| Learning rate | CyclicLR antara 0,001 dan 0,01; diperbarui setiap batch, fase naik 5 epoch |
| Loss | Cross-entropy |
| Batch size | 32 |
| Maksimum epoch | 350 |
| Checkpoint terbaik | Berdasarkan validation loss |
| Early stopping | Warm-up 25 epoch, patience 60 epoch, minimum improvement 1e-4 |
| Seed | 42, 123, 456 |
| Hardware asli | Google Colab, GPU NVIDIA Tesla T4 |

Catatan:
- Optimizer dibuat dengan `lr=0.01`, tetapi `CyclicLR` mengatur learning rate dari `base_lr=0.001` sampai `max_lr=0.01`. Nilai 0,01 adalah batas atas siklus.
- Seed juga menentukan pembagian validasi internal. Jadi variasi antar-seed mencakup perbedaan pembagian data dan proses pelatihan.
- Strict determinism dinonaktifkan secara default, sehingga hasil run ulang bisa sedikit berbeda.

## 3. Menjalankan notebook

**Persiapan**
1. Unduh dataset dari [Kaggle](https://www.kaggle.com/datasets/glennleonali/wl-bisindo) dan ekstrak videonya ke folder mana pun (subfolder didukung).
2. Instal dependency: `pip install -r requirements.txt`.
3. Tentukan folder kerja `PROJECT_ROOT` di sel konfigurasi **kedua** notebook (harus sama), atau lewat environment variable `WLBISINDO_ROOT`. Default: `~/wl-bisindo-workspace`.
   - Contoh Windows: `D:/penelitian/wl-bisindo-workspace`
   - Contoh Colab: `/content/drive/MyDrive/wl-bisindo-workspace`

**Notebook 1: ekstraksi pose**
1. Atur `VIDEO_DIR` (default `PROJECT_ROOT/data/videos`). Aktifkan `USE_GOOGLE_DRIVE` hanya jika memakai Drive di Colab.
2. Jalankan semua sel secara berurutan.
3. Jika belum ada CSV di `data/splits`, notebook membuat `video_inventory.csv` dari nama berkas dengan pola `signerN_labelK_sampleI.mp4`. Nama yang tidak sesuai pola dan ID duplikat akan ditolak.

**Notebook 2: pelatihan dan evaluasi**
1. Pakai `PROJECT_ROOT` yang sama.
2. Periksa `RUN_SEED`, `ACTIVE_EXPERIMENTS`, dan `AUTO_TRAIN`.
3. Notebook membentuk fold LOSO dan validasi internal dari inventaris, lalu melatih dan mengevaluasi model.

**Lokasi keluaran** (di bawah `PROJECT_ROOT`)

| Folder | Isi |
|---|---|
| `data/data_pose_raw` | Hasil ekstraksi pose |
| `data/reports` | Laporan kualitas pose |
| `data/experiments_e0_e7_multiseed` | Artefak preprocessing |
| `runs/loso_e0_e7_multiseed` | Checkpoint, log, prediksi, confusion matrix, `environment.json` |
| `cache` | Cache kerja |

Tips:
- Gunakan workspace baru jika mengganti dataset.
- Penyimpanan lokal Colab akan hilang saat runtime berakhir; simpan ke Drive atau salin hasil sebelum itu.

## 4. Faktor yang memengaruhi reproduksi

- **Versi package:** `requirements.txt` tidak mengunci versi. Notebook mencatat versi aktual ke berkas JSON saat dijalankan, tetapi catatan dari run asli tidak disertakan.
- **Model MediaPipe:** URL model memakai versi `latest`, sehingga aset model bisa berubah dari waktu ke waktu.
- **Inventaris data:** inventaris yang dibuat ulang dari nama video belum tentu sama persis dengan metadata yang dipakai saat penelitian.

## Ketersediaan berkas

| Berkas | Status |
|---|---|
| Dua notebook penelitian | ✅ Tersedia (lokasi input/output dan inventaris disesuaikan) |
| CSV rekap hasil dan skrip grafik | ✅ Tersedia |
| Video dataset | ⬇️ Unduh dari pemilik dataset |
| Metadata CSV asli | ❌ Belum disertakan (inventaris baru bisa dibuat dari video) |
| Cache pose dan laporan kualitas | ❌ Belum disertakan |
| Checkpoint, prediksi, dan log per-run | ❌ Belum disertakan |
| Catatan versi lingkungan asli | ❌ Belum disertakan |

## Pemeriksaan yang sudah dilakukan pada paket ini

Sudah:
- Struktur JSON notebook dan sintaks seluruh sel kode.
- Pembuatan inventaris dengan folder video bertingkat sintetis dan ID duplikat.
- Rekap rata-rata/SD dari nilai per seed, dengan toleransi pembulatan.
- Tidak ada path folder pribadi di notebook dan dokumentasi.
- Hash notebook asli dan hasil penyesuaian dicatat di [`source_manifest.json`](source_manifest.json).

Belum:
- Ekstraksi MediaPipe pada seluruh dataset dan pelatihan GPU dengan versi notebook ini.
- Reproduksi penuh angka hasil.
- Pengukuran waktu inferensi, FPS, atau FLOPs.
