# Pembacaan hasil dan keterbatasan

## Rekap eksperimen

| Berkas | Isi |
|---|---|
| [`main_results.csv`](../results/main_results.csv) | Konfigurasi E0–E7, akurasi per seed, rata-rata, SD, dan F1 tertimbang |
| [`main_effects.csv`](../results/main_effects.csv) | Efek utama interpolasi, normalisasi, dan augmentasi |
| [`e7_signer_results.csv`](../results/e7_signer_results.csv) | Akurasi E7 pada setiap signer uji |

CSV tersebut berisi rekap tabel hasil eksperimen. Prediksi, checkpoint, dan log per-run belum disertakan. Angka yang sudah dibulatkan dapat menimbulkan selisih kecil ketika dihitung ulang.

## Cara membaca metrik

Untuk setiap seed, skor merupakan rata-rata tanpa pembobotan dari empat fold LOSO. Rata-rata akhir dan simpangan baku sampel (SD) dihitung dari tiga skor seed. Setiap signer uji memiliki bobot sama meskipun jumlah videonya berbeda; skor ini bukan akurasi dari penggabungan seluruh prediksi uji. F1 tertimbang memperhitungkan jumlah contoh tiap kelas di dalam fold, lalu dirata-ratakan antar-fold.

SD menggambarkan variasi antar-pengulangan. Seed juga mengubah pembagian validasi internal, sehingga variasi ini tidak hanya berasal dari inisialisasi model. SD bukan ukuran variasi antar-signer, interval kepercayaan, atau bukti signifikansi statistik.

Peningkatan E7 terhadap E0 sebesar 34,58 poin persentase menggunakan baseline internal dengan protokol yang sama. Nilai ini tidak menyatakan keunggulan terhadap metode pada publikasi lain.

Main effect adalah rata-rata selisih skor ketika suatu faktor aktif dan nonaktif pada kombinasi faktor lain. Nilai main effect tidak dapat dijumlahkan langsung untuk memprediksi peningkatan E0 ke E7 karena perlakuan dapat berinteraksi.

## Ruang lingkup kesimpulan

Normalisasi spasial memberikan main effect terbesar pada arsitektur dan protokol WL-BISINDO yang diuji. Hasil belum mencakup semua pengguna BISINDO, isyarat kontinu, varian regional lain, kondisi kamera baru, maupun dataset lain.

Delapan konfigurasi dibandingkan pada empat signer uji yang sama. E7 dipilih berdasarkan hasil perbandingan tersebut; belum ada set uji eksternal independen untuk mengonfirmasi pilihan ini. Hand-anchor dan CLAHE merupakan pengujian eksploratif setelah analisis kesalahan, sehingga bukan validasi independen atas konfigurasi terpilih.

Performa signer 3 yang lebih rendah belum memiliki satu penjelasan kausal yang terbukti. Jumlah keypoint hilang saja belum cukup menjelaskannya. Kualitas ekstraksi, karakteristik gerakan, dan representasi pose perlu diperiksa bersama; hasil ini tidak membuktikan bahwa dataset keliru.

## Reproduksi

Notebook menyediakan konfigurasi lokasi input dan output untuk pengguna. Pelatihan penuh belum dijalankan ulang pada versi notebook ini. Kebutuhan data, lingkungan, dan artefak yang belum tersedia dijelaskan dalam [panduan menjalankan](methods_and_reproduction.md).
