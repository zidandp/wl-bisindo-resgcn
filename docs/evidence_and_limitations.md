# Sumber hasil dan keterbatasan

## Sumber angka

Hasil dalam repository mengikuti skripsi final. Slide sidang masih memuat hasil satu seed, termasuk E7 sebesar 73,09% dan hand-anchor sekitar 78,8%, sehingga tidak digunakan sebagai ringkasan hasil tiga seed.

| Informasi | Lokasi dalam skripsi final |
|---|---|
| 96 proses pelatihan, empat fold, tiga seed | Bagian 4.4, halaman tercetak 68–69 |
| Top-1 E0–E7, SD, dan nilai tiap seed | Tabel 4.8, halaman tercetak 69 / halaman PDF 84 |
| Precision, recall, dan F1 tertimbang | Tabel 4.9 |
| Main effect | Tabel 4.10 |
| Hasil E7 per signer dan hand-anchor | Tabel 4.13 |
| Kesimpulan | Bab V, halaman tercetak 96–98 |

Berkas `results/*.csv` merupakan salinan tabel agregat skripsi, bukan log mentah hasil pelatihan. Perhitungan ulang dari angka yang telah dibulatkan dapat menghasilkan selisih kecil.

## Ruang lingkup kesimpulan

Eksperimen menunjukkan manfaat normalisasi spasial pada konfigurasi ResGCN dan evaluasi WL-BISINDO yang digunakan. Pengujian belum mencakup semua pengguna BISINDO, isyarat kontinu, varian regional lain, kondisi kamera baru, maupun dataset lain.

Delapan konfigurasi dibandingkan pada empat signer uji yang sama. Konfigurasi terbaik ditentukan setelah hasil perbandingan diperoleh; belum ada set uji eksternal independen untuk mengonfirmasi pilihan tersebut. Pengujian lanjutan yang didorong analisis kesalahan bersifat eksploratif. SD yang dilaporkan bukan hasil uji signifikansi statistik.

Performa signer 3 yang lebih rendah belum memiliki satu penjelasan kausal yang terbukti. Jumlah keypoint hilang, karakteristik gerakan, dan representasi pose perlu diperiksa bersama.

## Berkas publik

Repository menyertakan kode dan dokumentasi penelitian tanpa PDF skripsi bertanda tangan, slide sidang, video dataset, atau isi Drive pribadi. Notebook dan panduan sumber asli dipertahankan. Atribusi metode tersedia di [referensi](references.md); kebutuhan menjalankan kode tersedia di [panduan reproduksi](methods_and_reproduction.md).
