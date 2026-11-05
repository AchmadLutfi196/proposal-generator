# METODOLOGI PENELITIAN

## 3.1 Alur Penelitian

Metodologi penelitian ini dirancang secara sistematis untuk menjawab seluruh rumusan masalah dan mencapai target tujuan penelitian yang telah ditetapkan. Rangkaian tahapan pelaksanaan penelitian disusun ke dalam enam fase utama: studi literatur, pengumpulan data, perancangan sistem, implementasi, pengujian dan evaluasi, serta penyusunan laporan akhir. Alur tahapan penelitian diilustrasikan secara visual pada Gambar 3.1 menggunakan diagram alir berstandar ISO 5807.

![Diagram alir tahapan penelitian](gambar/flowchart_penelitian.png)

Gambar 3.1 Diagram alir tahapan penelitian

Sumber: Perancangan Penelitian (2026)

Tahapan penelitian dimulai dengan studi literatur untuk mendalami konsep bidang Kecerdasan Komputasional dan metode CNN (Convolutional Neural Network). Fase pengumpulan data menghimpun data studi kasus. Tahap perancangan memodelkan kebutuhan dan arsitektur sistem. Tahap implementasi membangun komponen sesuai rancangan. Setelah sistem terbangun, dilakukan pengujian fungsional dan evaluasi berdasarkan skenario pada subbab 3.4. Apabila hasil pengujian memenuhi seluruh kriteria kelayakan, penelitian dilanjutkan ke fase analisis hasil dan penyusunan laporan akhir skripsi.

## 3.2 Teknik Perolehan Data

Dataset citra daun kopi berlabel sehat dan terserang karat daun dikumpulkan dari kebun dan dokumentasi visual. Prosedur validasi meliputi penghapusan citra buram, penyeimbangan kelas, dan split data menjadi latih, validasi, dan uji.

## 3.3 Perancangan dan Implementasi

Model menggunakan arsitektur MobileNetV2 dengan transfer learning. Tahapan meliputi praproses citra (resize, normalisasi piksel, augmentasi rotasi dan kecerahan), pelatihan model dengan optimizer Adam, serta penyimpanan model terbaik berdasarkan validasi. Antarmuka pengguna memungkinkan pengguna mengunggah citra daun dan menerima hasil klasifikasi beserta tingkat keyakinan.

## 3.4 Skenario Pengujian dan Evaluasi

Evaluasi performa model dilakukan menggunakan confusion matrix, akurasi, presisi, recall, dan F1-score:

$$\text{Accuracy} = \frac{TP+TN}{TP+TN+FP+FN}, \quad \text{Precision} = \frac{TP}{TP+FP}, \quad \text{Recall} = \frac{TP}{TP+FN}, \quad F1 = \frac{2 \cdot \text{Precision} \cdot \text{Recall}}{\text{Precision}+\text{Recall}}$$

Pengujian fungsional antarmuka dilakukan menggunakan black box testing pada modul unggah citra, penggelaran hasil klasifikasi, dan riwayat hasil. Kriteria keberhasilan ditetapkan apabila F1-score pada data uji mencapai target yang ditetapkan peneliti dan 100% kasus uji fungsional valid.
