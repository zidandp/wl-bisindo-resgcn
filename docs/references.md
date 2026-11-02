# Referensi dan kaitannya dengan implementasi

Pemetaan ini mengikuti kajian pustaka, metode, dan daftar pustaka skripsi. Rujukan ilmiah dibedakan dari sumber kode. Rincian bibliografi mengikuti skripsi; belum seluruh publikasi asli diperiksa ulang untuk paket ini.

## Arsitektur

N. Naz, H. Sajid, S. Ali, O. Hasan and M. K. Ehsan. 2023. **Signgraph: An Efficient and Accurate Pose-Based Graph Convolution Approach Toward Sign Language Recognition.** IEEE Access, 11, 19135–19147. https://doi.org/10.1109/ACCESS.2023.3247761

SIGNGRAPH menjadi acuan arsitektur implementasi `ResGCN_N39_R4`. Bagian 3.3.7 skripsi menyatakan bahwa source code asli SIGNGRAPH tidak digunakan secara langsung. Model memuat graph convolution spasial, convolution temporal, residual connection, dan blok bottleneck.

## Preprocessing

Kyunggeun Roh, Huije Lee, Eui Jun Hwang, Sukmin Cho, and Jong C. Park. 2024. **Preprocessing Mediapipe Keypoints with Keypoint Reconstruction and Anchors for Isolated Sign Language Recognition.** Proceedings of the LREC-COLING 2024 11th Workshop on the Representation and Processing of Sign Languages: Evaluation of Sign Language Resources, 323–334. ELRA and ICCL. https://aclanthology.org/2024.signlang-1.36/

Roh dkk. menjadi rujukan rekonstruksi keypoint dan normalisasi berbasis anchor. Pada kode utama penelitian ini, `interpolate_missing_keypoints` menggunakan `np.interp` untuk celah temporal internal, sedangkan `normalize_spatial` menggunakan pusat mid-hip dengan mekanisme pengganti dan skala jarak bahu. Implementasi ini tidak dinyatakan identik dengan seluruh pipeline Roh. Pengujian hand-anchor merupakan eksperimen tambahan terpisah.

## Dataset

Grace Oktaviani Kindy, Glenn Leonali and Henry Lucky. 2025. **Word-Level BISINDO: A Novel Video Indonesian Sign Language Dataset and Baseline Methods.** Procedia Computer Science, 269, 249–258. https://doi.org/10.1016/j.procs.2025.08.277

Sumber dataset: https://www.kaggle.com/datasets/glennleonali/wl-bisindo


## Landasan model graf

- **Song, Y.-F., Zhang, Z., Shan, C., & Wang, L. (2020).** Stronger, Faster and More Explainable: A Graph Convolutional Baseline for Skeleton-based Action Recognition. ACM Multimedia, 1625–1633. https://doi.org/10.1145/3394171.3413802 — Landasan ResGCN yang dibahas bersama SIGNGRAPH pada bagian 2.4.3.

- **Yan, S., Xiong, Y., & Lin, D. (2018).** Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action Recognition. AAAI, 32(1). https://doi.org/10.1609/aaai.v32i1.12328 — Landasan ST-GCN dalam kajian model graf.


## Ekstraksi dan kualitas pose

- **Lugaresi, C., et al. (2019).** MediaPipe: A Framework for Building Perception Pipelines. — Rujukan framework MediaPipe. Implementasi memakai Tasks Pose dan Hand Landmarker.

- **Moryossef, A., et al. (2021).** Evaluating the Immediate Applicability of Pose Estimation for Sign Language Recognition. CVPRW, 3429–3435. https://doi.org/10.1109/CVPRW53098.2021.00382 — Rujukan pembahasan kualitas pose dan keypoint yang tidak terdeteksi.


## Dasar pemilihan preprocessing dan studi pembanding

- **Bohacek, M., & Hruz, M. (2022).** Sign Pose-based Transformer for Word-level Sign Language Recognition. WACVW, 182–191. https://doi.org/10.1109/WACVW54805.2022.00024 — SPOTER; konteks normalisasi dan preprocessing pose.

- **De Coster, M., Van Herreweghe, M., & Dambre, J. (2020).** Sign Language Recognition with Transformer Networks. — Konteks preprocessing dan augmentasi. Detail venue tidak lengkap dalam daftar pustaka skripsi.

- **Akdag, A., & Baykan, O. K. (2024).** Isolated sign language recognition through integrating pose data and motion history images. PeerJ Computer Science, 10. https://doi.org/10.7717/PEERJ-CS.2054 — Metode berbasis pose yang dibahas dalam sintesis pada halaman 35.

- **Purbojo, T., & Wijaya, A. P. (2025).** Enhancing Pose-Based Sign Language Recognition: A Comparative Study of Preprocessing Strategies with GRU and LSTM. Advance Sustainable Science, Engineering and Technology, 7(2). https://doi.org/10.26877/asset.v7i2.1658 — Studi pembanding untuk menguji kembali preprocessing pada arsitektur berbeda.

- **Jiang, S., et al. (2021).** Skeleton Aware Multi-modal Sign Language Recognition. CVPRW, 3408–3418. https://doi.org/10.1109/CVPRW53098.2021.00380 — Kajian SLR berbasis skeleton dalam pertimbangan preprocessing.

- **Cormier, M., Schmid, Y., & Beyerer, J. (2024).** Enhancing Skeleton-Based Action Recognition in Real-World Scenarios Through Realistic Data Augmentation. WACVW, 300–309. https://doi.org/10.1109/WACVW60836.2024.00038 — Literatur pendukung augmentasi; bukan sumber seluruh nilai parameter augmentasi penelitian.


## Desain eksperimen dan evaluasi

- **Montgomery, D. C. (2013).** Design and Analysis of Experiments. John Wiley & Sons. — Dasar desain faktorial dan interpretasi efek.

- **Andrade, C. (2024).** Understanding Factorial Designs, Main Effects, and Interaction Effects: Simply Explained with a Worked Example. Indian Journal of Psychological Medicine, 46(2), 175–177. https://doi.org/10.1177/02537176241237066 — Pembahasan main effect dan interaksi.

- **Baker, T. B., et al. (2017).** Implementing Clinical Research Using Factorial Designs: A Primer. Behavior Therapy, 48(4), 567–580. https://doi.org/10.1016/j.beth.2016.12.005 — Landasan umum desain faktorial, bukan sumber implementasi computer vision.

- **Sokolova, M., & Lapalme, G. (2009).** A systematic analysis of performance measures for classification tasks. Information Processing & Management, 45(4), 427–437. https://doi.org/10.1016/j.ipm.2009.03.002 — Interpretasi metrik klasifikasi.

- **Powers, D. M. W. (2020).** Evaluation: from precision, recall and F-measure to ROC, informedness, markedness and correlation. — Rujukan evaluasi sebagaimana tercantum dalam skripsi.


## Batas atribusi

Halaman 34–35 skripsi menjelaskan bahwa pemilihan preprocessing mempertimbangkan beberapa studi, bukan mengadopsi satu pipeline secara utuh. Daftar di atas mencakup acuan metode, teori, serta pembanding; tidak berarti semua algoritma yang disebut diimplementasikan dalam penelitian.

Untuk SPOTER digunakan entri konferensi tahun 2022 yang lengkap. Entri duplikat tanpa tahun dengan tautan yang tidak sesuai pada daftar pustaka skripsi tidak disertakan kembali.
