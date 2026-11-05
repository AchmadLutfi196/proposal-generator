# METODOLOGI PENELITIAN

## 3.1 Alur Penelitian

Metodologi penelitian ini dirancang secara sistematis untuk menjawab seluruh rumusan masalah dan mencapai target tujuan penelitian yang telah ditetapkan. Rangkaian tahapan pelaksanaan penelitian disusun ke dalam enam fase utama: studi literatur, pengumpulan data, perancangan sistem, implementasi, pengujian dan evaluasi, serta penyusunan laporan akhir. Alur tahapan penelitian diilustrasikan secara visual pada Gambar 3.1 menggunakan diagram alir berstandar ISO 5807.

![Diagram alir tahapan penelitian](gambar/flowchart_penelitian.png)

Gambar 3.1 Diagram alir tahapan penelitian

Sumber: Perancangan Penelitian (2026)

Tahapan penelitian dimulai dengan studi literatur untuk mendalami konsep bidang Teknologi Perangkat Lunak dan metode Waterfall + UML + black box testing. Fase pengumpulan data menghimpun data studi kasus. Tahap perancangan memodelkan kebutuhan dan arsitektur sistem. Tahap implementasi membangun komponen sesuai rancangan. Setelah sistem terbangun, dilakukan pengujian fungsional dan evaluasi berdasarkan skenario pada subbab 3.4. Apabila hasil pengujian memenuhi seluruh kriteria kelayakan, penelitian dilanjutkan ke fase analisis hasil dan penyusunan laporan akhir skripsi.

## 3.2 Teknik Perolehan Data

Data kebutuhan diperoleh melalui observasi proses peminjaman manual, wawancara dengan admin laboratorium dan mahasiswa peminjam, serta studi dokumentasi inventaris alat. Data master meliputi daftar alat, jumlah unit, dan status ketersediaan.

## 3.3 Perancangan dan Implementasi

Rancangan sistem dimodelkan dengan UML: use case diagram untuk aktor admin dan mahasiswa, activity diagram untuk alur peminjaman dan pengembalian, serta class diagram untuk struktur data. Basis data relasional dirancang dengan tabel master alat, peminjaman, dan pengembalian. Implementasi dilakukan berbasis web dengan pemisahan front-end dan back-end.

## 3.4 Skenario Pengujian dan Evaluasi

Pengujian fungsional dilakukan menggunakan black box testing berbasis kasus uji pada seluruh modul wajib: autentikasi, manajemen inventaris, peminjaman, pengembalian, dan laporan pemakaian. Kriteria keberhasilan ditetapkan apabila 100% kasus uji wajib menghasilkan status valid sesuai perilaku keluaran yang diharapkan.
