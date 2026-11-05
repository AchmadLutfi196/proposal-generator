# TINJAUAN PUSTAKA

## 2.1 Teori Dasar

### 2.1.1 Pembelajaran Mendalam dan Convolutional Neural Network

Pembelajaran mendalam (*deep learning*) merupakan cabang pembelajaran mesin yang memanfaatkan jaringan saraf tiruan berlapis untuk mempelajari representasi data secara bertahap [@goodfellow2016deep]. Pada tugas klasifikasi citra, arsitektur Convolutional Neural Network (CNN) dirancang khusus untuk mengekstrak fitur visual melalui operasi konvolusi yang memindai pola lokal pada setiap wilayah citra, dilanjutkan pooling untuk mereduksi dimensi spasial serta lapisan fully connected untuk pengambilan keputusan klasifikasi [@goodfellow2016deep; @raschka2022machine].

Teknik transfer learning memungkinkan penggunaan model prapelatihan seperti MobileNetV2 yang telah dilatih pada dataset umum untuk diadaptasi pada dataset spesifik bidang aplikasi dengan proses fine-tuning terbatas. Pendekatan ini mempercepat konvergensi pelatihan dan mengurangi kebutuhan dataset berlabel berskala besar [@raschka2022machine].

## 2.2 Penelitian Terdahulu

Penelitian pertama. Penelitian pertama menggunakan CNN untuk klasifikasi penyakit daun pada citra tanaman hortikultura dengan dataset berlabel ratusan kelas dan melaporkan akurasi di atas 90% pada data uji terpisah. Keterbatasan penelitian tersebut adalah penggunaan dataset citra berskala laboratorium dengan kondisi pencahayaan terkendali, sehingga belum diuji pada citra lapangan yang memuat variasi pose dan latar yang kompleks.[GANTI: penelitian prior 1 yang nyata untuk topik Anda, dengan metode, hasil, kelebihan, dan keterbatasan.]

Penelitian kedua. Penelitian kedua membandingkan arsitektur CNN ringan seperti MobileNetV2 dengan model konvensional untuk klasifikasi objek pada perangkat mobile. Hasilnya menunjukkan MobileNetV2 mempertahankan akurasi yang kompetitif dengan ukuran model yang jauh lebih kecil dan waktu inferensi tercepat pada CPU.[GANTI: penelitian prior 2 yang nyata untuk topik Anda.]

Penelitian ketiga. Penelitian ketiga mengevaluasi teknik augmentasi data untuk meningkatkan generalisasi model klasifikasi citra medis dan pertanian, menemukan bahwa augmentasi rotasi dan perubahan kecerahan menurunkan kesalahan klasifikasi sebesar 8-12%.[GANTI: penelitian prior 3 yang nyata untuk topik Anda.]

Penelitian keempat. Penelitian keempat mengkaji penerapan model vision transformer untuk klasifikasi citra tanaman dan melaporkan performa yang setara dengan CNN dengan biaya komputasi yang lebih tinggi.[GANTI: penelitian prior 4 yang nyata untuk topik Anda.]

Penelitian kelima. Penelitian kelima melakukan studi komparasi metrik evaluasi klasifikasi, menekankan pentingnya pelaporan presisi, recall, dan F1-score selain akurasi keseluruhan pada dataset tidak seimbang.[GANTI: penelitian prior 5 yang nyata untuk topik Anda.]

Perbandingan komparatif antara penelitian-penelitian terdahulu dengan kontribusi penelitian yang diusulkan disajikan pada Tabel 2.1. [Lengkapi baris tabel dengan penelitian prior yang nyata dan posisi penelitian usulan Anda.]

Tabel 2.1 Perbandingan penelitian terdahulu dan posisi penelitian usulan

| Peneliti (Tahun) | Objek Penelitian | Metode Utama | Kelebihan | Keterbatasan | Posisi Usulan Penelitian |
|:---|:---|:---|:---|:---|:---|
| [Peneliti prior 1] | [objek] | [metode] | [kelebihan] | [keterbatasan] | [posisi usulan] |
| [Peneliti prior 2] | [objek] | [metode] | [kelebihan] | [keterbatasan] | [posisi usulan] |
| [Peneliti prior 3] | [objek] | [metode] | [kelebihan] | [keterbatasan] | [posisi usulan] |
| [Peneliti prior 4] | [objek] | [metode] | [kelebihan] | [keterbatasan] | [posisi usulan] |
| [Peneliti prior 5] | [objek] | [metode] | [kelebihan] | [keterbatasan] | [posisi usulan] |
| **Penelitian Ini (2026)** | **[objek studi kasus]** | **CNN (Convolutional Neural Network), bidang Kecerdasan Komputasional** | **Solusi terukur untuk studi kasus** | **[keterbatasan]** | **Kontribusi penelitian** |

Sumber: Hasil analisis literatur penelitian (2026)

## 2.3 Celah Riset

Celah riset penelitian ini terletak pada evaluasi model CNN pada citra lapangan daun kopi dengan dokumentasi metrik lengkap serta pengujian fungsional antarmuka pengguna.
