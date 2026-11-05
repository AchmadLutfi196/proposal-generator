# Resolusi Konflik Aturan Penulisan (Precedence Policy)

Dalam penyusunan naskah akademik di lingkungan Jurusan Teknik Informatika Fakultas Teknik Universitas Trunojoyo Madura, terdapat beberapa dokumen pedoman yang diterbitkan pada kurun waktu berbeda:
1. **Daftar Cek Seminar Proposal Teknik Informatika (TIF) v06** (Dokumen operasional pengujian terbaru yang digunakan oleh penguji seminar proposal).
2. **Template Proposal Skripsi Resmi FT UTM** (`Template_Proposal.md` / `Template_Proposal.pdf`).
3. **Buku Panduan Penulisan Skripsi FT UTM (Signed)** (Dokumen umum tingkat fakultas).

Guna mencegah ketidakpastian implementasi teknis pada script generator dan validator otomatis, framework ini menerapkan **Kebijakan Presedensi Ketat**:

$$\text{Ceklist Seminar Proposal v06} \succ \text{Template Proposal Resmi} \succ \text{Buku Panduan Fakultas}$$

---

## Rincian Rekonsiliasi Perbedaan Aturan

| Parameter | Ceklist v06 | Template Resmi | Panduan Fakultas §6–§7 | Keputusan Framework (`proposal-generator`) |
|:---|:---|:---|:---|:---|
| **Penomoran Bagian Awal** | Romawi kecil (`i, ii, iii...`) di bawah-tengah; cover tanpa nomor | Romawi kecil (`i, ii`) | Di beberapa bagian tertulis angka arab | **Mengikuti Ceklist & Template:** Bagian awal menggunakan `lowerRoman` di bawah-tengah, cover tanpa nomor. |
| **Penomoran Subbab** | `2.1 Subbab` (tanpa titik di akhir nomor) | `2.1 Subbab` | Kadang dicontohkan `2.1. Subbab` | **Mengikuti Ceklist:** `heading_sub_dot: false` (contoh: `2.1 Latar Belakang`). |
| **Format Caption Tabel** | `Tabel 2.1 Judul Tabel` | `Tabel 2.1 Judul Tabel` | Ditulis `Tabel 6. 1` (ada spasi) | **Mengikuti Ceklist:** `Tabel X.Y` rapat tanpa spasi di antara nomor bab dan nomor urut. |
| **Dosen Pembimbing di Cover** | Diperiksa oleh Pembimbing 1 & 2 | Menampilkan Pembimbing 1 & 2 dengan NIP | Cover skripsi final tidak menampilkan pembimbing | **Mengikuti Template Proposal:** Menampilkan nama dan NIP Dosen Pembimbing I dan II di halaman judul proposal. |
| **Gaya Sitasi & Bibliografi** | Format APA, namun dalam teks menggunakan angka kurung siku `[3]`, `[5–8]` urut kemunculan | Sitasi APA bernomor | Sitasi APA author-date standar | **Mengikuti Ceklist:** Menerapkan CSL `apa-numeric.csl` (sitasi numerik kurung siku dengan metadata bibliografi APA). |
| **Batas Latar Belakang** | Minimal 1000 kata atau > 5 kali abstrak | Dijabarkan mendalam | Tidak ada angka eksplisit | **Mengikuti Ceklist:** Validator memvalidasi minimal 1000 kata pada Latar Belakang. |
| **Penelitian Terdahulu** | Minimal 5 penelitian, 1 paragraf per penelitian, total $\ge 2$ halaman | Minimal 5 penelitian dengan tabel komparasi | Minimal 5 penelitian | **Mengikuti Ceklist:** Wajib $\ge 5$ penelitian terdahulu yang dirujuk dengan tabel perbandingan. |
