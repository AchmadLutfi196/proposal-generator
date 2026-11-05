# TINJAUAN PUSTAKA

## 2.1 Teori Dasar

Landasan teori pada bab ini menguraikan konsep-konsep fundamental komputasi yang dijadikan dasar perancangan sistem, mencakup representasi pemrosesan bahasa alami, arsitektur Transformer, model IndoBERT, kesamaan kosinus (*cosine similarity*), serta teori pengukuran multi-penilai (*multi-rater measurement*).

### 2.1.1 Pemrosesan Bahasa Alami dan Ekstraksi Semantik

Pemrosesan bahasa alami (*Natural Language Processing* / NLP) adalah cabang kecerdasan artifisial yang berfokus pada interaksi komputasional antara komputer dengan bahasa alami manusia [@jurafsky2024speech]. Dalam kaitannya dengan evaluasi jawaban esai, tantangan utama NLP adalah mengubah teks tak terstruktur (*unstructured text*) menjadi representasi numerik terstruktur (*embedding vectors*) yang mampu menangkap kedalaman makna semantik tanpa kehilangan konteks kalimat [@goodfellow2016deep]. 

Pendekatan klasik seperti *Bag-of-Words* (BoW) dan *Term Frequency-Inverse Document Frequency* (TF-IDF) hanya memperhitungkan frekuensi kemunculan kata secara ortogonal tanpa memedulikan urutan kata maupun sinonim [@raschka2022machine]. Keterbatasan ini kemudian diatasi oleh representasi terdistribusi (*word embeddings*) seperti Word2Vec dan FastText yang memetakan kata ke dalam ruang vektor berdimensi kontinu. Namun demikian, vektor kata statis tersebut tetap memiliki kelemahan mendasar karena memberikan representasi yang identik untuk kata-kata polisemi (kata yang sama dengan makna berbeda tergantung konteks kalimat) [@wilie2020indonlu].

### 2.1.2 Arsitektur Transformer dan Model IndoBERT

Arsitektur *Transformer* yang diperkenalkan oleh Vaswani et al. merevolusi lanskap pemrosesan bahasa alami melalui mekanisme atensi mandiri terdistribusi (*multi-head self-attention*) [@jurafsky2024speech]. Berbeda dengan model sekuensial rekursif seperti RNN atau LSTM yang memproses teks kata demi kata secara berurutan, Transformer memproses keseluruhan urutan kata secara paralel, memungkinkan pemodelan relasi jarak jauh (*long-range dependencies*) antar-kata dalam teks secara efisien [@goodfellow2016deep].

Model BERT (*Bidirectional Encoder Representations from Transformers*) menggunakan tumpukan enkoder Transformer dua arah untuk menghasilkan representasi kontekstual mendalam [@wang2022bert]. Untuk bahasa Indonesia, konsorsium IndoBenchmark melatih model IndoBERT pada korpus Indo4B yang memuat lebih dari 4 miliar token kata dari artikel berita, Wikipedia, dan media sosial [@wilie2020indonlu]. Model varian *indobenchmark/indobert-base-p2* terdiri atas 12 lapisan enkoder, 12 attention heads, dan menghasilkan vektor representasi tersembunyi berdimensi 768 untuk setiap token teks. Representasi keluaran ini menjadi landasan ekstraksi semantik jawaban esai peserta didik dalam penelitian ini.

### 2.1.3 Penghitungan Kesamaan Kosinus (*Cosine Similarity*)

Untuk menentukan tingkat kesesuaian antara vektor representasi jawaban siswa ($\vec{u}$) dan vektor kunci jawaban acuan ($\vec{v}$), digunakan metrik kesamaan kosinus (*cosine similarity*). Vektor kalimat utuh diperoleh melalui operasi *mean pooling*, yaitu menghitung rata-rata nilai vektor token pada lapisan enkoder terakhir dengan mengabaikan token bantalan (*padding tokens*) [@pradani2023aes].

Formula matematis kesamaan kosinus didefinisikan sebagai perkalian titik antara kedua vektor dibagi dengan hasil kali magnitudo masing-masing vektor:

$$\text{Cosine Similarity}(\vec{u}, \vec{v}) = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\| \|\vec{v}\|} = \frac{\sum_{i=1}^{n} u_i v_i}{\sqrt{\sum_{i=1}^{n} u_i^2} \sqrt{\sum_{i=1}^{n} v_i^2}}$$

Nilai kesamaan kosinus berada pada rentang numerik $[-1, 1]$. Dalam konteks perbandingan representasi teks IndoBERT, nilai kemiripan umumnya berada pada rentang $[0, 1]$, di mana nilai 1 merepresentasikan kemiripan semantik identik dan nilai 0 merepresentasikan ketiadaan relasi semantik sama sekali. Nilai kemiripan ini kemudian dikalikan secara proporsional dengan bobot nilai maksimal butir soal untuk menghasilkan rekomendasi skor kontinu [@prastyo2025comparative].

### 2.1.4 Evaluasi Multi-Rater dan Metrik Kesepakatan

Dalam asesmen pendidikan, keterlibatan beberapa penilai independen bertujuan mengendalikan bias persepsi individu [@xiao2025human]. Untuk mengukur derajat reliabilitas dan kesepakatan skor numerik antar-penilai manusia maupun antara sistem AI dengan pengajar, digunakan metrik Quadratic Weighted Kappa (QWK). Metrik QWK memberikan penalti kuadratik yang lebih berat terhadap selisih penilaian yang ekstrem dibandingkan selisih skor minor [@wang2022bert]. Di samping QWK, metrik galat absolut rata-rata (*Mean Absolute Error* / MAE) dan akar purata kuadrat galat (*Root Mean Square Error* / RMSE) digunakan untuk mengukur deviasi magnitudo skor rekomendasi sistem terhadap skor ril pengajar.

## 2.2 Penelitian Terdahulu

Penelitian mengenai penilaian esai otomatis dan integrasi model bahasa Transformer telah berkembang secara ekstensif dalam beberapa tahun terakhir. Tinjauan terhadap lima penelitian kunci terdahulu disajikan sebagai berikut untuk menegaskan posisi dan keterbaruan usulan penelitian ini.

Penelitian pertama dilakukan oleh Wang et al. (2022) yang meneliti pemanfaatan arsitektur multi-skala BERT untuk tugas penilaian esai otomatis pada dataset standar ASAP (*Automated Student Assessment Prize*) [@wang2022bert]. Penelitian tersebut mengombinasikan representasi tingkat kata, kalimat, dan paragraf menggunakan mekanisme fusi atensi hierarkis. Hasil eksperimen menunjukkan bahwa integrasi representasi hierarkis mampu meningkatkan nilai Quadratic Weighted Kappa hingga mencapai 0,81 pada evaluasi lintas topik. Namun demikian, penelitian tersebut berfokus pada bahasa Inggris serta memerlukan komputasi fine-tuning yang sangat intensif, sehingga kurang aplikatif untuk implementasi server sekolah di Indonesia.

Penelitian kedua dilakukan oleh Pradani et al. (2023) yang mengembangkan sistem penilaian esai otomatis untuk bahasa Indonesia berbasis *Semantic Textual Similarity* menggunakan model IndoBERT [@pradani2023aes]. Penelitian tersebut membandingkan efektivitas IndoBERT dengan pendekatan ekstraksi fitur TF-IDF dan Word2Vec pada korpus ujian universitas. Temuan penelitian menunjukkan bahwa model IndoBERT berbasis kesamaan kosinus menghasilkan koefisien korelasi skor Pearson sebesar 0,76, jauh melampaui metode TF-IDF (0,48). Walaupun demikian, sistem yang dikembangkan belum menyediakan arsitektur multi-penilai dan belum terintegrasi ke dalam platform antarmuka operasional guru.

Penelitian ketiga oleh Wibowo et al. (2024) mengevaluasi performa penggabungan representasi teks mendalam ganda (*multiple deep representations*) untuk penilaian jawaban singkat berbahasa Indonesia [@wibowo2024indonesian]. Mereka menggabungkan fitur keluaran IndoBERT dengan representasi graf semantik dan model n-gram karakter untuk menangani jawaban yang memuat kesalahan ketik (*typo*). Hasilnya menunjukkan penurunan nilai RMSE hingga 12% dibandingkan model dasar. Meskipun akurasi meningkat, kompleksitas arsitektur model tersebut menuntut beban komputasi yang tinggi dan tidak dirancang untuk lingkungan asesmen kolaboratif guru.

Penelitian keempat dilakukan oleh Xiao et al. (2025) yang mengeksplorasi kerangka kerja kolaborasi manusia dan kecerdasan artifisial (*human-AI collaboration*) dalam penilaian tugas esai reflektif di perguruan tinggi [@xiao2025human]. Penelitian tersebut menegaskan bahwa guru tidak merasa nyaman menggunakan sistem AI yang bekerja secara otonom tanpa transparansi. Rekomendasi skor yang disertai dengan penandaan bagian teks yang relevan meningkatkan penerimaan guru sebesar 40% dan mempercepat durasi koreksi hingga 35%. Namun, penelitian tersebut belum mengintegrasikan pencatatan multi-rater terstandarisasi untuk ujian sekolah berskala besar.

Penelitian kelima oleh Prastyo dan Handayani (2025) melakukan analisis komparasi komprehensif terhadap berbagai model Transformer bahasa Indonesia (IndoBERT, RoBERTa-Indo, dan IndoELECTRA) pada tugas skoring teks terbuka [@prastyo2025comparative]. Hasil pengujian menyimpulkan bahwa varian *indobenchmark/indobert-base-p2* memiliki keunggulan stabilitas representasi semantik dan waktu inferensi tercepat pada lingkungan tanpa GPU akselerator. Penelitian tersebut memberikan landasan empiris yang kuat bagi pemilihan model IndoBERT dalam penelitian ini, namun belum menyajikan implementasi rancang bangun perangkat lunak sistem informasi.

Perbandingan komparatif antara penelitian-penelitian terdahulu tersebut dengan kontribusi penelitian yang diusulkan disajikan secara terstruktur pada Tabel 2.1.

Tabel 2.1 Perbandingan penelitian terdahulu dan posisi penelitian usulan

| Peneliti (Tahun) | Objek & Bahasa | Metode Utama | Kelebihan | Keterbatasan | Posisi Usulan Penelitian |
|:---|:---|:---|:---|:---|:---|
| Wang et al. (2022) [@wang2022bert] | Esai ASAP, Bahasa Inggris | Multi-Scale Hierarchical BERT | QWK mencapai 0.81 pada evaluasi lintas prompt | Beban training berat, fokus bahasa Inggris | Menitikberatkan teks bahasa Indonesia tanpa training berat |
| Pradani et al. (2023) [@pradani2023aes] | Ujian Kuliah, Bahasa Indonesia | IndoBERT + Cosine Similarity | Korelasi Pearson 0.76 melampaui TF-IDF | Belum ada platform web & multi-rater | Membangun platform web terpadu dengan multi-rater |
| Wibowo et al. (2024) [@wibowo2024indonesian] | Jawaban Pendek, Bahasa Indonesia | Hybrid Deep Embedding + Graph | Tahan terhadap kesalahan ketik (*typo*) | Komputasi kompleks, arsitektur rumit | Mengutamakan efisiensi inferensi ramah CPU sekolah |
| Xiao et al. (2025) [@xiao2025human] | Esai Mahasiswa, Bahasa Inggris | Human-AI Collaborative Scoring | Penerimaan guru tinggi, hemat waktu 35% | Belum ada audit multi-penilai terstandar | Menjamin rekonsiliasi audit multi-rater eksplisit |
| Prastyo & Handayani (2025) [@prastyo2025comparative] | Uji Terbuka, Bahasa Indonesia | Benchmark Transformer Indo | Inferensi IndoBERT tercepat & stabil | Hanya eksperimen model, tanpa aplikasi | Mengintegrasikan model ke sistem informasi operasional |
| **Penelitian Ini (2026)** | **Esai Ujian Sekolah, Bahasa Indonesia** | **Platform Web + IndoBERT + Multi-Rater** | **Transparan, jejak audit multi-penilai, siap pakai** | **Inferensi CPU tanpa fine-tuning berat** | **Solusi hulu-ke-hilir untuk guru di sekolah** |

Sumber: Hasil analisis literatur penelitian (2026)
