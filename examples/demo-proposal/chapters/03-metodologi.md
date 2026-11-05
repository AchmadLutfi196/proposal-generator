# METODOLOGI PENELITIAN

## 3.1 Alur Penelitian

Metodologi penelitian ini dirancang secara sistematis untuk menjawab seluruh rumusan masalah dan mencapai target tujuan penelitian yang telah ditetapkan. Rangkaian tahapan pelaksanaan penelitian disusun ke dalam enam fase utama: studi literatur, pengumpulan data, perancangan sistem, implementasi platform, pengujian dan evaluasi, serta penyusunan laporan akhir. Alur tahapan penelitian diilustrasikan secara visual pada Gambar 3.1 menggunakan diagram alir berstandar ISO 5807.

![Diagram alir tahapan penelitian](gambar/flowchart_penelitian.png)

Gambar 3.1 Diagram alir tahapan penelitian

Sumber: Perancangan Penelitian (2026)

Tahapan penelitian dimulai dengan studi literatur untuk mendalami arsitektur model IndoBERT, teknik kesamaan semantik kosinus, serta prinsip rekayasa perangkat lunak sistem penilaian esai [@pressman2020software; @wilie2020indonlu]. Pada fase pengumpulan data, dilakukan inventarisasi lembar jawaban esai ujian sekolah dan verifikasi kunci jawaban bersama guru pengampu mata pelajaran. Tahap perancangan sistem memodelkan kebutuhan fungsional dan non-fungsional, perancangan basis data relasional, dan diagram alur kerja multi-rater. 

Tahap implementasi mencakup pengodean antarmuka web, logika bisnis pencatatan multi-penilai, dan integrasi modul inferensi IndoBERT [@raschka2022machine]. Setelah sistem terbangun, dilakukan pengujian fungsional kotak hitam (*black box testing*) dan evaluasi metrik akurasi rekomendasi skor terhadap acuan skor guru. Apabila hasil pengujian memenuhi seluruh kriteria kelayakan, penelitian dilanjutkan ke fase analisis hasil dan penyusunan laporan akhir skripsi.

## 3.2 Pengumpulan dan Validasi Data

Data penelitian bersumber dari lembar jawaban esai peserta didik pada Ujian Tengah Semester mata pelajaran non-eksakta di sekolah menengah. Karakteristik instrumen soal esai mencakup pertanyaan terbuka yang menuntut penalaran konseptual. Pengumpulan data dilaksanakan melalui studi dokumentasi terhadap lembar jawaban fisik yang kemudian ditranskripsi ke dalam format digital teks UTF-8 [@sommerville2016software].

Untuk memastikan kualitas data acuan sebelum proses evaluasi komputasi dilakukan, diterapkan prosedur validasi tiga tahap:

1. **Pemeriksaan Kunci Jawaban:** Kunci jawaban acuan diperiksa dan disepakati oleh tim guru pengampu mata pelajaran untuk menjamin kelengkapan cakupan aspek materi yang dinilai.
2. **Normalisasi Format:** Teks jawaban dibersihkan dari karakter non-standar, kesalahan pengetikan leksikal minor, dan spasi ganda.
3. **Penyusunan Subset Multi-Penilai:** Pada subset lembar jawaban kalibrasi evaluasi, dilakukan penilaian independen oleh dua orang pengajar berbeda menggunakan rubrik penilaian yang sama tanpa saling melihat skor masing-masing. Rata-rata dari skor kedua guru tersebut ditetapkan sebagai skor patokan (*ground truth benchmark*) [@xiao2025human].

## 3.3 Perancangan dan Implementasi Platform

Platform perangkat lunak dikembangkan berbasis web dengan pendekatan arsitektur klien-server modular. Pemisahan tanggung jawab antarmuka pengguna (*front-end*) dan mesin logika bisnis (*back-end*) dilakukan untuk memastikan fleksibilitas dan skalabilitas sistem [@pressman2020software].

Arsitektur sistem terdiri dari tiga modul utama:

1. **Modul Manajemen Asesmen:** Mengelola pembuatan kelas, butir soal esai, bobot nilai, batas waktu pengerjaan, dan pengunggahan kunci jawaban acuan.
2. **Modul Distribusi Multi-Rater:** Bertanggung jawab mendistribusikan lembar jawaban siswa kepada dua pengajar penilai, mencatat skor individual masing-masing penilai secara terisolasi, serta mendeteksi selisih skor yang melampaui ambang batas toleransi rekonsiliasi.
3. **Modul Inferensi Semantik IndoBERT:** Memuat model prapelatihan *indobenchmark/indobert-base-p2*. Modul ini mengekstrak vektor semantik dari teks jawaban siswa dan kunci jawaban acuan, melakukan operasi *mean pooling*, menghitung nilai kesamaan kosinus, dan mengonversinya menjadi rekomendasi skor terkalibrasi [@pradani2023aes].

Antarmuka pengajar dirancang responsif, menyajikan perbandingan teks jawaban siswa berdampingan dengan kunci jawaban, nilai rekomendasi IndoBERT sebagai panduan awal, serta formulir masukan skor resmi dan catatan umpan balik kualitatif guru.

## 3.4 Skenario Pengujian dan Evaluasi

Pengujian dan evaluasi penelitian dirancang mencakup dua dimensi: evaluasi kinerja rekomendasi algoritma kecerdasan komputasional dan evaluasi fungsionalitas sistem perangkat lunak.

### 3.4.1 Evaluasi Kinerja Rekomendasi Model

Evaluasi model inferensi IndoBERT dilakukan dengan mengukur kesesuaian antara nilai rekomendasi sistem ($y_i$) dengan nilai acuan rata-rata pengajar ($r_i$) pada dataset uji. Metrik yang digunakan meliputi:

1. **Quadratic Weighted Kappa (QWK):** Mengukur derajat reliabilitas kesepakatan antar-penilai dengan memberikan pembobotan kuadratik pada deviasi skor ordinal [@wang2022bert]. Nilai QWK mendekati 1,0 mengindikasikan kesepakatan sempurna.
2. **Mean Absolute Error (MAE):** Mengukur magnitudo rata-rata kesalahan prediksi skor secara langsung:
   $$\text{MAE} = \frac{1}{N} \sum_{i=1}^{N} |y_i - r_i|$$
3. **Root Mean Square Error (RMSE):** Mengukur akar purata kuadrat kesalahan untuk memberikan sensitivitas terhadap kesalahan prediksi berskala besar:
   $$\text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (y_i - r_i)^2}$$

### 3.4.2 Pengujian Fungsional Sistem (*Black Box Testing*)

Pengujian fungsionalitas platform dilakukan menggunakan teknik *black box testing* berbasis kasus uji (*test cases*) pada seluruh fungsi wajib sistem [@pressman2020software]. Cakupan pengujian meliputi:

- Modul autentikasi pengguna dan hak akses peran (Admin, Pengajar Utama, Pengajar Penilai).
- Modul pengelolaan bank soal dan kunci jawaban esai.
- Modul penugasan ganda pengajar dan kerahasiaan skor individual (*blind review*).
- Modul eksekusi inferensi semantik IndoBERT dan kestabilan waktu respons sistem.
- Modul rekapitulasi nilai akhir, penanganan anomali disparitas skor, dan pencetakan laporan hasil ujian.

Kriteria keberhasilan pengujian fungsional ditetapkan apabila 100% kasus uji wajib menghasilkan status valid sesuai dengan perilaku keluaran yang diharapkan (*expected results*).
