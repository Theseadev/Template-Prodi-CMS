from .models import IdentitasProdi

def identitas_prodi_context(request):
    """
    Menyediakan objek identitas program studi ke seluruh template secara otomatis.
    Jika belum ada data di database, kembalikan instance default agar website tetap tampil sempurna.
    """
    identitas = IdentitasProdi.objects.first()
    if not identitas:
        identitas = IdentitasProdi(
            nama_prodi="Teknik Informatika",
            fakultas="Fakultas Ilmu Komputer",
            universitas="Universitas Teknologi Nusantara",
            jenjang="S1",
            gelar_kelulusan="S.Kom.",
            akreditasi="Unggul",
            tagline="Membentuk Talenta Unggul Masa Depan Berbasis Teknologi & Inovasi",
            visi="Menjadi program studi rujukan nasional yang unggul dalam rekayasa perangkat lunak dan kecerdasan buatan bereputasi global pada tahun 2030.",
            misi="1. Menyelenggarakan pendidikan berkualitas tinggi di bidang teknologi informasi.\n2. Mengembangkan penelitian inovatif berstandar internasional.\n3. Melaksanakan pengabdian kepada masyarakat berbasis solusi digital.",
            alamat_kampus="Gedung Rektorat Lt. 3, Jl. Pendidikan No. 1, Kampus Utama",
            email_resmi="informatika@kampus.ac.id",
            telepon="(021) 7654321",
            whatsapp_layanan="6281234567890",
            url_pmb="https://pmb.kampus.ac.id",
        )
    if identitas:
        identitas.foto_kaprodi_fallback = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=800&auto=format&fit=crop"
    return {
        "prodi": identitas
    }
