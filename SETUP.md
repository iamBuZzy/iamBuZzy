# Cara Memasang GitHub Profile Scan

Paket ini adalah **README profil GitHub dengan banner GIF animasi asli**. Desainnya mengambil tema terminal/hacker, warna neon cyan, dua panel, dan efek garis pemindai. GIF dapat tampil pada GitHub tanpa JavaScript atau layanan gambar pihak ketiga.

## 1. Siapkan repo khusus profil

Misalnya username GitHub kamu `namaku`, buat repository **Public** bernama `namaku` (nama repository harus sama persis dengan username GitHub). Pilih Add README jika membuat lewat web, lalu ganti dengan README yang ada di paket ini.

## 2. Upload file berikut dengan struktur yang sama

```text
namaku/
├── README.md
└── assets/
    ├── profile-scan.gif          <- gambar utama yang bergerak
    ├── profile-scan.png          <- gambar diam / fallback
    └── profile-scan-source.png   <- ilustrasi asli kualitas penuh
```

File `tools/make_animation.py` dan `SETUP.md` boleh ikut diupload atau disimpan sebagai sumber lokal. Mereka tidak diperlukan untuk menampilkan animasi.

## 3. Sesuaikan tautan dan identitas

Buka README.md dan cari lalu ganti:

- `YOUR_USERNAME` → username GitHub milikmu (tanpa @)
- `YOUR_EMAIL@example.com` → email publik yang ingin dipakai
- Nama, perkenalan, stack, dan proyek → sesuai profilmu

**Penting:** nama dan detail di **gambar animasi** merupakan bagian dari ilustrasi sumber, bukan teks dari README. Jika mau mengganti tulisan di dalam banner (misalnya username, nama, stack, atau lokasi), ubah `assets/profile-scan-source.png` menggunakan editor gambar, lalu jalankan ulang skrip generator. Atau buat ulang base art sesuai identitasmu.

## 4. Animasi dan aksesibilitas

- File utama: `assets/profile-scan.gif` (loop otomatis, sekitar 3 detik).
- Gambar statis: `assets/profile-scan.png`.
- Untuk pengguna yang memilih tanpa animasi, edit di README: `profile-scan.gif` menjadi `profile-scan.png`.
- README GitHub tidak menjalankan JavaScript. GIF digunakan agar efek animasi konsisten di GitHub.

## 5. (Opsional) Regenerasi animasi

Instal Pillow:

```bash
python -m pip install pillow
```

Dari direktori utama paket ini, jalankan:

```bash
python tools/make_animation.py
```

Generator akan membuat ulang GIF dan PNG dari `assets/profile-scan-source.png`. Gunakan file sumber yang telah diubah jika identitas di banner perlu diperbarui.

## 6. Publikasikan

Commit file ke branch default (biasanya `main`), lalu buka `https://github.com/USERNAME_KAMU`. README akan terlihat di halaman profil. Bila GIF tidak terlihat, cek lagi bahwa nama file serta folder `assets` sama persis dengan path di README.

---

*Catatan:* Tautan contoh harus disesuaikan terlebih dahulu. Deskripsi proyek merupakan ringkasan; tambahkan tautan repository publik bila tersedia.
