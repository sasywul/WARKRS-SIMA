import requests
import time
import urllib3
import sys
import re
import os
from bs4 import BeautifulSoup

# Mengabaikan peringatan SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================
# ⚙️ KONFIGURASI USER
# ==========================================
MY_NIM      = "G.xxx.xx.xxx"
MY_PASSWORD = "xxxxx"
FILE_TARGET = "target.txt"

HEADERS_BROWSER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://sima.usm.ac.id/"
}

def load_targets_from_txt(filename):
    if not os.path.exists(filename):
        print(f"[ERROR] File '{filename}' tidak ditemukan.")
        sys.exit()

    targets = []
    print(f"[INFO] Membaca target dari '{filename}'...")
    
    with open(filename, "r") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"): continue
            
            if "," not in line:
                print(f"    [SKIP] Baris {i} salah format: '{line}'")
                continue

            parts = [p.strip().upper() for p in line.split(",")]
            if len(parts) >= 2:
                targets.append({"nama": parts[0], "kelas": parts[1:], "status": "PENDING"})
                # Format: PENGGALIAN DATA [A1, A2]
                kelas_str = ", ".join(parts[1:])
                print(f"    + Incaran: {parts[0]} [{kelas_str}]")
                
    if not targets:
        print("[ERROR] Target kosong.")
        sys.exit()
    return targets

def get_session_valid(nim, password):
    print(f"[LOGIN] Menghubungi Server USM ({nim})...")
    session = requests.Session()
    session.headers.update(HEADERS_BROWSER)
    
    try:
        r_home = session.get("https://sima.usm.ac.id/", timeout=15, verify=False)
        match = re.search(r'name=["\']token["\'][^>]*value=["\']([^"\']+)["\']', r_home.text)
        
        if not match: return None, "Gagal koneksi (Token hilang)."
        token_val = match.group(1)
        
        payload = {"username": nim, "token": token_val, "password": password}
        
        res_login = session.post("https://sima.usm.ac.id/login", data=payload, timeout=20, verify=False)

        url_akhir = res_login.url  
        #print(f"   [DEBUG] Mendarat di: {url_akhir}") 

        if "/app" in url_akhir:
            session.post("https://sima.usm.ac.id/app/routes", data={
                "id_aplikasi": "05494017904153", 
                "level_key": "6f1e80f8-4fb3-11ea-9ef2-1cb72c27dd68", 
                "id_bidang": "1"
            }, verify=False)
            
            print("[LOGIN] ✅ BERHASIL! (Redirect ke APP terkonfirmasi)")
            return session, None
            
        else:
            # Jika TIDAK ke /app (misal malah ke halaman depan lagi), berarti GAGAL.
            # Kita coba baca pesan errornya sekalian biar tau kenapa.
            soup = BeautifulSoup(res_login.text, 'html.parser')
            alert = soup.find('div', class_=re.compile(r'alert'))
            msg = alert.get_text(strip=True) if alert else "Password/User Salah (Tidak masuk ke /app)"
            
            return None, f"LOGIN GAGAL: {msg}"

    except Exception as e: return None, f"Error Koneksi: {e}"

def eksekusi_tembak(session, url, payload, headers, nama, kelas):
    print(f"\n\n>>> 🚀 MENEMBAK: {nama} [KELAS {kelas}] <<<")
    try:
        res = session.post(url, data=payload, headers=headers, verify=False)
        
        if "berhasil" in res.text.lower() or "sukses" in res.text.lower():
            print(f"   ✅ [SUKSES] {nama} BERHASIL DIAMBIL!")
            return True
        else:
            soup = BeautifulSoup(res.text, 'html.parser')
            alert = soup.find('div', class_=re.compile(r'alert'))
            msg = alert.get_text(strip=True) if alert else "Unknown Error"
            print(f"   ❌ [GAGAL] Server: {msg}")
            return False
    except: return False

def war_engine_start():
    print("="*60)
    print("   SIMA WAR - IG @rffdzky (RAPID FIRE MODE)")
    print("="*60)
    
    # 1. LOAD TARGET
    daftar_target = load_targets_from_txt(FILE_TARGET)
    total_target = len(daftar_target)
    
    # 2. WARNING ALERT
    print("\n" + "!"*60)
    print("⚠️  PERINGATAN MODE RAPID FIRE  ⚠️")
    print("!"*60)
    print(f"   TOTAL TARGET: {total_target} MATA KULIAH")
    print("-" * 60)
    print("1. Bot akan menembak SEMUA slot yang terbuka SEKALIGUS.")
    print("2. Pastikan SISA SKS CUKUP untuk mengambil banyak matkul.")
    print("3. Risiko bentrok jadwal ditanggung penumpang.")
    print("-" * 60)
    
    try:
        input("👉 Tekan [ENTER] jika sudah yakin & ingin melanjutkan...")
    except KeyboardInterrupt: sys.exit()

    # 3. LOGIN
    print("-" * 60)
    session, error_msg = get_session_valid(MY_NIM, MY_PASSWORD)
    if error_msg:
        print(f"[FATAL] {error_msg}")
        return 

    url_input = "https://sima.usm.ac.id/akademik/krs/input_krs_reguler"
    url_simpan = "https://sima.usm.ac.id/akademik/krs/input_krs_reguler/simpan_krs_reguler"

    print(f"\n[INFO] Monitoring dimulai... 🔥")
    print("-" * 60)
    
    attempt = 1
    while True:
        try:
            # Ambil hanya target yang belum SUKSES
            sisa_target = [t for t in daftar_target if t['status'] == 'PENDING']
            total_pending = len(sisa_target)
            
            if total_pending == 0:
                print("\n\n🎉 SEMUA TARGET SELESAI DIPROSES.")
                break

            t_start = time.time()
            try:
                resp = session.get(url_input, timeout=10, verify=False)
            except:
                sys.stdout.write(f"\r⚠️  Koneksi Timeout... Retrying.")
                sys.stdout.flush()
                time.sleep(1); continue
            
            t_load = round(time.time() - t_start, 2)
            soup = BeautifulSoup(resp.text, 'html.parser')
            cards = soup.find_all('div', class_='card')
            
            hits_in_this_round = 0 # Menghitung berapa kali nembak di ronde ini

            # --- LOOPING PENGECEKAN (TANPA BREAK UTAMA) ---
            for target in sisa_target:
                match_cards = [c for c in cards if target['nama'] in c.get_text().upper()]

                if not match_cards: continue 

                # Cek prioritas kelas
                for p_kelas in target['kelas']:
                    # Flag agar tidak nembak 2 kelas untuk 1 matkul yg sama
                    sudah_ditembak = False 
                    
                    p_reg = rf"KELAS\s+{re.escape(p_kelas)}(?!\w)"
                    for c in match_cards:
                        if re.search(p_reg, c.get_text().upper()):
                            form = c.find('form')
                            btn = c.find('button')
                            
                            # Skip jika tombol disabled
                            if not form or (btn and 'disabled' in btn.attrs):
                                continue

                            s_kuota = c.find('span', class_='text-success')
                            kuota = int(s_kuota.get_text(strip=True)) if s_kuota else 0

                            if kuota > 0:
                                # KETEMU SLOT! SIAPKAN PELURU
                                payload = {i.get('name'): i.get('value') for i in form.find_all('input', type='hidden')}
                                h_post = session.headers.copy()
                                h_post["Content-Type"] = "application/x-www-form-urlencoded"
                                h_post["Referer"] = url_input
                                
                                # DOR! TEMBAK LANGSUNG
                                if eksekusi_tembak(session, url_simpan, payload, h_post, target['nama'], p_kelas):
                                    target['status'] = 'SUKSES'
                                else:
                                    target['status'] = 'GAGAL_TEMP'
                                
                                hits_in_this_round += 1
                                sudah_ditembak = True
                                break # Break loop kartu (lanjut ke target matkul berikutnya)
                    
                    if sudah_ditembak:
                        break # Break loop prioritas kelas (lanjut ke target matkul berikutnya)
            
            # --- STATUS BAR ---
            # Jika ada tembakan, kasih enter biar log terbaca
            prefix = "\n" if hits_in_this_round > 0 else "\r"
            
            status_bar = (
                f"{prefix}[Scan: {attempt}] "
                f"🔒 Pending: {total_pending} "
                f"| ⏳ Load: {t_load}s "
                f"| {'✨' if attempt % 2 == 0 else '⚡'}"
            )
            
            sys.stdout.write(status_bar)
            sys.stdout.flush()

            attempt += 1
            time.sleep(0.5)

        except KeyboardInterrupt:
            print("\n\n[STOP] Program dihentikan user."); break
        except Exception as e:
            print(f"\n[ERROR] {e}")
            time.sleep(1)

if __name__ == "__main__":
    war_engine_start()