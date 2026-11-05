# TINJAUAN PUSTAKA

## 2.1 Teori Dasar

### 2.1.1 Sistem Terdistribusi, Load Balancing, dan Ketersediaan Layanan

Sistem terdistribusi adalah kumpulan komputer independen yang tampak oleh pengguna sebagai satu sistem koheren, bekerja sama melalui jaringan untuk menyediakan layanan bersama [@tanenbaum2017distributed]. Ketersediaan layanan ditingkatkan melalui replikasi, di mana beberapa replika layanan berjalan pada node berbeda sehingga kegagalan satu node tidak menghentikan layanan secara keseluruhan [@tanenbaum2017distributed; @coulouris2017distributed].

Penyeimbang beban (load balancer) mendistribusikan permintaan klien ke beberapa node server agar tidak ada node yang kewalahan. Algoritma Round Robin mendistribusikan permintaan secara bergiliran ke setiap node aktif, memberikan beban yang terdistribusi merata dalam skenario sederhana [@coulouris2017distributed]. Mekanisme health check berkala memantau status kesehatan setiap node, dan failover otomatis mengalihkan lalu lintas dari node yang tidak sehat ke node yang sehat.

## 2.2 Penelitian Terdahulu

Penelitian pertama. Penelitian pertama mengimplementasikan load balancing Round Robin menggunakan Nginx dan mengukur penurunan waktu respons rata-rata hingga 35% pada beban berjenjang, namun belum menguji skenario kegagalan node.[GANTI: penelitian prior 1 yang nyata untuk topik sistem terdistribusi Anda.]

Penelitian kedua. Penelitian kedua membandingkan algoritma load balancing Round Robin, least connection, dan least response pada layanan REST dan menemukan least connection unggul pada kondisi beban tidak merata.[GANTI: penelitian prior 2 yang nyata.]

Penelitian ketiga. Penelitian ketiga membangun arsitektur microservices dengan replikasi layanan dan melaporkan peningkatan ketersediaan hingga 99,9% pada pengujian kegagalan satu instance, dengan biaya kompleksitas operasional yang lebih tinggi.[GANTI: penelitian prior 3 yang nyata.]

Penelitian keempat. Penelitian keempat mengevaluasi konsistensi data pada replikasi basis data terdistribusi dan menemukan jendela inkonsistensi sementara pada skenario partition jaringan.[GANTI: penelitian prior 4 yang nyata.]

Penelitian kelima. Penelitian kelima mengukur throughput dan latensi sistem terdistribusi container-based pada Kubernetes dan melaporkan skalabilitas horizontal yang linear hingga 4 node.[GANTI: penelitian prior 5 yang nyata.]

Perbandingan komparatif antara penelitian-penelitian terdahulu dengan kontribusi penelitian yang diusulkan disajikan pada Tabel 2.1. [Lengkapi baris tabel dengan penelitian prior yang nyata dan posisi penelitian usulan Anda.]

Tabel 2.1 Perbandingan penelitian terdahulu dan posisi penelitian usulan

| Peneliti (Tahun) | Objek Penelitian | Metode Utama | Kelebihan | Keterbatasan | Posisi Usulan Penelitian |
|:---|:---|:---|:---|:---|:---|
| [Peneliti prior 1] | [objek] | [metode] | [kelebihan] | [keterbatasan] | [posisi usulan] |
| [Peneliti prior 2] | [objek] | [metode] | [kelebihan] | [keterbatasan] | [posisi usulan] |
| [Peneliti prior 3] | [objek] | [metode] | [kelebihan] | [keterbatasan] | [posisi usulan] |
| [Peneliti prior 4] | [objek] | [metode] | [kelebihan] | [keterbatasan] | [posisi usulan] |
| [Peneliti prior 5] | [objek] | [metode] | [kelebihan] | [keterbatasan] | [posisi usulan] |
| **Penelitian Ini (2026)** | **[objek studi kasus]** | **Load balancing Round Robin + replikasi + health check, bidang Sistem Terdistribusi** | **Solusi terukur untuk studi kasus** | **[keterbatasan]** | **Kontribusi penelitian** |

Sumber: Hasil analisis literatur penelitian (2026)

## 2.3 Celah Riset

Celah riset penelitian ini adalah evaluasi gabungan performa dan failover otomatis pada satu arsitektur load balancer Round Robin dengan replikasi layanan.
