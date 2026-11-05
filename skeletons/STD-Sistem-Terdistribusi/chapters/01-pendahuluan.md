# PENDAHULUAN

## 1.1 Latar Belakang

Bidang Minat: **SISTEM TERDISTRIBUSI**.

Topik penelitian ini adalah **Sistem Terdistribusi Penyeimbang Beban API Berbasis Round Robin**. Latar belakang berikut disusun dari permasalahan umum di bidang Sistem Terdistribusi menuju permasalahan spesifik studi kasus, kemudian mengarah pada kebutuhan solusi berbasis metode Load balancing Round Robin + replikasi + health check.

[GANTI: tulis latar belakang >=1000 kata untuk topik "Sistem Terdistribusi Penyeimbang Beban API Berbasis Round Robin" dengan alur global → lokal → kesenjangan riset → kontribusi. Isi awal ini contoh umum bidang Sistem Terdistribusi yang wajib diganti agent dengan isi spesifik topik mahasiswa, tetap memakai sitasi `[@cue...]` yang nyata.]

## 1.2 Rumusan Masalah

### 1.2.1 Permasalahan

[Permasalahan spesifik yang dihadapi pada studi kasus: kondisi saat ini, dampaknya, dan mengapa solusi manual/eksisting belum mencukupi.]

### 1.2.2 Metode Usulan

Metode usulan penelitian ini adalah **Load balancing Round Robin + replikasi + health check**. [Jelaskan secara singkat bagaimana metode tersebut menjawab permasalahan pada 1.2.1: tahapan, alat/teknologi, dan alasan pemilihannya dibanding alternatif.]

### 1.2.3 Pertanyaan Penelitian

1. [Pertanyaan penelitian 1, berkaitan dengan perancangan/pemodelan.]
2. [Pertanyaan penelitian 2, berkaitan dengan pengujian/evaluasi kinerja.]

## 1.3 Tujuan dan Manfaat

### 1.3.1 Tujuan Penelitian

Tujuan yang hendak dicapai melalui pelaksanaan penelitian ini meliputi:

1. Mengembangkan arsitektur dan antarmuka sistem informasi permasalahan pada studi kasus penelitian ini berbasis web yang mendukung pengelolaan soal, kunci jawaban, penugasan ganda pengajar (*multi-modul*), dan rekapitulasi skor final.
2. Mengintegrasikan algoritma representasi semantik Load balancing Round Robin + replikasi + health check dengan operasi *mean pooling* dan *cosine similarity* ke dalam sistem informasi untuk menghasilkan estimasi skor otomatis.
3. Mengukur performa akurasi rekomendasi skor otomatis menggunakan metrik QWK, RMSE, dan MAE serta menguji kelayakan fungsi sistem menggunakan pengujian *black box testing*.

### 1.3.2 Manfaat Penelitian

Penelitian ini diharapkan memberikan kontribusi nyata baik secara teoritis maupun praktis:

1. **Manfaat Teoritis:** Memberikan bukti empiris mengenai efektivitas penerapan model prapelatihan Transformer (Load balancing Round Robin + replikasi + health check) pada tugas penilaian teks bahasa Indonesia dalam skema evaluasi multi-penilai tanpa perlunya komputasi fine-tuning yang mahal.
2. **Manfaat Praktis:** Menyediakan perangkat lunak fungsional bagi sekolah dan tenaga pendidik untuk meningkatkan efisiensi koreksi ujian esai, meminimalkan disparitas skor antar-guru, serta mewujudkan sistem asesmen hasil belajar yang transparan dan akuntabel.

## 1.4 Batasan Masalah

Guna menjaga fokus penelitian agar terarah dan mendalam, ditetapkan batasan-batasan masalah sebagai berikut:

1. Model bahasa yang digunakan adalah *indobenchmark/indobert-base-p2* pada tingkatan *inference* representasi vektor teks tanpa melakukan proses penyesuaian bobot menyeluruh (*full fine-tuning*).
2. Data penelitian berfokus pada lembar jawaban ujian esai mata pelajaran non-eksakta yang disusun dalam bahasa Indonesia baku.
3. Arsitektur multi-modul yang dikembangkan membatasi penugasan evaluasi pada dua penilai independen untuk setiap lembar jawaban siswa pada subset uji kalibrasi.
4. Pengujian fungsionalitas perangkat lunak difokuskan pada metode pengujian kotak hitam (*black box testing*) pada seluruh alur kerja operasional sistem.

## 1.5 Sistematika Penulisan Skripsi

Proposal skripsi ini disusun ke dalam tiga bab utama dengan sistematika sebagai berikut:

- **BAB I PENDAHULUAN:** Memuat uraian latar belakang masalah, rumusan masalah (permasalahan, metode usulan, dan pertanyaan penelitian), tujuan dan manfaat penelitian, batasan masalah, sistematika penulisan, serta jadwal rencana kegiatan penelitian.
- **BAB II TINJAUAN PUSTAKA:** Menguraikan teori-teori dasar yang mendasari perancangan sistem dan model komputasi, mencakup pemrosesan bahasa alami, arsitektur Transformer, model Load balancing Round Robin + replikasi + health check, serta tinjauan kritis terhadap penelitian-penelitian terdahulu yang relevan.
- **BAB III METODOLOGI PENELITIAN:** Menjelaskan alur tahapan penelitian secara komprehensif, teknik pengumpulan dan validasi data, perancangan arsitektur sistem perangkat lunak, formulasi algoritma penilaian, serta skenario pengujian fungsional dan metrik evaluasi performa model.
- **DAFTAR PUSTAKA & LAMPIRAN:** Memuat seluruh daftar referensi ilmiah yang dirujuk dengan format APA serta lampiran data pendukung rancangan sistem.

## 1.6 Jadwal Penelitian

Pelaksanaan penelitian direncanakan berlangsung selama 6 (enam) bulan dengan rincian jadwal kerja sebagaimana tertera pada Tabel 1.1.

Tabel 1.1 Jadwal pelaksanaan kegiatan penelitian

| No | Tahapan Kegiatan Penelitian | Bulan 1 | Bulan 2 | Bulan 3 | Bulan 4 | Bulan 5 | Bulan 6 |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Studi literatur dan analisis kebutuhan sistem | ✓ | | | | | |
| 2 | Pengumpulan data esai dan validasi kunci jawaban | | ✓ | | | | |
| 3 | Perancangan arsitektur sistem dan antarmuka | | ✓ | ✓ | | | |
| 4 | Implementasi kode platform dan integrasi Load balancing Round Robin + replikasi + health check | | | ✓ | ✓ | | |
| 5 | Pengujian fungsional (*black box*) dan evaluasi metrik | | | | | ✓ | |
| 6 | Analisis hasil, finalisasi laporan, dan diseminasi | | | | | | ✓ |

Sumber: Perancangan Penelitian (2026)
