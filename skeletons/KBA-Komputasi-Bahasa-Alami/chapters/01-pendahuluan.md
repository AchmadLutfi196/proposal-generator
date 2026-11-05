# PENDAHULUAN

## 1.1 Latar Belakang

Pendidikan merupakan pilar fundamental dalam pengembangan kualitas sumber daya manusia di era revolusi industri dan transformasi digital saat ini. Di dalam proses kegiatan belajar-mengajar di sekolah maupun perguruan tinggi, evaluasi pembelajaran memiliki peranan yang sangat penting sebagai instrumen untuk mengukur tingkat ketercapaian kompetensi peserta didik [@pressman2020software]. Bentuk instrumen asesmen yang umum diterapkan terbagi menjadi dua kategori utama, yakni tes pilihan ganda (*multiple choice*) dan tes berbasis uraian bebas atau esai (*essay test*). Meskipun tes pilihan ganda menawarkan keunggulan efisiensi pemeriksaan yang instan dan objektivitas penilaian mutlak, instrumen tersebut memiliki keterbatasan mendasar karena cenderung hanya mengukur kemampuan kognitif tingkat rendah, seperti mengingat fakta dan mengenali informasi secara pasif. Sebaliknya, bentuk soal esai memberikan kebebasan yang luas bagi peserta didik untuk mengekspresikan gagasan, merangkai argumen logis, menganalisis persoalan secara mendalam, serta mensintesis pemahaman konseptual secara komprehensif [@sommerville2016software].

Meskipun instrumen esai memiliki keunggulan pedagogis yang signifikan dalam menilai kompetensi berpikir tingkat tinggi (*higher-order thinking skills*), implementasi operasionalnya di lembaga pendidikan sering kali menghadapi kendala teknis dan manajerial yang berat. Salah satu permasalahan krusial dalam evaluasi esai manual adalah tingginya beban kerja dan alokasi waktu yang harus dicurahkan oleh pengajar [@xiao2025human]. Ketika seorang pendidik harus memeriksa puluhan hingga ratusan lembar jawaban uraian yang panjang dan beragam pada setiap periode ujian sekolah, tingkat kelelahan fisik maupun psikologis (*fatigue*) tidak dapat dihindarkan. Kelelahan tersebut secara langsung berdampak negatif terhadap konsistensi pemberian skor, di mana lembar jawaban yang diperiksa pada awal waktu penilaian sering kali dinilai dengan standar ketelitian yang berbeda dibandingkan lembar jawaban yang diperiksa di akhir waktu evaluasi. Kondisi ini memicu munculnya fenomena variabilitas intra-penilai (*intra-rater variability*), di mana seorang guru yang sama dapat memberikan penilaian yang berbeda terhadap dua jawaban dengan substansi yang serupa pada waktu yang berlainan [@jurafsky2024speech].

Tantangan evaluasi menjadi semakin kompleks ketika penilaian esai melibatkan lebih dari satu orang pengajar atau penilai (*multi-rater assessment*). Pada konteks ujian bersama atau penilaian berbasis standar institusional, keterlibatan beberapa penilai dimaksudkan untuk memitigasi subjektivitas individu dan memastikan keadilan bagi seluruh peserta didik [@xiao2025human]. Namun demikian, ketiadaan keseragaman interpretasi terhadap rubrik penskoran dan perbedaan latar belakang keahlian sering menimbulkan kesenjangan skor yang tajam antar-penilai (*inter-rater disagreement*). Lembar jawaban esai yang dinilai oleh pengajar dengan kecenderungan ketat (*strict rater*) akan memperoleh nilai yang jauh lebih rendah dibandingkan lembar jawaban setara yang diperiksa oleh pengajar yang bermurah hati (*lenient rater*). Akibatnya, objektivitas dan validitas hasil ujian menjadi diragukan oleh peserta didik maupun pemangku kepentingan akademik. Selain itu, proses rekonsiliasi manual terhadap selisih skor antar-pengajar menuntut rapat koordinasi yang memakan waktu lama, sehingga memperlambat publikasi nilai akhir hasil belajar [@wang2022bert].

Seiring dengan pesatnya kemajuan teknologi pemrosesan bahasa alami (*Natural Language Processing* / NLP) dan kecerdasan artifisial, sistem penilaian esai otomatis (*Automated Essay Scoring* / AES) muncul sebagai solusi teknologi yang sangat menjanjikan untuk mengatasi kendala-kendala tersebut [@goodfellow2016deep; @raschka2022machine]. Sistem AES dirancang untuk menganalisis teks jawaban peserta didik secara komputasional dan memprediksi skor numerik yang setara dengan penilaian pengajar manusia. Pada masa awal perkembangannya, pendekatan AES banyak mengandalkan rekayasa fitur manual (*hand-crafted features*) seperti penghitungan panjang kata, kekayaan kosakata permukaan, jumlah kalimat, serta kecocokan kata kunci berbasis kamus (*dictionary lookup*). Walaupun pendekatan leksikal permukaan tersebut mudah diimplementasikan, kelemahannya sangat fatal: sistem dapat dengan mudah dimanipulasi oleh jawaban yang panjang berbelit-belit namun miskin makna, serta gagal menangkap konteks semantik yang diungkapkan melalui sinonim, parafrasa, atau variasi struktur sintaksis bahasa [@pradani2023aes].

Terobosan signifikan dalam pemrosesan teks bahasa alami terjadi seiring diperkenalkannya arsitektur *Transformer* berbasis mekanisme atensi mandiri (*self-attention mechanism*) [@wilie2020indonlu]. Model bahasa representasi dua arah seperti BERT (*Bidirectional Encoder Representations from Transformers*) memungkinkan representasi vektor kata dipelajari secara dinamis berdasarkan keseluruhan konteks kalimat di sekitarnya. Untuk ranah bahasa Indonesia, kehadiran model bahasa IndoBERT yang dilatih pada korpus teks bahasa Indonesia berskala besar memberikan lompatan performa yang luar biasa dalam berbagai tugas komputasi linguistik [@wilie2020indonlu; @prastyo2025comparative]. Melalui pemanfaatan representasi semantik mendalam dari model prapelatihan *indobenchmark/indobert-base-p2*, jawaban esai peserta didik dapat dipetakan ke dalam ruang vektor berdimensi tinggi yang secara akurat mencerminkan makna konseptual, bukan sekadar kesamaan leksikal harfiah [@wibowo2024indonesian]. Dengan mengombinasikan vektor jawaban siswa dan kunci jawaban acuan menggunakan metode perata-rataan vektor (*mean pooling*) serta penghitungan kesamaan kosinus (*cosine similarity*), tingkat kedekatan semantik jawaban dapat diukur secara presisi dan dipetakan ke dalam rentang skor rubrik penilaian [@pradani2023aes].

Meskipun pemanfaatan model bahasa prapelatihan menawarkan potensi akurasi yang tinggi, penerapannya dalam lingkungan asesmen pendidikan tidak boleh menyingkirkan peran manusia (*human-in-the-loop*). Pembelajaran transformatif di sekolah menuntut transparansi, akuntabilitas, dan empati pedagogis yang tidak dapat digantikan sepenuhnya oleh algoritma kotak hitam (*black-box algorithms*) [@xiao2025human]. Oleh karena itu, pendekatan yang paling ideal adalah menempatkan kecerdasan artifisial sebagai sistem pendukung keputusan (*decision support system*) yang menghasilkan rekomendasi skor awal dan indikasi anomali, sementara kewenangan penetapan skor akhir tetap berada di tangan pengajar. 

Tantangan teknis lain yang tidak kalah mendasar dalam implementasi skala sekolah adalah keterbatasan infrastruktur komputasi. Banyak institusi pendidikan menengah tidak memiliki server khusus berdaya komputasi GPU tinggi (*Graphics Processing Unit*) untuk menjalankan proses pelatihan ulang model berskala ratusan juta parameter secara berkelanjutan [@jurafsky2024speech]. Dengan demikian, perancangan sistem penilaian esai yang realistis harus mempertimbangkan aspek efisiensi komputasi, misalnya dengan memanfaatkan representasi vektor baku dari model prapelatihan yang dapat dijalankan secara efisien pada server berbasis CPU standar tanpa mengorbankan ketajaman inferensi semantik. Di samping itu, antarmuka sistem harus dirancang intuitif agar guru yang memiliki latar belakang literasi digital beragam dapat mengoperasikan alur penugasan, koreksi, dan rekapitulasi nilai tanpa hambatan teknis yang berarti [@pressman2020software; @sommerville2016software].

Dalam konteks tersebut, dibutuhkan sebuah platform sistem informasi terintegrasi yang mampu mengelola seluruh siklus asesmen esai secara aman, mulai dari penyusunan butir soal dan kunci jawaban, distribusi lembar jawaban digital kepada beberapa penilai independen, penghitungan rekomendasi skor berbasis IndoBERT secara *real-time*, hingga rekapitulasi audit selisih skor antar-pengajar secara otomatis. Integrasi sistem informasi berbasis web dengan mesin inferensi bahasa alami akan menjembatani kesenjangan antara inovasi kecerdasan komputasional mutakhir dengan kebutuhan praktis operasional sekolah sehari-hari.

Berdasarkan keseluruhan tinjauan masalah tersebut, penelitian ini memfokuskan pada pengembangan platform sistem informasi penilaian esai multi-rater berbasis web yang terintegrasi dengan mesin rekomendasi IndoBERT. Penelitian ini dirancang untuk menjawab kebutuhan nyata di lingkungan sekolah dengan menyajikan arsitektur perangkat lunak yang andal, transparan, dan terukur. Dengan adanya platform ini, pengajar dapat mempercepat proses koreksi tanpa kehilangan kendali pedagogis, kesenjangan penilaian antar-pengajar dapat termonitor secara sistematis, dan peserta didik memperoleh umpan balik asesmen yang lebih adil, objektif, dan tepat waktu.

## 1.2 Rumusan Masalah

Berdasarkan uraian latar belakang yang telah dipaparkan, permasalahan yang menjadi fokus dalam penelitian ini dirumuskan ke dalam tiga bagian terstruktur:

### 1.2.1 Permasalahan

Proses penilaian esai manual pada ujian sekolah melibatkan beban pemeriksaan yang tinggi, risiko variabilitas subjektivitas penilai, serta potensi ketidaksepakatan skor (*inter-rater disagreement*) ketika evaluasi dilakukan oleh beberapa pengajar secara terpisah tanpa sistem rekapitulasi terintegrasi. Selain itu, pemanfaatan model bahasa prapelatihan IndoBERT untuk penilaian esai bahasa Indonesia memerlukan perancangan alur integrasi komputasi yang tepat agar rekomendasi skor tetap transparan dan dapat dikalibrasi terhadap skor acuan pengajar manusia.

### 1.2.2 Metode Usulan

Untuk menyelesaikan permasalahan tersebut, diusulkan pengembangan sistem informasi penilaian esai multi-rater berbasis web menggunakan arsitektur modular yang memisahkan modul pengelolaan data ujian dengan modul kecerdasan artifisial. Mesin inferensi semantik dibangun memanfaatkan model *indobenchmark/indobert-base-p2* tanpa proses pelatihan ulang (*fine-tuning*) berat, menggunakan operasi *mean pooling* dan metrik *cosine similarity* guna menghasilkan representasi teks terstandarisasi. Seluruh catatan penilaian individual antar-pengajar direkam secara terpisah untuk menjamin transparansi jejak audit (*audit trail*).

### 1.2.3 Pertanyaan Penelitian

Secara spesifik, penelitian ini diarahkan untuk menjawab dua pertanyaan penelitian berikut:

1. Bagaimana merancang dan membangun platform sistem informasi penilaian esai berbasis web yang mampu mengelola penilaian multi-penilai (*multi-rater*) secara terstruktur dan terverifikasi melalui pengujian fungsional *black box testing*?
2. Bagaimana tingkat akurasi dan kesesuaian rekomendasi skor yang dihasilkan oleh model IndoBERT terhadap skor acuan pengajar manusia berdasarkan metrik Quadratic Weighted Kappa (QWK), Root Mean Square Error (RMSE), dan Mean Absolute Error (MAE)?

## 1.3 Tujuan dan Manfaat

### 1.3.1 Tujuan Penelitian

Tujuan yang hendak dicapai melalui pelaksanaan penelitian ini meliputi:

1. Mengembangkan arsitektur dan antarmuka sistem informasi penilaian esai berbasis web yang mendukung pengelolaan soal, kunci jawaban, penugasan ganda pengajar (*multi-rater*), dan rekapitulasi skor final.
2. Mengintegrasikan algoritma representasi semantik IndoBERT dengan operasi *mean pooling* dan *cosine similarity* ke dalam sistem informasi untuk menghasilkan estimasi skor otomatis.
3. Mengukur performa akurasi rekomendasi skor otomatis menggunakan metrik QWK, RMSE, dan MAE serta menguji kelayakan fungsi sistem menggunakan pengujian *black box testing*.

### 1.3.2 Manfaat Penelitian

Penelitian ini diharapkan memberikan kontribusi nyata baik secara teoritis maupun praktis:

1. **Manfaat Teoritis:** Memberikan bukti empiris mengenai efektivitas penerapan model prapelatihan Transformer (IndoBERT) pada tugas penilaian teks bahasa Indonesia dalam skema evaluasi multi-penilai tanpa perlunya komputasi fine-tuning yang mahal.
2. **Manfaat Praktis:** Menyediakan perangkat lunak fungsional bagi sekolah dan tenaga pendidik untuk meningkatkan efisiensi koreksi ujian esai, meminimalkan disparitas skor antar-guru, serta mewujudkan sistem asesmen hasil belajar yang transparan dan akuntabel.

## 1.4 Batasan Masalah

Guna menjaga fokus penelitian agar terarah dan mendalam, ditetapkan batasan-batasan masalah sebagai berikut:

1. Model bahasa yang digunakan adalah *indobenchmark/indobert-base-p2* pada tingkatan *inference* representasi vektor teks tanpa melakukan proses penyesuaian bobot menyeluruh (*full fine-tuning*).
2. Data penelitian berfokus pada lembar jawaban ujian esai mata pelajaran non-eksakta yang disusun dalam bahasa Indonesia baku.
3. Arsitektur multi-rater yang dikembangkan membatasi penugasan evaluasi pada dua penilai independen untuk setiap lembar jawaban siswa pada subset uji kalibrasi.
4. Pengujian fungsionalitas perangkat lunak difokuskan pada metode pengujian kotak hitam (*black box testing*) pada seluruh alur kerja operasional sistem.

## 1.5 Sistematika Penulisan Skripsi

Proposal skripsi ini disusun ke dalam tiga bab utama dengan sistematika sebagai berikut:

- **BAB I PENDAHULUAN:** Memuat uraian latar belakang masalah, rumusan masalah (permasalahan, metode usulan, dan pertanyaan penelitian), tujuan dan manfaat penelitian, batasan masalah, sistematika penulisan, serta jadwal rencana kegiatan penelitian.
- **BAB II TINJAUAN PUSTAKA:** Menguraikan teori-teori dasar yang mendasari perancangan sistem dan model komputasi, mencakup pemrosesan bahasa alami, arsitektur Transformer, model IndoBERT, serta tinjauan kritis terhadap penelitian-penelitian terdahulu yang relevan.
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
| 4 | Implementasi kode platform dan integrasi IndoBERT | | | ✓ | ✓ | | |
| 5 | Pengujian fungsional (*black box*) dan evaluasi metrik | | | | | ✓ | |
| 6 | Analisis hasil, finalisasi laporan, dan diseminasi | | | | | | ✓ |

Sumber: Perancangan Penelitian (2026)
