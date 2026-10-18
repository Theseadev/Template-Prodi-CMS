from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portal.models import (
    IdentitasProdi, ProfilLulusan, ProgramUnggulan, Fasilitas,
    Dosen, TestimoniAlumni, MitraKerjasama, Prestasi,
    MataKuliah, KategoriBerita, Berita, KategoriDokumen, DokumenAkademik, FAQ
)


class Command(BaseCommand):
    help = "Mengisi database dengan data awal realistis untuk template CMS Program Studi"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Memulai seeding data awal CMS Program Studi..."))

        # 1. Superuser
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@kampus.ac.id", "admin123")
            self.stdout.write(self.style.SUCCESS("[OK] Superuser dibuat: admin / admin123"))

        # 2. Identitas Prodi (Singleton)
        identitas, _ = IdentitasProdi.objects.get_or_create(
            pk=1,
            defaults={
                "nama_prodi": "Teknik Informatika",
                "fakultas": "Fakultas Ilmu Komputer & Teknologi Informasi",
                "universitas": "Universitas Teknologi Nusantara",
                "jenjang": "S1",
                "gelar_kelulusan": "S.Kom.",
                "akreditasi": "Unggul",
                "lembaga_akreditasi": "LAM-INFOKOM",
                "nomor_sk_akreditasi": "SK-042/LAM-INFOKOM/Akred/S1/2025",
                "tagline": "Membentuk Inovator Teknologi Global yang Berdaya Saing, Berintegritas, dan Adaptif",
                "visi": "Menjadi program studi unggulan bereputasi internasional dalam bidang Rekayasa Perangkat Lunak dan Kecerdasan Buatan yang berakar pada nilai-nilai integritas dan inovasi berkelanjutan pada tahun 2030.",
                "misi": (
                    "1. Menyelenggarakan pendidikan sarjana berstandar global dengan kurikulum mutakhir berbasis OBE dan MBKM.\n"
                    "2. Menghasilkan riset inovatif dan solutif di bidang teknologi informasi yang diakui secara nasional maupun internasional.\n"
                    "3. Mengimplementasikan pengabdian kepada masyarakat berbasis transformasi digital untuk kesejahteraan bangsa.\n"
                    "4. Memperluas kerjasama strategis dengan dunia usaha, dunia industri, dan institusi pendidikan global."
                ),
                "tujuan": "Menghasilkan lulusan sarjana komputer yang kompeten, mandiri, berjiwa kewirausahaan teknologi (technopreneur), dan siap memimpin transformasi digital di era industri 4.0 dan masyarakat 5.0.",
                "nama_kaprodi": "Dr. Eng. Ir. Hendra Gunawan, S.Kom., M.T.",
                "sambutan_kaprodi": (
                    "Selamat datang di portal resmi Program Studi Teknik Informatika Universitas Teknologi Nusantara. "
                    "Kami berkomitmen menyediakan lingkungan belajar dinamis yang menggabungkan penguasaan dasar keilmuan komputer "
                    "yang kokoh dengan praktik langsung pada proyek nyata industri. Melalui bimbingan para dosen berkualifikasi tinggi "
                    "dan kolaborasi mitra teknologi global, kami mendidik mahasiswa bukan sekadar menjadi pengguna teknologi, "
                    "melainkan pencipta solusi inovatif masa depan."
                ),
                "warna_tema_hex": "#2563EB",
                "alamat_kampus": "Gedung Menara Sains Lt. 4, Jl. Technopark Raya No. 1, Kawasan Edukasi Digital, Nusantara",
                "email_resmi": "informatika@utn.ac.id",
                "telepon": "(021) 7890123",
                "whatsapp_layanan": "6281234567890",
                "url_pmb": "https://pmb.kampus.ac.id",
                "url_tracer_study": "https://tracer.kampus.ac.id/prodi/if",
                "instagram_url": "https://instagram.com/if_kampus",
                "youtube_url": "https://youtube.com/@if_kampus",
                "linkedin_url": "https://linkedin.com/school/if-kampus",
            }
        )
        self.stdout.write(self.style.SUCCESS("[OK] Identitas Prodi berhasil diset."))

        # 3. Profil Lulusan
        profil_data = [
            ("Software Engineer & Architect", "Merancang, mengembangkan, dan memelihara aplikasi web skala besar, mobile, dan sistem arsitektur microservices berbasis cloud modern.", 1),
            ("AI & Machine Learning Specialist", "Membangun sistem komputasi cerdas, pemrosesan bahasa alami (NLP), dan computer vision untuk otomatisasi dan analitik prediktif.", 2),
            ("Cyber Security & Cloud Engineer", "Menjaga keamanan data sistem informasi, melakukan audit keamanan siber, dan mengelola infrastruktur cloud DevOps terdistribusi.", 3),
            ("Data Engineer & Big Data Analyst", "Membangun pipeline data skala terabyte, data warehousing, dan menyediakan data mart untuk pengambilan keputusan bisnis strategis.", 4),
            ("IT Project Manager & Consultant", "Memimpin tim rekayasa perangkat lunak dengan metodologi Agile/Scrum serta memberikan konsultasi transformasi digital institusi.", 5),
            ("Technology Entrepreneur (Technopreneur)", "Mendirikan dan mengembangkan startup teknologi berbasis produk inovatif pemecah masalah riil masyarakat.", 6),
        ]
        for nama, desk, urut in profil_data:
            ProfilLulusan.objects.get_or_create(nama_profesi=nama, defaults={"deskripsi": desk, "urutan": urut})
        self.stdout.write(self.style.SUCCESS("[OK] Profil Lulusan berhasil diset."))

        # 4. Program Unggulan
        unggulan_data = [
            ("Program Fast-Track S1 & S2", "Raih gelar Sarjana (S.Kom.) dan Magister Komputer (M.Kom.) secara berkesinambungan hanya dalam kurun waktu 5 tahun penuh.", "Akademik Cepat", 1),
            ("Magang MBKM Bersertifikat", "Program magang terakreditasi selama 1-2 semester di perusahaan unicorn dan industri teknologi global dengan konversi 20 SKS.", "Siap Kerja", 2),
            ("Sertifikasi Internasional Gratis", "Voucher ujian sertifikasi resmi vendor global (AWS Certified, Cisco CCNA, Red Hat Certified) yang didanai universitas.", "Sertifikasi Global", 3),
            ("Inkubator Startup Mahasiswa", "Pendanaan awal (seed funding), fasilitas co-working, dan mentoring eksklusif dari founder startup ternama untuk proyek tugas akhir.", "Technopreneur", 4),
        ]
        for judul, desk, badge, urut in unggulan_data:
            ProgramUnggulan.objects.get_or_create(judul=judul, defaults={"deskripsi": desk, "badge": badge, "urutan": urut})
        self.stdout.write(self.style.SUCCESS("[OK] Program Unggulan berhasil diset."))

        # 5. Fasilitas & Lab
        fasilitas_data = [
            ("Laboratorium Kecerdasan Buatan & Data", "Dilengkapi dengan GPU Workstation berkecepatan tinggi untuk riset Deep Learning, Computer Vision, dan NLP.", 1),
            ("Laboratorium Rekayasa Perangkat Lunak & Cloud", "Sarana praktikum arsitektur sistem enterprise, automated testing, dan CI/CD pipeline berbasis private cloud.", 2),
            ("Studio Multimedia, AR/VR & Game Dev", "Dilengkapi perangkat VR Headset (Meta Quest), render farm, dan display pen untuk perancangan aplikasi imersif.", 3),
            ("Laboratorium Jaringan & Keamanan Siber", "Peralatan router & switch industri Cisco terpusat serta server simulasi ethical hacking dan penetration testing.", 4),
        ]
        for nama, desk, urut in fasilitas_data:
            Fasilitas.objects.get_or_create(nama_fasilitas=nama, defaults={"deskripsi": desk, "urutan": urut})
        self.stdout.write(self.style.SUCCESS("[OK] Fasilitas berhasil diset."))

        # 6. Dosen & Peneliti
        dosen_data = [
            ("Dr. Eng. Ir. Hendra Gunawan, S.Kom., M.T.", "1234567801", "198005122005011002", "Lektor Kepala", "Ketua Program Studi", "Software Architecture, Distributed Systems, Cloud Computing", "hendra.gunawan@utn.ac.id", 1),
            ("Prof. Dr. Ir. Sri Wahyuni, M.Sc., Ph.D.", "1234567802", "197508241999032001", "Guru Besar", "Kepala Lab AI", "Artificial Intelligence, Deep Learning, Medical Imaging", "sri.wahyuni@utn.ac.id", 2),
            ("Ahmad Fauzi, S.Kom., M.Kom., Ph.D.", "1234567803", "198801152012121001", "Lektor", "Sekretaris Program Studi", "Cyber Security, Cryptography, Blockchain Technology", "ahmad.fauzi@utn.ac.id", 3),
            ("Dewi Sartika, S.Kom., M.T., Ph.D.", "1234567804", "198904202015042002", "Lektor", "Kepala Lab RPL", "Human-Computer Interaction (HCI), UI/UX Research, Mobile Computing", "dewi.sartika@utn.ac.id", 4),
            ("Bambang Kurniawan, S.T., M.Kom.", "1234567805", "199209102018011003", "Asisten Ahli", "", "Data Engineering, Big Data Analytics, Knowledge Graph", "bambang.k@utn.ac.id", 5),
            ("Rian Hidayat, S.Kom., M.Cs.", "1234567806", "199302142020121004", "Asisten Ahli", "", "Internet of Things (IoT), Embedded Systems, Computer Networks", "rian.hidayat@utn.ac.id", 6),
        ]
        for nama, nidn, nip, jab_fung, jab_struk, keahlian, email, urut in dosen_data:
            Dosen.objects.get_or_create(
                nidn=nidn,
                defaults={
                    "nama_lengkap": nama,
                    "nip": nip,
                    "jabatan_fungsional": jab_fung,
                    "jabatan_struktural": jab_struk,
                    "bidang_keahlian": keahlian,
                    "email": email,
                    "url_sinta": "https://sinta.kemdikbud.go.id",
                    "url_scholar": "https://scholar.google.com",
                    "url_linkedin": "https://linkedin.com",
                    "urutan": urut,
                }
            )
        self.stdout.write(self.style.SUCCESS("[OK] Data Dosen berhasil diset."))

        # 7. Testimoni Alumni
        testi_data = [
            ("Andi Pratama, S.Kom.", 2022, "Senior Software Engineer", "GoTo Financial (Gojek)", "Materi kuliah yang diajarkan sangat relevan dengan kebutuhan industri. Magang MBKM dan proyek bersama dosen membuat saya sangat siap bersaing di tech startup decacorn.", 1),
            ("Siti Rahmawati, S.Kom.", 2023, "Cloud Security Analyst", "Bank Mandiri Persero", "Fasilitas lab jaringan dan bimbingan sertifikasi gratis di prodi menjadi batu loncatan terbesar saya untuk langsung direkrut di perbankan nasional sebelum wisuda.", 2),
            ("Budi Santoso, S.Kom.", 2021, "AI Research Engineer", "PT Telkom Indonesia", "Pembelajaran riset mandiri di lab AI membentuk daya nalar analitis yang kuat untuk merancang model machine learning yang diterapkan pada skala jutaan pengguna.", 3),
        ]
        for nama, thn, prof, kantor, isi, urut in testi_data:
            TestimoniAlumni.objects.get_or_create(nama_alumni=nama, defaults={"tahun_lulus": thn, "profesi_sekarang": prof, "nama_kantor": kantor, "isi_testimoni": isi, "urutan": urut})
        self.stdout.write(self.style.SUCCESS("[OK] Testimoni Alumni berhasil diset."))

        # 8. Mitra Kerjasama
        mitra_data = [
            ("PT Telkom Indonesia (Persero) Tbk", "Industri", "https://telkom.co.id", 1),
            ("Bank Central Asia (BCA)", "Industri", "https://bca.co.id", 2),
            ("GoTo (Gojek Tokopedia)", "Industri", "https://goto.com", 3),
            ("Kementerian Komunikasi dan Informatika RI", "Pemerintah", "https://kominfo.go.id", 4),
            ("AWS Academy (Amazon Web Services)", "Sertifikasi", "https://aws.amazon.com", 5),
            ("Universitas Teknologi Malaysia (UTM)", "Universitas", "https://utm.my", 6),
        ]
        for nama, kat, web, urut in mitra_data:
            MitraKerjasama.objects.get_or_create(nama_mitra=nama, defaults={"kategori": kat, "website_mitra": web, "urutan": urut})
        self.stdout.write(self.style.SUCCESS("[OK] Mitra Kerjasama berhasil diset."))

        # 9. Prestasi
        prestasi_data = [
            ("Juara 1 Pagelaran Mahasiswa Nasional TIK (GEMASTIK)", "Mahasiswa", "Nasional", "Tim Algoritma Juara (Rizky, Fajar, Dimas)", 2025, "Kategori Pengembangan Perangkat Lunak tingkat nasional diselenggarakan Kemendikbudristek."),
            ("Pemenang Global Imagine Cup Regional APAC", "Mahasiswa", "Internasional", "Tim IoT Nusantara (Sarah, Bima)", 2024, "Inovasi sistem deteksi dini kebakaran hutan berbasis AIoT dan citra satelit."),
            ("Penerima Pendanaan Riset Terapan Kemendikbud", "Dosen", "Nasional", "Dr. Eng. Hendra Gunawan & Tim", 2025, "Pengembangan platform arsitektur microservices untuk tata kelola data cerdas kampus."),
        ]
        for judul, kat, ting, peraih, thn, desk in prestasi_data:
            Prestasi.objects.get_or_create(judul_prestasi=judul, defaults={"kategori": kat, "tingkat": ting, "peraih": peraih, "tahun": thn, "deskripsi": desk})
        self.stdout.write(self.style.SUCCESS("[OK] Prestasi berhasil diset."))

        # 10. Mata Kuliah (Sampel representatif tiap semester 1-8)
        matkul_data = [
            # Sem 1
            ("IF101", "Algoritma & Pemrograman I", 1, 2, 2, True, "Dasar logika komputasi, struktur kendali, array, dan fungsi menggunakan Python."),
            ("IF102", "Matematika Diskrit", 1, 3, 0, True, "Teori himpunan, relasi, logika proposisi, induksi matematika, dan teori graf."),
            ("IF103", "Pengantar Teknologi Informasi", 1, 2, 0, True, "Konsep dasar komputer, arsitektur sistem, jaringan, dan etika profesi IT."),
            # Sem 2
            ("IF201", "Algoritma & Struktur Data", 2, 2, 2, True, "Stack, queue, linked list, tree, graph, serta analisis kompleksitas Big-O."),
            ("IF202", "Arsitektur & Organisasi Komputer", 2, 3, 0, True, "Unit pemrosesan (CPU), memori, I/O, bahasa assembly, dan mikroarsitektur."),
            ("IF203", "Kalkulus untuk Informatika", 2, 3, 0, True, "Diferensial, integral, limit, dan aplikasi kalkulus dalam optimasi komputasi."),
            # Sem 3
            ("IF301", "Pemrograman Berorientasi Objek (OOP)", 3, 2, 2, True, "Encapsulation, inheritance, polymorphism, design patterns menggunakan Java/C++."),
            ("IF302", "Sistem Basis Data", 3, 2, 2, True, "Entity-Relationship model, normalisasi database, query SQL, dan manajemen RDBMS."),
            ("IF303", "Sistem Operasi", 3, 2, 1, True, "Manajemen proses, thread, penjadwalan CPU, memori virtual, dan sistem berkas."),
            # Sem 4
            ("IF401", "Rekayasa Perangkat Lunak (RPL)", 4, 3, 0, True, "SDLC, Scrum/Agile, analisis kebutuhan sistem, dan pemodelan UML."),
            ("IF402", "Jaringan Komputer & Komunikasi Data", 4, 2, 2, True, "Model OSI 7-layer, TCP/IP, routing, subnetting, dan konfigurasi switch."),
            ("IF403", "Kecerdasan Buatan (Artificial Intelligence)", 4, 2, 1, True, "Search algorithms, expert systems, machine learning dasar, dan representasi pengetahuan."),
            # Sem 5
            ("IF501", "Pengembangan Aplikasi Web Modern", 5, 2, 2, True, "Frontend modern, backend framework Django/Node.js, dan REST API."),
            ("IF502", "Keamanan Informasi & Jaringan", 5, 2, 1, True, "Kriptografi, penetration testing, firewall, dan mitigasi serangan cyber."),
            ("IF503", "Machine Learning & Deep Learning", 5, 2, 2, False, "Supervised & unsupervised learning, neural networks, TensorFlow, dan PyTorch."),
            # Sem 6
            ("IF601", "Cloud Computing & DevOps", 6, 2, 2, True, "Virtualisasi, Docker, Kubernetes, CI/CD pipeline, dan arsitektur AWS."),
            ("IF602", "Metodologi Riset Informatika", 6, 2, 0, True, "Penulisan karya ilmiah, perumusan masalah penelitian, dan analisis literatur."),
            ("IF603", "Pengolahan Bahasa Alami (NLP)", 6, 2, 1, False, "Tokenisasi, sentiment analysis, text classification, dan arsitektur Transformer."),
            # Sem 7
            ("IF701", "Kerja Praktik / Magang Industri MBKM", 7, 0, 8, True, "Pengalaman kerja nyata di industri mitra selama 1 semester penuh."),
            ("IF702", "Pengembangan Technopreneurship", 7, 2, 1, True, "Validasi ide bisnis teknologi, perancangan MVP, dan pitching startup."),
            # Sem 8
            ("IF801", "Tugas Akhir / Skripsi", 8, 0, 6, True, "Penyusunan karya tulis dan produk inovatif tugas akhir sarjana komputer."),
        ]
        for kode, nama, sem, teori, prak, wajib, desk in matkul_data:
            MataKuliah.objects.get_or_create(
                kode_mk=kode,
                defaults={
                    "nama_mk": nama,
                    "semester": sem,
                    "sks_teori": teori,
                    "sks_praktikum": prak,
                    "is_wajib": wajib,
                    "deskripsi": desk,
                }
            )
        self.stdout.write(self.style.SUCCESS("[OK] Mata Kuliah Kurikulum berhasil diset."))

        # 11. Kategori Berita & Berita
        kat_akademik, _ = KategoriBerita.objects.get_or_create(nama="Akademik", defaults={"slug": "akademik"})
        kat_prestasi, _ = KategoriBerita.objects.get_or_create(nama="Prestasi", defaults={"slug": "prestasi"})
        kat_event, _ = KategoriBerita.objects.get_or_create(nama="Event & Seminar", defaults={"slug": "event-seminar"})

        berita_data = [
            (
                "Mahasiswa Teknik Informatika Raih Juara 1 Gemastik Nasional 2025",
                "tim-if-juara-gemastik-2025",
                "Berita",
                kat_prestasi,
                "Tim mahasiswa Teknik Informatika berhasil menyabet medali emas pada ajang bergengsi Pagelaran Mahasiswa Nasional Bidang TIK (GEMASTIK) kategori Software Development.",
                (
                    "Prestasi membanggakan kembali diukir oleh civitas akademika Teknik Informatika. "
                    "Tim 'Algoritma Juara' yang digawangi oleh mahasiswa angkatan 2022 berhasil mengungguli puluhan universitas ternama "
                    "di seluruh Indonesia. Proyek yang dikembangkan adalah sistem pemantauan polusi udara cerdas berbasis IoT dan AI prediktif "
                    "yang langsung mendapat apresiasi tinggi dari dewan juri."
                )
            ),
            (
                "Pengumuman Jadwal Pengisian Kartu Rencana Studi (KRS) Semester Gasal 2026/2027",
                "jadwal-krs-gasal-2026-2027",
                "Pengumuman",
                kat_akademik,
                "Diumumkan kepada seluruh mahasiswa aktif perihal batas waktu konsultasi Dosen Pembimbing Akademik (DPA) dan pengisian KRS online di portal akademik.",
                (
                    "Diberitahukan kepada seluruh mahasiswa Program Studi Teknik Informatika bahwa periode pengisian KRS Semester Gasal "
                    "Tahun Akademik 2026/2027 akan dibuka mulai tanggal 1 s.d. 14 Agustus 2026. Mahasiswa diwajibkan melakukan bimbingan akademik "
                    "terlebih dahulu dengan DPA masing-masing sebelum mengunci rencana studi."
                )
            ),
            (
                "Kuliah Umum Internasional: 'The Era of Generative AI and Autonomous Software Agents'",
                "seminar-nasional-ai-2026",
                "Agenda",
                kat_event,
                "Menghadirkan pakar riset Artificial Intelligence dari Silicon Valley untuk mengupas masa depan rekayasa perangkat lunak otonom.",
                (
                    "Program studi mengundang seluruh mahasiswa dan akademisi untuk menghadiri kuliah umum bertaraf internasional "
                    "yang diselenggarakan pada hari Sabtu, 25 Juli 2026 bertempat di Auditorium Utama dan disiarkan langsung melalui YouTube."
                )
            ),
        ]
        for judul, slug, tipe, kat, ringk, isi in berita_data:
            Berita.objects.get_or_create(
                slug=slug,
                defaults={
                    "judul": judul,
                    "tipe": tipe,
                    "kategori": kat,
                    "ringkasan": ringk,
                    "konten": isi,
                    "is_published": True,
                    "views": 150,
                }
            )
        self.stdout.write(self.style.SUCCESS("[OK] Berita, Pengumuman & Agenda berhasil diset."))

        # 12. Kategori Dokumen & Dokumen
        kat_skripsi, _ = KategoriDokumen.objects.get_or_create(nama="Pedoman Tugas Akhir / Skripsi")
        kat_magang, _ = KategoriDokumen.objects.get_or_create(nama="Kerja Praktik & Magang MBKM")
        kat_akred, _ = KategoriDokumen.objects.get_or_create(nama="Dokumen & Sertifikat Akreditasi")

        # 13. FAQ
        faq_data = [
            ("Apakah program studi ini menerima lulusan SMA dari jurusan IPS atau SMK?", "Ya, kami menerima lulusan dari semua jurusan (SMA IPA/IPS/Bahasa, MA, dan SMK). Pada semester awal kami menyediakan program matrikulasi dasar komputasi dan logika pemrograman agar seluruh mahasiswa baru memiliki titik awal pemahaman yang sama.", 1),
            ("Apakah tersedia program beasiswa untuk calon mahasiswa baru?", "Tersedia berbagai pilihan beasiswa resmi, seperti Beasiswa KIP-Kuliah (Kemendikbud), Beasiswa Prestasi Akademik/Non-Akademik (potongan biaya kuliah hingga 100%), Beasiswa Tahfidz Quran, serta beasiswa dari mitra industri.", 2),
            ("Bagaimana peluang magang industri dan kesempatan kerja sebelum lulus?", "Melalui kurikulum MBKM, mahasiswa difasilitasi magang bersertifikat selama 1-2 semester di perusahaan mitra kami (GoTo, Telkom, perbankan nasional, dsb.). Lebih dari 85% lulusan kami telah mendapatkan tawaran kerja sebelum upacara wisuda.", 3),
            ("Apakah mahasiswa difasilitasi sertifikasi profesi internasional?", "Ya. Program studi kami merupakan akademi resmi dari AWS, Cisco, dan Red Hat. Mahasiswa berprestasi mendapatkan voucher ujian sertifikasi internasional secara cuma-cuma sebelum kelulusan.", 4),
        ]
        for tanya, jawab, urut in faq_data:
            FAQ.objects.get_or_create(pertanyaan=tanya, defaults={"jawaban": jawab, "urutan": urut})
        self.stdout.write(self.style.SUCCESS("[OK] FAQ Bantuan Cepat berhasil diset."))

        self.stdout.write(self.style.SUCCESS("\n[BERHASIL] PROSES SEEDING SELESAI! Seluruh modul siap digunakan."))

