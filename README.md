# ⚔️ USM KRS WARRIOR (SIMA Automation)

**Automasi KRS SIMA -- Universitas Semarang (USM)**

Script berbasis Python untuk membantu mahasiswa Universitas Semarang
mendapatkan mata kuliah incaran secara cepat, tepat, dan otomatis
melalui sistem SIMA.

Dirancang dengan tampilan **Clean Mode** (tanpa spam terminal), validasi
login cerdas, dan sistem prioritas kelas.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Stable-green?style=for-the-badge)
![Creator](https://img.shields.io/badge/Creator-rffdzky-purple?style=for-the-badge&logo=github)

---

## 🚀 Fitur Utama

- 🛡️ **Safety Alert System**\
  Menampilkan total target dan peringatan sebelum eksekusi untuk
  memastikan jadwal sudah dicek.

- 👀 **Clean Mode UI**\
  Status monitoring hanya satu baris dinamis (tidak memenuhi layar).

- 🔐 **Smart Login Validation**\
  Validasi login berdasarkan respons server SIMA, bukan hanya
  pengecekan cookie.

- ⚡ **Priority Class System**\
  Mendukung pencarian kelas berdasarkan prioritas.\
  Contoh: Cari kelas **A1** terlebih dahulu. Jika penuh, otomatis cari
  kelas **A**.

- 📊 **Auto Target Counter**\
  Menghitung total mata kuliah yang diburu secara otomatis.

- 📝 **Format Validator**\
  Mendeteksi kesalahan format di `target.txt` agar bot tidak crash.

---

## 🛠️ Instalasi

Pastikan sudah terinstall **Python 3.8 atau lebih baru**.

### 1️⃣ Clone / Download Repository

Download atau clone repository ini ke komputer Anda.

### 2️⃣ Install Dependencies

Buka terminal/CMD di folder project, lalu jalankan:

```bash
pip install curl-cffi beautifulsoup4
```

---

## ⚙️ Cara Penggunaan

### 1️⃣ Buat File `target.txt`

Buat file bernama `target.txt`, lalu isi dengan format berikut:

    NAMA_MATKUL, KELAS_PRIORITAS_1, KELAS_PRIORITAS_2

⚠️ Gunakan tanda koma (,) sebagai pemisah.

### Contoh `target.txt`

```text
PENGGALIAN DATA, A1
TRANSFORMASI DIGITAL, A1, A
MANAJEMEN RISIKO TI, B1
ETIKA PROFESI, A, A1
```

Penjelasan: - Untuk Transformasi Digital, bot akan mencari kelas **A1**
terlebih dahulu. - Jika penuh, bot otomatis mencari kelas **A**.

---

### 2️⃣ Konfigurasi Akun

Buka file `krswar.py`, lalu edit bagian berikut di atas script:

```python
MY_NIM = "G.111.xx.xxxx"
MY_PASSWORD = "PasswordSimaKamu"
```

Isi sesuai akun SIMA Anda.

---

### 3️⃣ Jalankan Bot

Di terminal:

```bash
python krswar.py
```

---

## 📸 Preview Tampilan

### 🛡️ Safety Check

    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ⚠️ PERINGATAN SEBELUM EKSEKUSI ⚠️
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    TOTAL TARGET: 4 MATA KULIAH

    1. Pastikan JADWAL target.txt tidak ada matkul/ruangan salah ketik
    2. Pastikan SISA SKS CUKUP (Max 24).
    3. Bot ini akan mengeksekusi OTOMATIS begitu kuota tersedia.

    👉 Tekan [ENTER] untuk melanjutkan...

---

### 🔎 Mode Monitoring

    [Scan: 154] 🔒 Pending: 4 | ⏳ Load: 0.22s | ⚡

Status akan terus diperbarui di baris yang sama tanpa membuat terminal
penuh.

---

### 🚀 Saat Berhasil

    >>> 🚀 MENEMBAK: MANAJEMEN RISIKO TI [KELAS B1] <<<
    >>> ✅ [SUKSES] MANAJEMEN RISIKO TI BERHASIL DIAMBIL!

---

## ❓ Troubleshooting

---

Masalah Penyebab Solusi

---

Login Ditolak NIM atau Password salah Periksa konfigurasi di
`krswar.py`

\[SKIP\] Baris Salah Format `target.txt` Pastikan ada tanda
Format tidak sesuai koma (,)

❌ \[GAGAL\] Server: SKS SKS sudah mencapai batas Hapus mata kuliah lama
(maks 24) secara manual di SIMA

❌ \[GAGAL\] Server: Jadwal bertabrakan Periksa ulang jadwal
Bentrok sebelum menjalankan
bot

---

---

## ⚠️ Disclaimer

Gunakan dengan bijak dan bertanggung jawab.\
Segala risiko penggunaan menjadi tanggung jawab pengguna.

---

## 👨‍💻 Creator

**rffdzky**
