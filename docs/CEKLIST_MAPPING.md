# Pemetaan Otomasi Ceklist Seminar Proposal FT UTM v06

Berikut adalah matriks pemetaan seluruh butir pada dokumen **Daftar Cek Seminar Proposal Teknik Informatika (TIF) FT UTM v06** terhadap modul otomasi di dalam framework `proposal-generator`.

---

## Matriks Otomasi Ceklist

| Kode Rule | Butir Pengecekan pada Ceklist v06 | Modul Pelaksana di Framework | Status Otomasi |
|:---|:---|:---|:---:|
| `ADM-01` | Lulus Mata Kuliah minimal 120 sks | Verifikasi administrasi di SISRI | Manual |
| `ADM-02` | Sudah lulus Mata Kuliah Kerja Praktek | Verifikasi administrasi di SISRI | Manual |
| `ADM-03` | Referensi jurnal/prosiding $\ge 5$ ($\le 5$ th) dan textbook $\ge 5$ ($\le 20$ th) | `scripts/check_proposal.py` mem-parsing `references.bib` | **Otomatis** |
| `ADM-04` | Kelayakan/kedalaman topik skripsi sesuai Bidang Minat | Penilaian Dosen Pembimbing | Manual |
| `ADM-05` | Perkiraan waktu penelitian tidak lebih dari 2 semester | Logbook Skripsi | Manual |
| `ADM-06` | Menunjukkan rencana kerja (Jadwal Kegiatan) | Tabel 1.1 pada `01-pendahuluan.md` | **Otomatis** |
| `ADM-07` | Pengajuan dosen pembimbing pada SISRI | SISRI UTM | Manual |
| `ADM-08` | Minimal 2 kali konsultasi dibuktikan Logbook Skripsi | Logbook SISRI | Manual |
| `ADM-09` | Pengecekan plagiarisme dan penggunaan AI | Turnitin / AI Detector | Manual |
| `ADM-10` | Pendaftaran seminar proposal melalui SISRI | SISRI UTM | Manual |
| `TYP-01` | Ukuran kertas A4 ($21\text{ cm} \times 29{,}7\text{ cm}$) | `templates/reference.docx` & `presets/utm-proposal.yml` | **Otomatis** |
| `TYP-02` | Margin: Atas 3 cm, Kiri 4 cm, Bawah 3 cm, Kanan 3 cm | `make_reference_docx.py` & `check_proposal.py` | **Otomatis** |
| `TYP-03` | Jarak spasi 1.5 antar baris pada naskah utama | Gaya `Normal` line="360" di OpenXML | **Otomatis** |
| `TYP-04` | Font Times New Roman 12 pt, Judul 14 pt Bold | Gaya `Normal`, `Heading1` di OpenXML | **Otomatis** |
| `NUM-01` | Format footer "different first page" | `scripts/finalize_docx.py` menyisipkan `<w:titlePg/>` | **Otomatis** |
| `NUM-02` | Bagian awal romawi kecil (`i, ii...`) bawah-tengah, cover tanpa nomor | `finalize_docx.py` `<w:pgNumType w:fmt="lowerRoman"/>` | **Otomatis** |
| `NUM-03` | Bagian inti angka arab (awal bab bawah-tengah, lanjutan kanan-atas) | `finalize_docx.py` & header-footer reference | **Otomatis** |
| `NUM-04` | Subbab angka (`1.1`), sub-subbab maksimal 3 angka (`1.1.1`) rata kiri | `templates/docx.lua` (`heading_sub_dot: false`) | **Otomatis** |
| `FIG-01` | Gambar dan tabel disajikan jelas / tidak kabur ($\ge 150\text{ DPI}$) | `scripts/render_figures.py` menghasilkan 200–300 DPI | **Otomatis** |
| `FIG-02` | Font isi tabel, caption tabel dan gambar ukuran 12 pt spasi 1.0 | Style `CaptionFigure`, `CaptionTable`, `Source` | **Otomatis** |
| `FIG-03` | Nomor tabel (contoh: `Tabel 2.1`) diletakkan di SEBELAH ATAS | `docx.lua` & format naskah | **Otomatis** |
| `FIG-04` | Nomor gambar (contoh: `Gambar 3.1`) diletakkan di SEBELAH BAWAH | `docx.lua` & format naskah | **Otomatis** |
| `FIG-05` | Gambar/tabel bukan dokumentasi pribadi wajib ada baris Sumber | Format paragraf `Source` | **Otomatis** |
| `CIT-01` | Kutipan dalam teks menggunakan nomor urut kemunculan `[3]`, `[5–8]` | `templates/apa-numeric.csl` via pandoc `--citeproc` | **Otomatis** |
| `CIT-02` | Daftar Pustaka format APA berurutan kemunculan | `apa-numeric.csl` layout | **Otomatis** |
| `CIT-03` | Kesesuaian timbal balik (*two-way match*) teks dan Daftar Pustaka | `scripts/check_proposal.py` mengaudit relasi naskah-.bib | **Otomatis** |
| `TTL-01` | Judul memuat 3 komponen: Objek, Tujuan, dan Metode | `check_proposal.py` deteksi komponen | **Otomatis** |
| `TTL-02` | Panjang judul proposal antara 8 sampai 12 kata | `check_proposal.py` menghitung jumlah kata judul | **Otomatis** |
| `TTL-03` | Judul diketik huruf kapital semua tanpa singkatan | `docx.lua` fungsi `balance_title(text:upper())` | **Otomatis** |
| `TTL-04` | Susunan judul piramida terbalik (huruf V) atau sejajar | `docx.lua` dynamic programming title balance | **Otomatis** |
| `TTL-05` | Lambang UTM pentagon ukuran diameter 4 cm | `docx.lua` Image width="4cm" | **Otomatis** |
| `TTL-06` | Nama penulis lengkap tanpa singkatan, NPM di bawah nama | `metadata.yml` parsing & `docx.lua` cover block | **Otomatis** |
| `ABS-01` | Abstrak 1 paragraf ringkas (masalah, tujuan, metode) | `check_proposal.py` hitung jumlah paragraf | **Otomatis** |
| `ABS-02` | Abstrak maksimal 200 kata, spasi tunggal 1.0, tanpa kutipan | `check_proposal.py` & style `AbstractBody` | **Otomatis** |
| `ABS-03` | Kata kunci 3–5 kata dan tertera di dalam naskah abstrak | `check_proposal.py` pencocokan kata kunci | **Otomatis** |
| `CH1-01` | Subbab Bab I: Latar Belakang, Rumusan Masalah, Tujuan & Manfaat, Batasan | `check_proposal.py` deteksi heading Bab 1 | **Otomatis** |
| `CH1-02` | Latar Belakang minimal 1000 kata | `check_proposal.py` token word counter | **Otomatis** |
| `CH1-03` | Rumusan masalah kalimat tanya, 5W+1H, penomoran angka | `check_proposal.py` parsing penomoran & tanda tanya | **Otomatis** |
| `CH2-01` | Subbab Bab II: Teori Dasar dan Penelitian Terdahulu | `check_proposal.py` deteksi heading Bab 2 | **Otomatis** |
| `CH2-02` | Penelitian terdahulu minimal 5 penelitian, format perbandingan | `check_proposal.py` menghitung sitasi penelitian | **Otomatis** |
| `CH3-01` | Subbab Bab III: Pengumpulan data dan metode/alat yang digunakan | `check_proposal.py` deteksi komponen metodologi | **Otomatis** |
