# ⚔️ USM KRS WARRIOR (SIMA Automation)

**Ultimate KRS War Bot for Universitas Semarang (USM)**

Script otomasi berbasis Python untuk membantu mahasiswa USM mendapatkan mata kuliah incaran di sistem **SIMA** secara cepat, tepat, dan otomatis. Dirancang dengan tampilan _Clean Mode_ (anti-spam terminal) dan dilengkapi fitur keamanan jadwal.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Stable-green?style=for-the-badge)
![IG](https://img.shields.io/badge/Creator-@rffdzky-purple?style=for-the-badge&logo=instagram)

---

## 🔥 Fitur Utama (v.Final)

- **🛡️ Safety First:** Dilengkapi peringatan dini (Safety Alert) untuk menampilkan total target dan memastikan user sudah mengecek jadwal sebelum eksekusi.
- **👀 Clean Mode UI:** Tampilan terminal yang rapi. Status scanning hanya satu baris yang diperbarui otomatis (tidak _scrolling_ ke bawah), kecuali saat berhasil mengambil mata kuliah.
- **🔐 Smart Login Validation:** Memastikan Username/Password benar dengan membaca respon server SIMA (bukan hanya cek cookie).
- **⚡ Priority System:** Mendukung prioritas kelas.
  - _Contoh:_ Cari kelas **A1** dulu. Jika penuh, otomatis cari kelas **A**.
- **📊 Total Matkul Counter:** Menghitung jumlah mata kuliah yang akan diburu secara otomatis.
- **📝 Format Validator:** Mendeteksi kesalahan penulisan di `target.txt` (misal: kurang koma) agar bot tidak _crash_.

---

## 🛠️ Persiapan (Installation)

Pastikan komputer Anda sudah terinstall **Python 3**.

1.  **Clone / Download Repository ini**
2.  **Install Library Pendukung**
    Buka terminal/CMD di folder bot, lalu ketik:
    ```bash
    pip install requests beautifulsoup4 urllib3
    ```

---

## ⚙️ Cara Pakai

### 1. Edit File `target.txt`

Buat file bernama `target.txt`. Masukkan daftar mata kuliah dengan format:
`NAMA_MATKUL, KELAS_PRIORITAS_1, KELAS_PRIORITAS_2`

**⚠️ PENTING:** Jangan lupa tanda **KOMA (,)** pemisah antar nama dan kelas!

**Contoh Isi `target.txt`:**

```text
PENGGALIAN DATA, A1
TRANSFORMASI DIGITAL, A1, A
MANAJEMEN RISIKO TI, B1
ETIKA PROFESI, A, A1
```

(Artinya: Untuk Transformasi Digital, bot cari kelas A1 dulu. Kalau penuh, cari kelas A).

2. Atur Akun (Di dalam Script)
   Buka file krswar.py, cari bagian paling atas dan isi NIM & Password SIMA kamu:
   MY_NIM = "G.111.xx.xxxx"
   MY_PASSWORD = "PasswordSimaKamu"

3. Jalankan Bot
   Buka terminal dan ketik:
   python krswar.py

📸 Preview Tampilan

1. Peringatan Awal (Safety Check):
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   ⚠️ PERINGATAN SEBELUM PERANG ⚠️
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   TOTAL TARGET: 4 MATA KULIAH

---

1. Pastikan JADWAL target.txt tidak bentrok satu sama lain.
2. Pastikan JADWAL tidak bentrok dengan matkul yg sudah diambil.
3. Pastikan SISA SKS CUKUP (Max 24).

---

👉 Tekan [ENTER] jika sudah yakin & ingin melanjutkan...

2. Mode Monitoring (Scanning):
   [Scan: 154] 🔒 Pending: 4 | ⏳ Load: 0.22s | ⚡
   Baris ini akan terus berkedip di tempat yang sama, tidak memenuhi layar)

3. Saat Berhasil (Success):

   > > > 🚀 MENEMBAK: MANAJEMEN RISIKO TI [KELAS B1] <<<
   > > > ✅ [SUKSES] MANAJEMEN RISIKO TI BERHASIL DIAMBIL!

❓ FAQ (Troubleshooting)
Masalah,Penyebab & Solusi
Login Ditolak,Password atau NIM salah. Cek konfigurasi di script.
[SKIP] Baris Salah Format,"Anda lupa menaruh tanda koma (,) di file target.txt."
❌ [GAGAL] Server: SKS,Jatah SKS habis (Max 24). Bot tidak menghapus matkul lama. Hapus manual di web SIMA.
❌ [GAGAL] Server: Bentrok,Jadwal matkul incaran bertabrakan dengan matkul yang sudah diambil.
