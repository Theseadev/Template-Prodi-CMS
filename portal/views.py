from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F, Q
from django.http import Http404
from .models import (
    IdentitasProdi, ProfilLulusan, ProgramUnggulan, Fasilitas,
    Dosen, TestimoniAlumni, MitraKerjasama, Prestasi,
    MataKuliah, KategoriBerita, Berita, KategoriDokumen, DokumenAkademik, FAQ,
    HeroSlider
)


# Metadata Penunjang Visual Akademik & Fallback Foto
DOSEN_PHOTO_FALLBACKS = {
    "Dr. Eng. Ir. Hendra Gunawan, S.Kom., M.T.": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=600&auto=format&fit=crop",
    "Prof. Dr. Ir. Sri Wahyuni, M.Sc., Ph.D.": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=600&auto=format&fit=crop",
    "Ahmad Fauzi, S.Kom., M.Kom., Ph.D.": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=600&auto=format&fit=crop",
    "Dewi Sartika, S.Kom., M.T., Ph.D.": "https://images.unsplash.com/photo-1580489944761-15a19d654956?q=80&w=600&auto=format&fit=crop",
    "Bambang Kurniawan, S.T., M.Kom.": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?q=80&w=600&auto=format&fit=crop",
    "Rian Hidayat, S.Kom., M.Cs.": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?q=80&w=600&auto=format&fit=crop",
}

PIMPINAN_META_MAP = {
    "Dr. Eng. Ir. Hendra Gunawan, S.Kom., M.T.": {
        "foto": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=600&auto=format&fit=crop",
        "urutan": 1,
        "fokus": "Software Architecture, Cloud Computing & Distributed Systems"
    },
    "Ahmad Fauzi, S.Kom., M.Kom., Ph.D.": {
        "foto": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=600&auto=format&fit=crop",
        "urutan": 2,
        "fokus": "Cyber Security, Applied Cryptography & Information Assurance"
    },
    "Prof. Dr. Ir. Sri Wahyuni, M.Sc., Ph.D.": {
        "foto": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=600&auto=format&fit=crop",
        "urutan": 3,
        "fokus": "Artificial Intelligence, Deep Learning & Natural Language Processing"
    },
    "Dewi Sartika, S.Kom., M.T., Ph.D.": {
        "foto": "https://images.unsplash.com/photo-1580489944761-15a19d654956?q=80&w=600&auto=format&fit=crop",
        "urutan": 4,
        "fokus": "Advanced Software Engineering, HCI & Quality Assurance"
    }
}


def _get_pimpinan_list():
    """Mengambil dan menyusun pimpinan struktural prodi secara konsisten."""
    pimpinan_dosen = Dosen.objects.filter(is_active=True).exclude(jabatan_struktural="").order_by("id")
    pimpinan_list = []
    for d in pimpinan_dosen:
        pmeta = PIMPINAN_META_MAP.get(d.nama_lengkap, {
            "foto": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?q=80&w=600&auto=format&fit=crop",
            "urutan": 99,
            "fokus": d.bidang_keahlian
        })
        pimpinan_list.append({
            "obj": d,
            "nama": d.nama_lengkap,
            "jabatan_struktural": d.jabatan_struktural,
            "jabatan_fungsional": d.jabatan_fungsional,
            "nidn": d.nidn,
            "foto": d.foto.url if d.foto else pmeta["foto"],
            "fokus": pmeta["fokus"],
            "urutan": pmeta["urutan"]
        })
    pimpinan_list.sort(key=lambda x: x["urutan"])
    return pimpinan_list


def home(request):
    """
    Halaman Utama (Beranda) - Showcasing Hero Slider kampus, berita & agenda, visi, profil lulusan, dosen.
    """
    hero_slides = HeroSlider.objects.filter(is_active=True).order_by("urutan")
    profil_lulusan = ProfilLulusan.objects.all()[:6]
    program_unggulan = ProgramUnggulan.objects.all()[:4]
    fasilitas = Fasilitas.objects.all()[:6]
    dosen_list = Dosen.objects.filter(is_active=True)[:6]
    testimoni_list = TestimoniAlumni.objects.filter(is_featured=True)[:4]
    mitra_list = MitraKerjasama.objects.all()[:12]
    prestasi_list = Prestasi.objects.all()[:4]
    berita_terbaru = Berita.objects.filter(is_published=True, tipe="Berita")[:4]
    pengumuman_terbaru = Berita.objects.filter(is_published=True, tipe="Pengumuman")[:2]
    agenda_terbaru = Berita.objects.filter(is_published=True, tipe="Agenda").order_by("tanggal_agenda", "-tanggal_publikasi")[:3]
    faq_list = FAQ.objects.all()[:6]

    # Statistik cepat
    stats = {
        "total_dosen": Dosen.objects.filter(is_active=True).count() or 18,
        "total_matakuliah": MataKuliah.objects.count() or 54,
        "total_mitra": MitraKerjasama.objects.count() or 25,
        "total_prestasi": Prestasi.objects.count() or 42,
    }

    context = {
        "hero_slides": hero_slides,
        "profil_lulusan": profil_lulusan,
        "program_unggulan": program_unggulan,
        "fasilitas": fasilitas,
        "dosen_list": dosen_list,
        "testimoni_list": testimoni_list,
        "mitra_list": mitra_list,
        "prestasi_list": prestasi_list,
        "berita_terbaru": berita_terbaru,
        "pengumuman_terbaru": pengumuman_terbaru,
        "agenda_terbaru": agenda_terbaru,
        "faq_list": faq_list,
        "stats": stats,
    }
    return render(request, "portal/home.html", context)


def profil(request):
    """
    Halaman Profil Lengkap: Visi Misi, Sambutan Kaprodi, Pimpinan Prodi, Fasilitas Lab, dan Legalitas.
    """
    fasilitas_queryset = Fasilitas.objects.all()
    
    # Metadata penunjang visual fasilitas
    lab_meta_map = {
        "Laboratorium Kecerdasan Buatan & Data": {
            "foto": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=800&auto=format&fit=crop",
            "tag": "Komputasi Performa Tinggi (HPC)",
            "kapasitas": "40 Stasiun Kerja",
            "spesifikasi": ["GPU Cluster NVIDIA RTX", "Dual-Monitor Ultra-Wide Setup", "PyTorch & TensorFlow Suite", "Apache Spark Distributed Node"],
            "badge_color": "bg-purple-50 text-purple-700 border-purple-200"
        },
        "Laboratorium Rekayasa Perangkat Lunak & Cloud": {
            "foto": "https://images.unsplash.com/photo-1531482615713-2afd69097998?q=80&w=800&auto=format&fit=crop",
            "tag": "Enterprise Architecture & DevOps",
            "kapasitas": "45 Stasiun Kerja",
            "spesifikasi": ["Private Kubernetes Cluster", "Automated CI/CD Testbed", "Enterprise Cloud Suite", "Scrum Collaborative Workpod"],
            "badge_color": "bg-blue-50 text-blue-700 border-blue-200"
        },
        "Studio Multimedia, AR/VR & Game Dev": {
            "foto": "https://images.unsplash.com/photo-1593508512255-86ab42a8e620?q=80&w=800&auto=format&fit=crop",
            "tag": "Immersive Media & 3D Interactive",
            "kapasitas": "35 Stasiun Kerja",
            "spesifikasi": ["Meta Quest VR Headsets", "Wacom Cintiq Pen Displays", "Unreal Engine 5 & Unity Suite", "High-Resolution Render Farm"],
            "badge_color": "bg-rose-50 text-rose-700 border-rose-200"
        },
        "Laboratorium Jaringan & Keamanan Siber": {
            "foto": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=800&auto=format&fit=crop",
            "tag": "Network Simulation & Cyber Defense",
            "kapasitas": "40 Stasiun Kerja",
            "spesifikasi": ["Cisco Catalyst Enterprise Switches", "Isolated Penetration Testing Sandbox", "Hardware Next-Gen Firewall", "Packet Inspection Rig"],
            "badge_color": "bg-emerald-50 text-emerald-700 border-emerald-200"
        }
    }
    
    fasilitas_list = []
    for f in fasilitas_queryset:
        meta = lab_meta_map.get(f.nama_fasilitas, {
            "foto": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=800&auto=format&fit=crop",
            "tag": "Laboratorium Komputasi",
            "kapasitas": "35 Stasiun Kerja",
            "spesifikasi": ["Workstation Terintegrasi", "Akses Internet Gigabit", "Software Berlisensi Resmi"],
            "badge_color": "bg-slate-100 text-slate-700 border-slate-200"
        })
        fasilitas_list.append({
            "obj": f,
            "nama": f.nama_fasilitas,
            "deskripsi": f.deskripsi,
            "gambar": f.gambar.url if f.gambar else meta["foto"],
            "tag": meta["tag"],
            "kapasitas": meta["kapasitas"],
            "spesifikasi": meta["spesifikasi"],
            "badge_color": meta["badge_color"],
        })

    # Pimpinan Program Studi
    pimpinan_list = _get_pimpinan_list()

    # Tonggak Sejarah / Milestones Perjalanan Prodi
    milestones = [
        {
            "tahun": "2012",
            "judul": "Pendirian Program Studi",
            "deskripsi": "Resmi beroperasi berdasarkan Surat Keputusan Kemendikbudristek untuk merespons percepatan era komputasi modern dan kebutuhan talenta digital nasional.",
            "badge": "Fondasi Awal",
            "pencapaian": "Penerimaan angkatan pertama mahasiswa sarjana komputer."
        },
        {
            "tahun": "2016",
            "judul": "Akreditasi B & Ekspansi Laboratorium",
            "deskripsi": "Meraih Akreditasi B BAN-PT serta meresmikan perluasan fasilitas laboratorium riset komputasi dan rekayasa perangkat lunak.",
            "badge": "Infrastruktur",
            "pencapaian": "100% lulusan pertama terserap industri dalam kurun waktu kurang dari 4 bulan."
        },
        {
            "tahun": "2020",
            "judul": "Kurikulum OBE & Akselerasi MBKM",
            "deskripsi": "Mengadopsi kerangka kurikulum Outcome-Based Education (OBE) dan mengintegrasikan program magang industri bersertifikat di perusahaan teknologi terkemuka.",
            "badge": "Kurikulum OBE",
            "pencapaian": "Kemitraan strategis kurikulum komputasi awan bersama AWS & Google Cloud."
        },
        {
            "tahun": "2023",
            "judul": "Akreditasi UNGGUL LAM-INFOKOM",
            "deskripsi": "Mencapai peringkat akreditasi tertinggi nasional dari Lembaga Akreditasi Mandiri Informatika dan Komputer dengan evaluasi mutu akademik istimewa.",
            "badge": "Predikat Tertinggi",
            "pencapaian": "Standarisasi laboratorium dan peningkatan rasio publikasi riset terindeks internasional."
        },
        {
            "tahun": "2025 & Menuju 2030",
            "judul": "Akselerasi Riset AI & Kemitraan Global",
            "deskripsi": "Fokus pada ekspansi riset frontier Artificial Intelligence, pertukaran mahasiswa internasional, dan hilirisasi paten inovasi digital berkelanjutan.",
            "badge": "Visi Masa Depan",
            "pencapaian": "Pusat rujukan keunggulan komputasi terapan dan technopreneurship bereputasi global."
        }
    ]

    # 4 Pilar Misi Tridharma
    misi_pillars = [
        {
            "nomor": "01",
            "judul": "Pendidikan Sarjana Berstandar Global",
            "sub": "Pilar Pendidikan & Pengajaran",
            "deskripsi": "Menyelenggarakan proses pembelajaran komputasi mutakhir berbasis Outcome-Based Education (OBE) dan MBKM untuk melahirkan sarjana yang adaptif, inovatif, dan beretika luhur.",
            "icon": "academic"
        },
        {
            "nomor": "02",
            "judul": "Riset Transformatif & Publikasi Bereputasi",
            "sub": "Pilar Penelitian & Pengembangan",
            "deskripsi": "Mengembangkan penelitian frontier dalam domain kecerdasan buatan, rekayasa perangkat lunak, dan keamanan siber yang terpublikasi di jurnal ilmiah bereputasi tinggi.",
            "icon": "research"
        },
        {
            "nomor": "03",
            "judul": "Pengabdian Berbasis Solusi Digital",
            "sub": "Pilar Pengabdian Masyarakat",
            "deskripsi": "Menerapkan inovasi teknologi dan hilirisasi produk perangkat lunak untuk memecahkan persoalan nyata pada sektor publik, UMKM, dan masyarakat secara berkelanjutan.",
            "icon": "hand"
        },
        {
            "nomor": "04",
            "judul": "Kemitraan Industri & Jejaring Internasional",
            "sub": "Pilar Sinergi & Kerjasama",
            "deskripsi": "Membangun kolaborasi aktif bersama industri teknologi global, ekosistem startup terkemuka, dan universitas mitra luar negeri guna akselerasi karir lulusan.",
            "icon": "globe"
        }
    ]

    # Seluruh Dosen untuk tab Dosen & Pengajar
    dosen_all = []
    for d in Dosen.objects.filter(is_active=True):
        d.foto_display = d.foto.url if d.foto else DOSEN_PHOTO_FALLBACKS.get(d.nama_lengkap, "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=600&auto=format&fit=crop")
        dosen_all.append(d)

    context = {
        "fasilitas_list": fasilitas_list,
        "pimpinan_list": pimpinan_list,
        "dosen_all": dosen_all,
        "milestones": milestones,
        "misi_pillars": misi_pillars,
        "total_dosen": len(dosen_all),
        "total_lab": fasilitas_queryset.count(),
    }
    return render(request, "portal/profil.html", context)


def dosen_list(request):
    """
    Direktori Lengkap Dosen & Tenaga Pengajar dengan Filter Pencarian dan visual fallback profesional.
    """
    query = request.GET.get("q", "").strip()
    jabatan = request.GET.get("jabatan", "").strip()

    dosen = Dosen.objects.filter(is_active=True)
    if query:
        dosen = dosen.filter(
            Q(nama_lengkap__icontains=query) |
            Q(bidang_keahlian__icontains=query) |
            Q(nidn__icontains=query)
        )
    if jabatan:
        dosen = dosen.filter(jabatan_fungsional=jabatan)

    dosen_items = []
    for d in dosen:
        d.foto_display = d.foto.url if d.foto else DOSEN_PHOTO_FALLBACKS.get(d.nama_lengkap, "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=600&auto=format&fit=crop")
        dosen_items.append(d)

    pimpinan_list = _get_pimpinan_list()

    context = {
        "dosen_list": dosen_items,
        "pimpinan_list": pimpinan_list,
        "query": query,
        "selected_jabatan": jabatan,
        "jabatan_choices": Dosen.JABATAN_CHOICES,
        "total_dosen": len(dosen_items),
    }
    return render(request, "portal/dosen.html", context)


def kurikulum(request):
    """
    Struktur Kurikulum Per Semester (1 s.d. 8) dan Silabus/RPS.
    """
    # Mengelompokkan mata kuliah per semester
    matakuliah_per_semester = {}
    for sem in range(1, 9):
        matakuliah_per_semester[sem] = MataKuliah.objects.filter(semester=sem)

    total_sks_wajib = sum(mk.total_sks for mk in MataKuliah.objects.filter(is_wajib=True))
    total_sks_pilihan = sum(mk.total_sks for mk in MataKuliah.objects.filter(is_wajib=False))

    context = {
        "matakuliah_per_semester": matakuliah_per_semester,
        "semesters": range(1, 9),
        "total_sks_wajib": total_sks_wajib,
        "total_sks_pilihan": total_sks_pilihan,
        "total_sks_semua": total_sks_wajib + total_sks_pilihan,
    }
    return render(request, "portal/kurikulum.html", context)


def berita_list(request):
    """
    Daftar Berita, Pengumuman, dan Agenda Kegiatan.
    """
    tipe = request.GET.get("tipe", "")
    kategori_slug = request.GET.get("kategori", "")
    query = request.GET.get("q", "").strip()

    berita = Berita.objects.filter(is_published=True)

    if tipe in ["Berita", "Pengumuman", "Agenda"]:
        berita = berita.filter(tipe=tipe)

    if kategori_slug:
        berita = berita.filter(kategori__slug=kategori_slug)

    if query:
        berita = berita.filter(
            Q(judul__icontains=query) | Q(ringkasan__icontains=query) | Q(konten__icontains=query)
        )

    kategori_list = KategoriBerita.objects.all()

    context = {
        "berita_list": berita,
        "kategori_list": kategori_list,
        "current_tipe": tipe,
        "current_kategori": kategori_slug,
        "query": query,
    }
    return render(request, "portal/berita_list.html", context)


def berita_detail(request, slug):
    """
    Detail Konten Berita / Pengumuman / Agenda.
    """
    artikel = get_object_or_404(Berita, slug=slug, is_published=True)
    
    # Increment view counter
    Berita.objects.filter(pk=artikel.pk).update(views=F("views") + 1)
    artikel.refresh_from_db()

    berita_terkait = Berita.objects.filter(is_published=True).exclude(pk=artikel.pk)[:3]

    context = {
        "artikel": artikel,
        "berita_terkait": berita_terkait,
    }
    return render(request, "portal/berita_detail.html", context)


def dokumen_list(request):
    """
    Pusat Unduhan Dokumen Akademik.
    """
    kategori_list = KategoriDokumen.objects.prefetch_related("dokumenakademik_set").all()
    context = {
        "kategori_list": kategori_list,
    }
    return render(request, "portal/dokumen.html", context)


def unduh_dokumen(request, pk):
    """
    Download handler untuk menghitung jumlah unduhan file secara akurat.
    """
    dokumen = get_object_or_404(DokumenAkademik, pk=pk)
    DokumenAkademik.objects.filter(pk=pk).update(download_count=F("download_count") + 1)
    if dokumen.file_dokumen:
        return redirect(dokumen.file_dokumen.url)
    raise Http404("Berkas fisik tidak ditemukan.")


def kontak(request):
    """
    Halaman Kontak Resmi & Layanan Mahasiswa.
    """
    faq_list = FAQ.objects.all()
    context = {
        "faq_list": faq_list,
    }
    return render(request, "portal/kontak.html", context)


def kemahasiswaan(request):
    """
    Halaman Kemahasiswaan: Prestasi Civitas, Organisasi Mahasiswa (HMTI), dan Jejak Alumni.
    """
    tingkat = request.GET.get("tingkat", "").strip()
    prestasi = Prestasi.objects.all().order_by("-tahun")
    if tingkat:
        prestasi = prestasi.filter(tingkat__iexact=tingkat)

    testimoni = TestimoniAlumni.objects.all()

    context = {
        "prestasi_list": prestasi,
        "selected_tingkat": tingkat,
        "tingkat_choices": ["Internasional", "Nasional", "Provinsi", "Universitas"],
        "testimoni_list": testimoni,
    }
    return render(request, "portal/kemahasiswaan.html", context)


def kerjasama(request):
    """
    Halaman Kerja Sama & Kemitraan Industri: Direktori Mitra Industri, Program MBKM, dan Kolaborasi Riset.
    """
    mitra = MitraKerjasama.objects.all().order_by("nama_mitra")
    context = {
        "mitra_list": mitra,
    }
    return render(request, "portal/kerjasama.html", context)

