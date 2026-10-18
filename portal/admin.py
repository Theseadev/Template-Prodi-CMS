from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    IdentitasProdi, ProfilLulusan, ProgramUnggulan, Fasilitas,
    Dosen, TestimoniAlumni, MitraKerjasama, Prestasi,
    MataKuliah, KategoriBerita, Berita, KategoriDokumen, DokumenAkademik, FAQ,
    HeroSlider
)


@admin.register(HeroSlider)
class HeroSliderAdmin(ModelAdmin):
    list_display = ("judul", "subjudul", "urutan", "is_active")
    list_editable = ("urutan", "is_active")
    search_fields = ("judul", "subjudul", "deskripsi")



@admin.register(IdentitasProdi)
class IdentitasProdiAdmin(ModelAdmin):
    list_display = ("nama_prodi", "jenjang", "fakultas", "universitas", "akreditasi", "email_resmi")
    fieldsets = (
        ("Identitas Dasar & Akreditasi", {
            "fields": (
                ("nama_prodi", "jenjang", "gelar_kelulusan"),
                ("fakultas", "universitas"),
                ("akreditasi", "lembaga_akreditasi", "nomor_sk_akreditasi"),
                "tagline",
            )
        }),
        ("Visi, Misi & Tujuan", {
            "fields": ("visi", "misi", "tujuan")
        }),
        ("Pimpinan & Sambutan Kaprodi", {
            "fields": (
                ("nama_kaprodi", "foto_kaprodi"),
                "sambutan_kaprodi",
            )
        }),
        ("Branding Visual", {
            "fields": (
                ("logo", "favicon"),
                "warna_tema_hex",
            )
        }),
        ("Kontak & Lokasi Kampus", {
            "fields": (
                "alamat_kampus",
                ("email_resmi", "telepon", "whatsapp_layanan"),
            )
        }),
        ("Link Aksi Utama (PMB & Tracer Study)", {
            "fields": (
                ("url_pmb", "url_tracer_study"),
            )
        }),
        ("Media Sosial", {
            "fields": (
                ("instagram_url", "youtube_url", "linkedin_url"),
            )
        }),
    )

    def has_add_permission(self, request):
        # Hanya boleh 1 record identitas prodi
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(ProfilLulusan)
class ProfilLulusanAdmin(ModelAdmin):
    list_display = ("nama_profesi", "ikon", "urutan")
    list_editable = ("urutan",)
    search_fields = ("nama_profesi", "deskripsi")


@admin.register(ProgramUnggulan)
class ProgramUnggulanAdmin(ModelAdmin):
    list_display = ("judul", "badge", "ikon", "urutan")
    list_editable = ("urutan", "badge")
    search_fields = ("judul", "deskripsi")


@admin.register(Fasilitas)
class FasilitasAdmin(ModelAdmin):
    list_display = ("nama_fasilitas", "urutan")
    list_editable = ("urutan",)
    search_fields = ("nama_fasilitas", "deskripsi")


@admin.register(Dosen)
class DosenAdmin(ModelAdmin):
    list_display = ("nama_lengkap", "jabatan_fungsional", "jabatan_struktural", "bidang_keahlian", "is_active", "urutan")
    list_filter = ("jabatan_fungsional", "is_active")
    list_editable = ("is_active", "urutan")
    search_fields = ("nama_lengkap", "nidn", "nip", "bidang_keahlian")
    fieldsets = (
        ("Biodata Pengajar", {
            "fields": (
                "nama_lengkap",
                ("nidn", "nip"),
                ("jabatan_fungsional", "jabatan_struktural"),
                "bidang_keahlian",
                ("foto", "email"),
                "is_active",
                "urutan",
            )
        }),
        ("Tautan Akademik & Repositori Ilmiah", {
            "fields": (
                ("url_sinta", "url_scholar"),
                ("url_scopus", "url_linkedin"),
            )
        }),
    )


@admin.register(TestimoniAlumni)
class TestimoniAlumniAdmin(ModelAdmin):
    list_display = ("nama_alumni", "profesi_sekarang", "nama_kantor", "tahun_lulus", "is_featured", "urutan")
    list_filter = ("tahun_lulus", "is_featured")
    list_editable = ("is_featured", "urutan")
    search_fields = ("nama_alumni", "profesi_sekarang", "nama_kantor", "isi_testimoni")


@admin.register(MitraKerjasama)
class MitraKerjasamaAdmin(ModelAdmin):
    list_display = ("nama_mitra", "kategori", "website_mitra", "urutan")
    list_filter = ("kategori",)
    list_editable = ("urutan",)
    search_fields = ("nama_mitra",)


@admin.register(Prestasi)
class PrestasiAdmin(ModelAdmin):
    list_display = ("judul_prestasi", "kategori", "tingkat", "peraih", "tahun")
    list_filter = ("kategori", "tingkat", "tahun")
    search_fields = ("judul_prestasi", "peraih", "deskripsi")


@admin.register(MataKuliah)
class MataKuliahAdmin(ModelAdmin):
    list_display = ("kode_mk", "nama_mk", "semester", "sks_teori", "sks_praktikum", "total_sks", "is_wajib")
    list_filter = ("semester", "is_wajib")
    search_fields = ("kode_mk", "nama_mk")
    list_editable = ("is_wajib",)


@admin.register(KategoriBerita)
class KategoriBeritaAdmin(ModelAdmin):
    list_display = ("nama", "slug")
    prepopulated_fields = {"slug": ("nama",)}


@admin.register(Berita)
class BeritaAdmin(ModelAdmin):
    list_display = ("judul", "tipe", "kategori", "tanggal_publikasi", "is_published", "views")
    list_filter = ("tipe", "kategori", "is_published", "tanggal_publikasi")
    list_editable = ("is_published",)
    search_fields = ("judul", "ringkasan", "konten")
    prepopulated_fields = {"slug": ("judul",)}
    fieldsets = (
        ("Informasi Utama", {
            "fields": (
                "judul",
                "slug",
                ("tipe", "kategori"),
                "gambar_sampul",
                "ringkasan",
                "konten",
            )
        }),
        ("Khusus Agenda / Acara", {
            "fields": (
                ("tanggal_agenda", "lokasi_agenda"),
            )
        }),
        ("Status Publikasi", {
            "fields": (
                "is_published",
            )
        }),
    )


@admin.register(KategoriDokumen)
class KategoriDokumenAdmin(ModelAdmin):
    list_display = ("nama",)


@admin.register(DokumenAkademik)
class DokumenAkademikAdmin(ModelAdmin):
    list_display = ("nama_dokumen", "kategori", "tanggal_unggah", "download_count")
    list_filter = ("kategori",)
    search_fields = ("nama_dokumen", "deskripsi")


@admin.register(FAQ)
class FAQAdmin(ModelAdmin):
    list_display = ("pertanyaan", "urutan")
    list_editable = ("urutan",)
    search_fields = ("pertanyaan", "jawaban")
