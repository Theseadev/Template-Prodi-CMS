from django.db import models
from django.utils.text import slugify


class IdentitasProdi(models.Model):
    """
    Model Singleton untuk menyimpan konfigurasi dan identitas Program Studi (White-label).
    Dapat diubah kapan saja melalui panel admin tanpa mengedit kode.
    """
    nama_prodi = models.CharField(max_length=150, default="Teknik Informatika", verbose_name="Nama Program Studi")
    fakultas = models.CharField(max_length=150, default="Fakultas Ilmu Komputer", verbose_name="Fakultas")
    universitas = models.CharField(max_length=150, default="Universitas Teknologi Nusantara", verbose_name="Nama Universitas / Institut")
    jenjang = models.CharField(
        max_length=10, 
        choices=[("D3", "D3"), ("D4", "D4"), ("S1", "S1"), ("S2", "S2"), ("S3", "S3")],
        default="S1", 
        verbose_name="Jenjang Pendidikan"
    )
    gelar_kelulusan = models.CharField(max_length=50, default="S.Kom.", verbose_name="Gelar Akademik Lulusan")
    akreditasi = models.CharField(
        max_length=50, 
        choices=[("Unggul", "Unggul"), ("A", "A"), ("Baik Sekali", "Baik Sekali"), ("Baik", "Baik"), ("Internasional", "Terakreditasi Internasional")],
        default="Unggul", 
        verbose_name="Status Akreditasi"
    )
    lembaga_akreditasi = models.CharField(max_length=100, default="LAM-INFOKOM", verbose_name="Lembaga Akreditasi (BAN-PT / LAM)")
    nomor_sk_akreditasi = models.CharField(max_length=150, blank=True, verbose_name="Nomor SK Akreditasi")
    
    # Tagline & Visi Misi
    tagline = models.CharField(max_length=255, default="Membentuk Talenta Unggul Masa Depan Berbasis Teknologi & Inovasi", verbose_name="Tagline Utama")
    visi = models.TextField(verbose_name="Visi Program Studi")
    misi = models.TextField(help_text="Gunakan baris baru atau nomor untuk setiap butir misi", verbose_name="Misi Program Studi")
    tujuan = models.TextField(blank=True, verbose_name="Tujuan Pendidikan")

    # Kaprodi
    nama_kaprodi = models.CharField(max_length=150, blank=True, verbose_name="Nama Ketua Program Studi (Kaprodi)")
    sambutan_kaprodi = models.TextField(blank=True, verbose_name="Sambutan Kaprodi")
    foto_kaprodi = models.ImageField(upload_to="identitas/", blank=True, null=True, verbose_name="Foto Kaprodi")

    # Aset Visual
    logo = models.ImageField(upload_to="identitas/", blank=True, null=True, verbose_name="Logo Program Studi / Kampus")
    favicon = models.ImageField(upload_to="identitas/", blank=True, null=True, verbose_name="Favicon")
    warna_tema_hex = models.CharField(max_length=7, default="#2563EB", verbose_name="Warna Tema Utama (Hex Code, misal: #2563EB)")

    # Kontak & Lokasi
    alamat_kampus = models.TextField(default="Gedung Rektorat Lt. 3, Kampus Utama", verbose_name="Alamat Lengkap Kampus")
    email_resmi = models.EmailField(default="prodi@kampus.ac.id", verbose_name="Email Resmi")
    telepon = models.CharField(max_length=30, default="(021) 1234567", verbose_name="Nomor Telepon Kantor")
    whatsapp_layanan = models.CharField(max_length=25, blank=True, help_text="Format: 6281234567890", verbose_name="WhatsApp Layanan / Konsultasi")

    # Call-to-Action & Eksternal Links
    url_pmb = models.URLField(default="https://pmb.kampus.ac.id", verbose_name="Link Portal PMB (Pendaftaran)")
    url_tracer_study = models.URLField(blank=True, verbose_name="Link Kuesioner Tracer Study Alumni")
    
    # Media Sosial
    instagram_url = models.URLField(blank=True, verbose_name="URL Instagram")
    youtube_url = models.URLField(blank=True, verbose_name="URL YouTube")
    linkedin_url = models.URLField(blank=True, verbose_name="URL LinkedIn")

    class Meta:
        verbose_name = "1. Pengaturan Identitas Prodi"
        verbose_name_plural = "1. Pengaturan Identitas Prodi"

    def __str__(self):
        return f"{self.jenjang} {self.nama_prodi} - {self.universitas}"

    def save(self, *args, **kwargs):
        # Memastikan hanya ada 1 baris setting identitas
        self.pk = 1
        super().save(*args, **kwargs)


class ProfilLulusan(models.Model):
    """
    Peluang Karir & Profil Lulusan ("Lulus Nanti Jadi Apa?")
    """
    nama_profesi = models.CharField(max_length=120, verbose_name="Nama Profesi / Peran Karir")
    deskripsi = models.TextField(verbose_name="Deskripsi Peran & Keahlian yang Dibekali")
    ikon = models.CharField(
        max_length=50, 
        default="code", 
        help_text="Nama icon (misal: code, shield, database, cpu, brain, rocket, chart)",
        verbose_name="Nama Ikon"
    )
    urutan = models.PositiveSmallIntegerField(default=1, verbose_name="Urutan Tampil")

    class Meta:
        verbose_name = "Profil Lulusan / Karir"
        verbose_name_plural = "Profil Lulusan / Karir"
        ordering = ["urutan"]

    def __str__(self):
        return self.nama_profesi


class ProgramUnggulan(models.Model):
    """
    Program Keunggulan Spesifik Prodi (Fast-Track, Kelas Internasional, MBKM, dll.)
    """
    judul = models.CharField(max_length=150, verbose_name="Nama Program Unggulan")
    deskripsi = models.TextField(verbose_name="Deskripsi Keunggulan & Manfaat")
    badge = models.CharField(max_length=50, blank=True, help_text="Contoh: 'Terfavorit', 'Bersertifikat Internasional'", verbose_name="Badge / Label Singkat")
    ikon = models.CharField(max_length=50, default="star", help_text="Contoh: star, globe, award, zap, users", verbose_name="Ikon Fitur")
    urutan = models.PositiveSmallIntegerField(default=1, verbose_name="Urutan Tampil")

    class Meta:
        verbose_name = "Program Unggulan"
        verbose_name_plural = "Program Unggulan"
        ordering = ["urutan"]

    def __str__(self):
        return self.judul


class Fasilitas(models.Model):
    """
    Fasilitas & Laboratorium Pendukung Perkuliahan
    """
    nama_fasilitas = models.CharField(max_length=150, verbose_name="Nama Fasilitas / Lab")
    deskripsi = models.TextField(verbose_name="Deskripsi Sarana & Kelengkapan")
    gambar = models.ImageField(upload_to="fasilitas/", blank=True, null=True, verbose_name="Foto Fasilitas")
    urutan = models.PositiveSmallIntegerField(default=1, verbose_name="Urutan Tampil")

    class Meta:
        verbose_name = "Fasilitas & Lab"
        verbose_name_plural = "Fasilitas & Lab"
        ordering = ["urutan"]

    def __str__(self):
        return self.nama_fasilitas


class Dosen(models.Model):
    """
    Direktori Tenaga Pendidik / Dosen Program Studi
    """
    JABATAN_CHOICES = [
        ("Tenaga Pendidik", "Tenaga Pendidik"),
        ("Asisten Ahli", "Asisten Ahli"),
        ("Lektor", "Lektor"),
        ("Lektor Kepala", "Lektor Kepala"),
        ("Guru Besar", "Guru Besar / Profesor"),
    ]

    nama_lengkap = models.CharField(max_length=200, verbose_name="Nama Lengkap & Gelar")
    nidn = models.CharField(max_length=30, blank=True, verbose_name="NIDN")
    nip = models.CharField(max_length=30, blank=True, verbose_name="NIP")
    jabatan_fungsional = models.CharField(max_length=50, choices=JABATAN_CHOICES, default="Lektor", verbose_name="Jabatan Fungsional")
    jabatan_struktural = models.CharField(max_length=100, blank=True, help_text="Contoh: Ketua Program Studi, Sekretaris Prodi, Kepala Lab AI", verbose_name="Jabatan Tambahan")
    bidang_keahlian = models.CharField(max_length=255, help_text="Contoh: Artificial Intelligence, Cyber Security, Software Architecture", verbose_name="Bidang Keahlian / Minat Riset")
    foto = models.ImageField(upload_to="dosen/", blank=True, null=True, verbose_name="Foto Resmi")
    email = models.EmailField(blank=True, verbose_name="Email Institusi")

    # Link Repositori Ilmiah
    url_sinta = models.URLField(blank=True, verbose_name="Link Profil SINTA")
    url_scholar = models.URLField(blank=True, verbose_name="Link Google Scholar")
    url_scopus = models.URLField(blank=True, verbose_name="Link Profil Scopus")
    url_linkedin = models.URLField(blank=True, verbose_name="Link LinkedIn")

    is_active = models.BooleanField(default=True, verbose_name="Status Aktif")
    urutan = models.PositiveSmallIntegerField(default=1, verbose_name="Urutan Tampil")

    class Meta:
        verbose_name = "Dosen & Pengajar"
        verbose_name_plural = "Dosen & Pengajar"
        ordering = ["urutan", "nama_lengkap"]

    def __str__(self):
        return self.nama_lengkap


class TestimoniAlumni(models.Model):
    """
    Testimoni Lulusan & Cerita Sukses Alumni
    """
    nama_alumni = models.CharField(max_length=150, verbose_name="Nama Lengkap Alumni")
    tahun_lulus = models.PositiveSmallIntegerField(verbose_name="Tahun Kelulusan")
    profesi_sekarang = models.CharField(max_length=150, verbose_name="Profesi / Jabatan Sekarang")
    nama_kantor = models.CharField(max_length=150, verbose_name="Perusahaan / Instansi Tempat Kerja")
    isi_testimoni = models.TextField(verbose_name="Pesan Testimoni")
    foto = models.ImageField(upload_to="alumni/", blank=True, null=True, verbose_name="Foto Alumni")
    linkedin_url = models.URLField(blank=True, verbose_name="Profil LinkedIn")
    is_featured = models.BooleanField(default=True, verbose_name="Tampilkan di Beranda Utama")
    urutan = models.PositiveSmallIntegerField(default=1, verbose_name="Urutan")

    class Meta:
        verbose_name = "Testimoni Alumni"
        verbose_name_plural = "Testimoni Alumni"
        ordering = ["urutan", "-tahun_lulus"]

    def __str__(self):
        return f"{self.nama_alumni} - {self.profesi_sekarang} ({self.nama_kantor})"


class MitraKerjasama(models.Model):
    """
    Mitra Industri, Dunia Usaha, Kampus Luar Negeri, atau Lembaga Sertifikasi
    """
    KATEGORI_CHOICES = [
        ("Industri", "Dunia Usaha & Industri"),
        ("Universitas", "Perguruan Tinggi Mitra (Dalam / Luar Negeri)"),
        ("Pemerintah", "Instansi Pemerintah / BUMN"),
        ("Sertifikasi", "Lembaga Sertifikasi Internasional"),
    ]

    nama_mitra = models.CharField(max_length=150, verbose_name="Nama Institusi / Perusahaan")
    kategori = models.CharField(max_length=30, choices=KATEGORI_CHOICES, default="Industri", verbose_name="Kategori Mitra")
    logo_mitra = models.ImageField(upload_to="mitra/", blank=True, null=True, verbose_name="Logo Mitra (Transparan disarankan)")
    url_logo_eksternal = models.URLField(blank=True, help_text="Tautan logo eksternal (SVG/PNG transparan)", verbose_name="URL Logo Eksternal")
    website_mitra = models.URLField(blank=True, verbose_name="Website Resmi Mitra")
    urutan = models.PositiveSmallIntegerField(default=1, verbose_name="Urutan")

    class Meta:
        verbose_name = "Mitra Kerjasama"
        verbose_name_plural = "Mitra Kerjasama"
        ordering = ["urutan", "nama_mitra"]

    def __str__(self):
        return self.nama_mitra


class Prestasi(models.Model):
    """
    Pencapaian & Prestasi Mahasiswa dan Dosen
    """
    TINGKAT_CHOICES = [
        ("Regional", "Regional / Wilayah"),
        ("Nasional", "Tingkat Nasional"),
        ("Internasional", "Tingkat Internasional"),
    ]
    KATEGORI_CHOICES = [
        ("Mahasiswa", "Prestasi Mahasiswa"),
        ("Dosen", "Prestasi Dosen"),
    ]

    judul_prestasi = models.CharField(max_length=200, verbose_name="Judul Prestasi / Kejuaraan")
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES, default="Mahasiswa", verbose_name="Kategori")
    tingkat = models.CharField(max_length=20, choices=TINGKAT_CHOICES, default="Nasional", verbose_name="Tingkat Prestasi")
    peraih = models.CharField(max_length=255, help_text="Nama individu atau tim peraih prestasi", verbose_name="Nama Peraih / Tim")
    tahun = models.PositiveSmallIntegerField(default=2026, verbose_name="Tahun Perolehan")
    deskripsi = models.TextField(blank=True, verbose_name="Keterangan Lomba / Penyelenggara")
    foto = models.ImageField(upload_to="prestasi/", blank=True, null=True, verbose_name="Foto Dokumentasi / Sertifikat")

    class Meta:
        verbose_name = "Prestasi Mahasiswa & Dosen"
        verbose_name_plural = "Prestasi Mahasiswa & Dosen"
        ordering = ["-tahun", "tingkat"]

    def __str__(self):
        return f"{self.judul_prestasi} ({self.tingkat} - {self.tahun})"


class MataKuliah(models.Model):
    """
    Struktur Kurikulum dan Silabus
    """
    SEMESTER_CHOICES = [(i, f"Semester {i}") for i in range(1, 9)]

    kode_mk = models.CharField(max_length=20, verbose_name="Kode Mata Kuliah")
    nama_mk = models.CharField(max_length=150, verbose_name="Nama Mata Kuliah")
    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES, verbose_name="Semester")
    sks_teori = models.PositiveSmallIntegerField(default=2, verbose_name="SKS Teori")
    sks_praktikum = models.PositiveSmallIntegerField(default=1, verbose_name="SKS Praktikum")
    is_wajib = models.BooleanField(default=True, verbose_name="Mata Kuliah Wajib? (Jika tidak, Mata Kuliah Pilihan)")
    deskripsi = models.TextField(blank=True, verbose_name="Deskripsi Singkat / Capaian Pembelajaran")
    file_rps = models.FileField(upload_to="rps/", blank=True, null=True, verbose_name="File RPS / Silabus (PDF)")

    @property
    def total_sks(self):
        return self.sks_teori + self.sks_praktikum

    class Meta:
        verbose_name = "Mata Kuliah (Kurikulum)"
        verbose_name_plural = "Mata Kuliah (Kurikulum)"
        ordering = ["semester", "kode_mk"]

    def __str__(self):
        return f"[{self.kode_mk}] {self.nama_mk} ({self.total_sks} SKS)"


class KategoriBerita(models.Model):
    nama = models.CharField(max_length=100, verbose_name="Nama Kategori")
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Kategori Berita"
        verbose_name_plural = "Kategori Berita"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama


class Berita(models.Model):
    """
    Publikasi Berita, Pengumuman, dan Agenda Kegiatan
    """
    TIPE_CHOICES = [
        ("Berita", "Berita / Liputan"),
        ("Pengumuman", "Pengumuman Akademik"),
        ("Agenda", "Agenda / Event"),
    ]

    judul = models.CharField(max_length=255, verbose_name="Judul Artikel")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    tipe = models.CharField(max_length=20, choices=TIPE_CHOICES, default="Berita", verbose_name="Tipe Konten")
    kategori = models.ForeignKey(KategoriBerita, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kategori")
    ringkasan = models.TextField(help_text="Cuplikan singkat untuk kartu berita di beranda", verbose_name="Ringkasan Singkat")
    konten = models.TextField(verbose_name="Isi Lengkap Konten")
    gambar_sampul = models.ImageField(upload_to="berita/", blank=True, null=True, verbose_name="Foto Sampul / Banner")
    url_gambar_eksternal = models.URLField(blank=True, help_text="URL gambar online jika tidak mengunggah file", verbose_name="URL Gambar Eksternal")
    
    # Khusus Agenda
    tanggal_agenda = models.DateField(blank=True, null=True, verbose_name="Tanggal Acara (Jika Agenda)")
    lokasi_agenda = models.CharField(max_length=150, blank=True, verbose_name="Tempat / Lokasi Acara")

    tanggal_publikasi = models.DateTimeField(auto_now_add=True, verbose_name="Tanggal Diterbitkan")
    is_published = models.BooleanField(default=True, verbose_name="Publikasikan?")
    views = models.PositiveIntegerField(default=0, verbose_name="Jumlah Dilihat")

    class Meta:
        verbose_name = "Berita, Pengumuman & Agenda"
        verbose_name_plural = "Berita, Pengumuman & Agenda"
        ordering = ["-tanggal_publikasi"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.judul)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.tipe}] {self.judul}"


class KategoriDokumen(models.Model):
    nama = models.CharField(max_length=100, verbose_name="Nama Kategori Dokumen")

    class Meta:
        verbose_name = "Kategori Dokumen Unduhan"
        verbose_name_plural = "Kategori Dokumen Unduhan"

    def __str__(self):
        return self.nama


class DokumenAkademik(models.Model):
    """
    Pusat Unduhan (Pedoman Skripsi, Magang, Borang, Formulir)
    """
    nama_dokumen = models.CharField(max_length=200, verbose_name="Nama Berkas / Dokumen")
    kategori = models.ForeignKey(KategoriDokumen, on_delete=models.CASCADE, verbose_name="Kategori Dokumen")
    file_dokumen = models.FileField(upload_to="dokumen/", verbose_name="File Berkas (PDF/DOCX/ZIP)")
    deskripsi = models.CharField(max_length=255, blank=True, verbose_name="Keterangan Singkat")
    tanggal_unggah = models.DateField(auto_now_add=True, verbose_name="Tanggal Unggah")
    download_count = models.PositiveIntegerField(default=0, verbose_name="Jumlah Unduhan")

    class Meta:
        verbose_name = "Dokumen Akademik & Unduhan"
        verbose_name_plural = "Dokumen Akademik & Unduhan"
        ordering = ["kategori", "nama_dokumen"]

    def __str__(self):
        return f"{self.nama_dokumen} ({self.kategori.nama})"


class FAQ(models.Model):
    """
    Pertanyaan yang Sering Diajukan (FAQ)
    """
    pertanyaan = models.CharField(max_length=255, verbose_name="Pertanyaan")
    jawaban = models.TextField(verbose_name="Jawaban Lengkap")
    urutan = models.PositiveSmallIntegerField(default=1, verbose_name="Urutan Tampil")

    class Meta:
        verbose_name = "FAQ (Tanya Jawab)"
        verbose_name_plural = "FAQ (Tanya Jawab)"
        ordering = ["urutan"]

    def __str__(self):
        return self.pertanyaan


class HeroSlider(models.Model):
    """
    Banner Carousel / Hero Slider Halaman Beranda Kampus
    """
    judul = models.CharField(max_length=200, verbose_name="Judul Slide")
    subjudul = models.CharField(max_length=255, blank=True, verbose_name="Tagline / Badge Singkat")
    deskripsi = models.TextField(verbose_name="Deskripsi / Ringkasan Slide")
    gambar = models.ImageField(upload_to="slider/", blank=True, null=True, verbose_name="Unggah Foto Latar")
    url_gambar_eksternal = models.URLField(blank=True, help_text="Opsional: URL gambar resolusi tinggi jika tidak mengunggah berkas", verbose_name="URL Gambar Eksternal")
    label_tombol = models.CharField(max_length=50, default="Pelajari Selengkapnya", verbose_name="Teks Tombol Utama")
    url_tombol = models.CharField(max_length=255, default="/profil/", verbose_name="Tautan Tombol Utama")
    label_tombol_sekunder = models.CharField(max_length=50, blank=True, verbose_name="Teks Tombol Sekunder (Opsional)")
    url_tombol_sekunder = models.CharField(max_length=255, blank=True, verbose_name="Tautan Tombol Sekunder")
    urutan = models.PositiveSmallIntegerField(default=1, verbose_name="Urutan Tampil")
    is_active = models.BooleanField(default=True, verbose_name="Aktif?")

    class Meta:
        verbose_name = "Hero Slider (Beranda)"
        verbose_name_plural = "Hero Slider (Beranda)"
        ordering = ["urutan"]

    def __str__(self):
        return self.judul

