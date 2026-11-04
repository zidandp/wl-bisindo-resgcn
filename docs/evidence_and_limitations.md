# Hasil dan keterbatasan

## Sumber angka

| Berkas | Isi |
|---|---|
| [`main_results.csv`](../results/main_results.csv) | Akurasi per seed, rata-rata, SD, dan F1 tertimbang untuk E0–E7 |
| [`main_effects.csv`](../results/main_effects.csv) | Main effect interpolasi, normalisasi, dan augmentasi |
| [`e7_signer_results.csv`](../results/e7_signer_results.csv) | Akurasi E7 per signer uji |

Semua angka adalah rekap dari tabel skripsi. Prediksi, checkpoint, dan log per-run tidak disertakan. Karena angka sudah dibulatkan, menghitung ulang bisa menghasilkan selisih kecil.

## Cara membaca metrik

- **Skor per seed:** rata-rata tanpa pembobotan dari empat fold LOSO, sehingga setiap signer uji berbobot sama meskipun jumlah videonya berbeda. Skor ini bukan akurasi dari gabungan seluruh prediksi uji.
- **Rata-rata dan SD:** dihitung dari tiga skor seed (SD sampel).
- **SD menunjukkan variasi antar-pengulangan.** Karena seed juga mengubah pembagian validasi internal, variasi ini tidak hanya berasal dari inisialisasi model. SD bukan variasi antar-signer, interval kepercayaan, atau bukti signifikansi.
- **F1 tertimbang:** dihitung per fold dengan bobot jumlah contoh tiap kelas, lalu dirata-ratakan antar-fold.
- **Main effect:** rata-rata selisih skor saat suatu faktor aktif dibandingkan nonaktif, pada semua kombinasi faktor lain. Nilainya tidak bisa dijumlahkan untuk memprediksi kenaikan E0 → E7 karena faktor dapat berinteraksi.

## Yang didukung hasil

- Pada arsitektur dan protokol yang diuji, menggabungkan ketiga teknik (E7) memberikan akurasi rata-rata tertinggi di antara E0–E7.
- Normalisasi spasial memberikan main effect terbesar.
- Kenaikan E7 terhadap E0 (34,58 poin persentase) dihitung terhadap baseline internal dengan protokol yang sama.
- Performa sangat berbeda antar-signer; signer 3 paling rendah dan paling bervariasi.

## Yang belum dibuktikan

**Generalisasi**
- Hasil belum diuji pada pengguna BISINDO lain, isyarat kontinu, varian regional, kondisi kamera baru, atau dataset lain.
- Hanya ada empat signer uji, dan semua konfigurasi dibandingkan pada signer yang sama. E7 dipilih dari perbandingan tersebut; belum ada set uji eksternal untuk mengonfirmasinya.
- Belum ada uji signifikansi statistik antar-konfigurasi. Selisih yang kecil, seperti E6 dan E7, perlu dibaca hati-hati.

**Perbandingan dengan penelitian lain**
- Angka ini tidak menyatakan keunggulan atas metode di publikasi lain, termasuk baseline pada paper dataset, karena protokolnya berbeda.

**Penyebab performa signer 3**
- Belum ada satu penjelasan kausal yang terbukti. Jumlah keypoint hilang saja tidak cukup menjelaskannya. Kualitas ekstraksi, karakteristik gerakan, dan representasi pose perlu diperiksa bersama.
- Hasil ini tidak menunjukkan bahwa dataset keliru.

**Aspek sistem**
- Belum ada pengukuran waktu inferensi, FPS, atau FLOPs. Yang tersedia hanya jumlah parameter model.
- Penelitian ini tidak membangun aplikasi atau prototipe real-time.
- Input hanya pose 2D dari video RGB; data kedalaman (RGB-D) tidak digunakan.

## Reproduksi

Notebook sudah bisa dikonfigurasi untuk folder milik pengguna, tetapi pelatihan penuh belum dijalankan ulang dengan versi ini. Kebutuhan data, lingkungan, dan artefak yang belum tersedia dijelaskan di [panduan menjalankan](methods_and_reproduction.md).
