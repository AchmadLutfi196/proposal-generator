# METODOLOGI PENELITIAN

## 3.1 Alur Penelitian

Metodologi penelitian ini dirancang secara sistematis untuk menjawab seluruh rumusan masalah dan mencapai target tujuan penelitian yang telah ditetapkan. Rangkaian tahapan pelaksanaan penelitian disusun ke dalam enam fase utama: studi literatur, pengumpulan data, perancangan sistem, implementasi, pengujian dan evaluasi, serta penyusunan laporan akhir. Alur tahapan penelitian diilustrasikan secara visual pada Gambar 3.1 menggunakan diagram alir berstandar ISO 5807.

![Diagram alir tahapan penelitian](gambar/flowchart_penelitian.png)

Gambar 3.1 Diagram alir tahapan penelitian

Sumber: Perancangan Penelitian (2026)

Tahapan penelitian dimulai dengan studi literatur untuk mendalami konsep bidang Sistem Terdistribusi dan metode Load balancing Round Robin + replikasi + health check. Fase pengumpulan data menghimpun data studi kasus. Tahap perancangan memodelkan kebutuhan dan arsitektur sistem. Tahap implementasi membangun komponen sesuai rancangan. Setelah sistem terbangun, dilakukan pengujian fungsional dan evaluasi berdasarkan skenario pada subbab 3.4. Apabila hasil pengujian memenuhi seluruh kriteria kelayakan, penelitian dilanjutkan ke fase analisis hasil dan penyusunan laporan akhir skripsi.

## 3.2 Teknik Perolehan Data

Data diperoleh melalui studi literatur arsitektur sistem terdistribusi serta observasi beban layanan API kampus saat ini. Skenario beban disimulasikan dengan generator permintaan HTTP pada tingkat konkurensi bertingkat.

## 3.3 Perancangan dan Implementasi

Arsitektur sistem terdiri dari klien, penyeimbang beban Round Robin, dan beberapa node server yang masing-masing menjalankan replika layanan API. Penyeimbang beban mendistribusikan permintaan secara bergiliran ke node aktif, menjalankan health check berkala, dan mengalihkan lalu lintas dari node tidak sehat melalui failover otomatis. Replikasi layanan memastikan satu node gagal tidak menghentikan layanan.

## 3.4 Skenario Pengujian dan Evaluasi

Evaluasi performa diukur melalui throughput, waktu respons rata-rata, nilai persentil latensi, dan ketersediaan layanan:

$$\text{Throughput} = \frac{\text{jumlah permintaan berhasil}}{\text{selang waktu pengamatan}}, \quad \text{Availability} = \frac{\text{waktu layanan aktif}}{\text{total waktu pengamatan}} \times 100\%$$

Pengujian skenario kegagalan mematikan satu node saat beban berjalan dan memverifikasi failover otomatis tanpa kehilangan permintaan. Pengujian fungsional dilengkapi black box testing pada modul konfigurasi dan pemantauan node.
