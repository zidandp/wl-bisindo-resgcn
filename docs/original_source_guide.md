# Source Code Skripsi

**Penulis:** Zidan Dwi Permana  
**Judul:** *Pengaruh Preprocessing Pose terhadap Performa dan Stabilitas ResGCN untuk Pengenalan Kata BISINDO Signer-Independent*  
**Program Studi:** Rekayasa Perangkat Lunak, Kampus UPI di Cibiru, Universitas Pendidikan Indonesia

Repository ini memuat pipeline penelitian untuk ekstraksi pose WL-BISINDO, preprocessing data pose, pelatihan ResGCN, dan evaluasi signer-independent menggunakan skema Leave-One-Signer-Out (LOSO).

## Dataset

Penelitian menggunakan **WL-BISINDO (Word-Level BISINDO)** yang diperkenalkan oleh:

- Grace Oktaviani Kindy
- Glenn Leonali
- Henry Lucky

dalam paper:

**Word-Level BISINDO: A Novel Video Indonesian Sign Language Dataset and Baseline Methods**  
*Procedia Computer Science*, Volume 269, 2025, Pages 249–258  
DOI: https://doi.org/10.1016/j.procs.2025.08.277

WL-BISINDO merupakan dataset video **Bahasa Isyarat Indonesia (BISINDO)** pada tingkat kata yang berfokus pada **varian regional Banten**. Dataset terdiri atas:

- 1.600 video RGB
- 32 isolated signs / kelas kosakata
- 5 signers

Dataset tersedia secara publik pada Kaggle:

https://www.kaggle.com/datasets/glennleonali/wl-bisindo

Dataset WL-BISINDO didistribusikan dengan lisensi **CC BY-NC 4.0**, sehingga penggunaannya dibatasi untuk tujuan non-komersial dan memerlukan atribusi kepada pembuat dataset.

Dataset tidak disertakan di dalam repository source code ini. Pengguna perlu mengunduh WL-BISINDO secara terpisah dari sumber resminya.

## Isi Repository

```text
Source_Code_Skripsi_Zidan_Dwi_Permana/
├── README.md
├── requirements.txt
├── 01_pose_extraction.ipynb
└── 02_resgcn_loso_e0_e7.ipynb
```

### `01_pose_extraction.ipynb`

Mengekstraksi video RGB WL-BISINDO menjadi sequence pose mentah menggunakan MediaPipe Pose Landmarker dan Hand Landmarker.

Setiap frame direpresentasikan menggunakan **65 keypoint**:

- 21 keypoint tangan kiri
- 21 keypoint tangan kanan
- 11 keypoint kepala/wajah
- 12 keypoint tubuh bagian atas

Output setiap video disimpan dalam format:

```text
(T, 65, 2)
```

dengan `T` sebagai jumlah frame asli video dan `2` sebagai koordinat `x` dan `y`.

Keypoint yang tidak terdeteksi disimpan sebagai `(0, 0)`. Notebook juga menghasilkan laporan quality control untuk panjang sequence dan proporsi missing keypoint.

### `02_resgcn_loso_e0_e7.ipynb`

Menjalankan pipeline preprocessing, pembagian LOSO, graph construction, pelatihan ResGCN, evaluasi model, serta rekap hasil eksperimen E0–E7.

Notebook mencakup:

- signer-independent LOSO
- internal validation split
- linear interpolation
- spatial normalization
- temporal standardization menjadi 64 frame
- pose augmentation
- graph construction 65 node
- ResGCN_N39_R4
- checkpoint dan resume training
- classification report
- confusion matrix
- rekap metrik per fold
- analisis main effect faktor preprocessing

## Struktur Data

Struktur Google Drive yang digunakan:

```text
MyDrive/Skripsi/model/
└── data/
    ├── videos/
    │   └── *.mp4
    ├── splits/
    │   └── *.csv
    └── data_pose_raw/
        └── *.npz
```

Folder `data_pose_raw/` dihasilkan oleh notebook `01_pose_extraction.ipynb`.

## Urutan Menjalankan Pipeline

### 1. Siapkan Dataset

Unduh WL-BISINDO dari Kaggle dan tempatkan video pada:

```text
MyDrive/Skripsi/model/data/videos/
```

Siapkan metadata split pada:

```text
MyDrive/Skripsi/model/data/splits/
```

Metadata yang digunakan oleh notebook harus memiliki kolom `video_id`.

### 2. Ekstraksi Pose

Jalankan:

```text
01_pose_extraction.ipynb
```

Output utama:

```text
data/data_pose_raw/*.npz
data/configs/joints65.yaml
data/reports/pose_qc.csv
data/reports/pose_qc_by_signer.csv
data/reports/pose_qc_by_label.csv
```

Raw pose tetap mempertahankan panjang sequence asli `(T, 65, 2)`. Standardisasi menjadi 64 frame dilakukan pada tahap preprocessing di notebook training.

### 3. Pilih Random Seed

Pada `02_resgcn_loso_e0_e7.ipynb`, tentukan:

```python
RUN_SEED = 42
```

Tiga seed yang digunakan pada eksperimen penelitian adalah:

```text
42
123
456
```

### 4. Pilih Eksperimen

Contoh menjalankan satu konfigurasi:

```python
ACTIVE_EXPERIMENTS = ["E0"]
```

Untuk seluruh E0–E7:

```python
ACTIVE_EXPERIMENTS = [
    "E0", "E1", "E2", "E3",
    "E4", "E5", "E6", "E7"
]
```

Output setiap seed disimpan secara terpisah:

```text
runs/loso_e0_e7_multiseed/
├── seed_42/
├── seed_123/
└── seed_456/
```

## Skenario Signer-Independent

Evaluasi utama menggunakan empat fold LOSO:

| Fold | Test signer |
|---|---:|
| Fold 1 | Signer 1 |
| Fold 2 | Signer 2 |
| Fold 3 | Signer 3 |
| Fold 4 | Signer 4 |

Pada setiap fold, test signer tidak digunakan pada proses training maupun internal validation.

Signer 0 tetap berada pada training pool karena cakupan labelnya tidak memenuhi seluruh 32 kelas untuk digunakan sebagai test fold.

Sebanyak **15%** kandidat data latih dipisahkan sebagai internal validation menggunakan label-stratified sampling.

## Desain Eksperimen E0–E7

Tiga faktor preprocessing diuji menggunakan desain faktorial 2³:

| Eksperimen | Interpolasi | Normalisasi | Augmentasi |
|---|---|---|---|
| E0 | Tidak | Tidak | Tidak |
| E1 | Ya | Tidak | Tidak |
| E2 | Tidak | Ya | Tidak |
| E3 | Tidak | Tidak | Ya |
| E4 | Ya | Ya | Tidak |
| E5 | Ya | Tidak | Ya |
| E6 | Tidak | Ya | Ya |
| E7 | Ya | Ya | Ya |

Standardisasi temporal menjadi 64 frame diterapkan pada seluruh eksperimen dan bukan merupakan faktor pembanding.

## Preprocessing

### Linear Interpolation

Interpolasi digunakan untuk mengisi missing keypoint pada bagian tengah sequence apabila terdapat koordinat valid sebelum dan sesudah titik yang hilang.

### Spatial Normalization

Pose ditranslasikan terhadap pusat tubuh dan diskalakan berdasarkan rata-rata jarak bahu. Keypoint yang tetap tidak valid dikembalikan ke `(0, 0)`.

### Temporal Standardization

Setiap sequence distandardisasi menjadi:

```text
64 frame
```

sehingga representasi sebelum masuk model memiliki bentuk:

```text
(64, 65, 2)
```

dan kemudian diubah menjadi:

```text
(2, 64, 65)
```

### Pose Augmentation

Augmentasi hanya diterapkan pada data `train_fit`:

- random rotation ±10°, probability 0.5
- Gaussian spatial jitter dengan σ = 0.015, probability 0.5

Data internal validation dan test tidak diaugmentasi.

## Model dan Training

Konfigurasi utama:

| Komponen | Nilai |
|---|---|
| Model | ResGCN_N39_R4 |
| Jumlah kelas | 32 |
| Input | 2 × 64 × 65 |
| Batch size | 32 |
| Maximum epoch | 350 |
| Optimizer | Adam |
| Initial learning rate | 0.01 |
| Scheduler | CyclicLR |
| Loss | Cross-entropy loss |
| Early stopping warm-up | 25 epoch |
| Patience | 60 epoch |
| Minimum improvement | 1e-4 |
| Best model criterion | Validation loss |

Model menghasilkan prediksi terhadap 32 kelas kosakata BISINDO.

## Repeated Runs

Eksperimen E0–E7 dijalankan dengan tiga random seed:

```text
42
123
456
```

Dengan 8 konfigurasi dan 4 LOSO fold, keseluruhan eksperimen utama terdiri atas:

```text
3 seeds × 8 experiments × 4 folds = 96 training runs
```

Seed memengaruhi inisialisasi model, internal validation split, urutan training, dan augmentasi acak.

## Reproducibility

Notebook menyimpan informasi yang diperlukan untuk menelusuri setiap eksperimen, termasuk:

- random seed
- konfigurasi eksperimen
- versi package dan runtime
- internal train/validation/test split
- konfigurasi preprocessing
- training log
- checkpoint
- test predictions
- classification report
- confusion matrix
- runtime log

`STRICT_DETERMINISM=False` digunakan sebagai konfigurasi default untuk training. Karena sebagian operasi CUDA dapat bersifat nondeterministik, rerun pada hardware atau runtime yang berbeda dapat menghasilkan variasi numerik kecil meskipun random seed sama.

## Dependencies

Dependency utama tersedia pada `requirements.txt`.

Instalasi dapat dilakukan dengan:

```bash
pip install -r requirements.txt
```

Google Colab direkomendasikan karena pipeline training menggunakan GPU.

## Citation Dataset

Jika menggunakan WL-BISINDO, sitasi dataset/paper asli:

```bibtex
@article{KINDY2025249,
  title   = {Word-Level BISINDO: A Novel Video Indonesian Sign Language Dataset and Baseline Methods},
  journal = {Procedia Computer Science},
  volume  = {269},
  pages   = {249--258},
  year    = {2025},
  doi     = {10.1016/j.procs.2025.08.277},
  author  = {Grace Oktaviani Kindy and Glenn Leonali and Henry Lucky}
}
```

## License dan Attribution

Source code penelitian ini menggunakan WL-BISINDO sebagai dataset penelitian. Hak atas dataset tetap dimiliki oleh pembuat WL-BISINDO dan mengikuti lisensi **CC BY-NC 4.0**.

Implementasi penelitian ini tidak mendistribusikan ulang video WL-BISINDO di dalam repository.
