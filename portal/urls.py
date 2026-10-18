from django.urls import path
from . import views

app_name = "portal"

urlpatterns = [
    path("", views.home, name="home"),
    path("profil/", views.profil, name="profil"),
    path("dosen/", views.dosen_list, name="dosen_list"),
    path("kurikulum/", views.kurikulum, name="kurikulum"),
    path("berita/", views.berita_list, name="berita_list"),
    path("berita/<slug:slug>/", views.berita_detail, name="berita_detail"),
    path("dokumen/", views.dokumen_list, name="dokumen_list"),
    path("dokumen/<int:pk>/unduh/", views.unduh_dokumen, name="unduh_dokumen"),
    path("kemahasiswaan/", views.kemahasiswaan, name="kemahasiswaan"),
    path("kerjasama/", views.kerjasama, name="kerjasama"),
    path("kontak/", views.kontak, name="kontak"),
]
