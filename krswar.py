from curl_cffi import requests
import time
import sys
import re
import os
import random
from bs4 import BeautifulSoup

# ==========================================
# ⚙️ KONFIGURASI USER
# ==========================================
MY_NIM      = "G.111.24.0021"
MY_PASSWORD = "xxxx"
FILE_TARGET = "target.txt"


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

def get_smart_headers():

    ua = random.choice(USER_AGENTS)
    
    platform = '"Windows"' if "Windows" in ua else ('"macOS"' if "Macintosh" in ua else '"Linux"')
    
    headers = {
        "Host": "sima.usm.ac.id",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Referer": "https://sima.usm.ac.id/",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
        
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": platform,
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
    }
    return headers



def load_targets_from_txt(filename):
    if not os.path.exists(filename):
        print(f"[ERROR] File '{filename}' tidak ditemukan.")
        sys.exit()
    targets = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "," not in line: continue
            parts = [p.strip().upper() for p in line.split(",")]
            if len(parts) >= 2:
                targets.append({"nama": parts[0], "kelas": parts[1:], "status": "PENDING"})
                print(f"    + Incaran: {parts[0]} [{', '.join(parts[1:])}]")
    if not targets: sys.exit("[ERROR] Target kosong.")
    return targets

def is_cloudflare(resp):
    server_header = resp.headers.get('Server', '').lower()
    status_check = resp.status_code in [403, 429, 503]
    has_cf_html = any(kw in resp.text for kw in ['cf-turnstile', 'challenges.cloudflare.com', 'ray ID:'])
    return server_header == 'cloudflare' or has_cf_html

def get_session_valid(nim, password):
    print(f"[LOGIN] Menghubungi Server USM ({nim})...")
    session = requests.Session(impersonate="chrome120")
    session.headers = get_smart_headers()
    
    try:
        r_home = session.get("https://sima.usm.ac.id/", timeout=15)
        
        # --- CEK CLOUDFLARE DI SINI ---
        if is_cloudflare(r_home):
            print("[ALERT] Terdeteksi Cloudflare! Mencoba menembus dengan curl_cffi...")
        
        soup = BeautifulSoup(r_home.text, 'html.parser')
        el_token = soup.find('input', {'name': 'token'})
        
        if not el_token:
            if "Just a moment" in r_home.text:
                return None, "Stuck di Cloudflare Challenge (Butuh Browser asli)."
            return None, "Token CSRF hilang (Block IP?)"
            
        token_val = el_token.get('value')
        payload = {"username": nim, "token": token_val, "password": password}
        
        res_login = session.post("https://sima.usm.ac.id/login", data=payload, timeout=20)

        if "/app" in res_login.url:
            # Bypass route aplikasi USM
            session.post("https://sima.usm.ac.id/app/routes", data={
                "id_aplikasi": "05494017904153", 
                "level_key": "6f1e80f8-4fb3-11ea-9ef2-1cb72c27dd68", 
                "id_bidang": "1"
            })
            print("[LOGIN] ✅ BERHASIL")
            return session, None
        else:
            return None, "Login Gagal (Password salah / Redirect gagal)"

    except Exception as e: 
        return None, f"Error: {e}"

def eksekusi_tembak(session, url, payload, nama):
    try:
        res = session.post(url, data=payload)
        if "berhasil" in res.text.lower() or "sukses" in res.text.lower():
            print(f"   ✅ [SUKSES] {nama} BERHASIL DIAMBIL!")
            return True
        else:
            print(f"   ❌ [GAGAL] {nama}: Penuh/Gagal.")
            return False
    except: return False

def war_engine_start():
    print("="*60)
    print("   SIMA WAR - HYBRID MODE (Anti-Detect Headers)")
    print("="*60)
    
    daftar_target = load_targets_from_txt(FILE_TARGET)
    session, error_msg = get_session_valid(MY_NIM, MY_PASSWORD)
    
    if error_msg:
        print(f"[FATAL] {error_msg}")
        return 

    url_input = "https://sima.usm.ac.id/akademik/krs/input_krs_reguler"
    url_simpan = "https://sima.usm.ac.id/akademik/krs/input_krs_reguler/simpan_krs_reguler"

    print(f"\n[INFO] Monitoring dimulai... 🔥")
    attempt = 1
    
    while True:
        try:
            sisa_target = [t for t in daftar_target if t['status'] == 'PENDING']
            if not sisa_target: break

            t_start = time.time()
            resp = session.get(url_input, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            cards = soup.find_all('div', class_='card')
            
            hits = 0
            for target in sisa_target:
                match_cards = [c for c in cards if target['nama'] in c.get_text().upper()]
                if not match_cards: continue 

                for p_kelas in target['kelas']:
                    p_reg = rf"KELAS\s+{re.escape(p_kelas)}(?!\w)"
                    for c in match_cards:
                        if re.search(p_reg, c.get_text().upper()):
                            form = c.find('form')
                            btn = c.find('button')
                            
                            # Cek kuota & tombol
                            s_kuota = c.find('span', class_='text-success')
                            kuota = int(s_kuota.get_text(strip=True)) if s_kuota else 0
                            
                            if form and (not btn or 'disabled' not in btn.attrs) and kuota > 0:
                                payload = {i.get('name'): i.get('value') for i in form.find_all('input', type='hidden')}
                                if eksekusi_tembak(session, url_simpan, payload, target['nama']):
                                    target['status'] = 'SUKSES'
                                hits += 1
                                break
                    if target['status'] == 'SUKSES': break
            
            # Print Status
            sys.stdout.write(f"\r[Scan: {attempt}] Pending: {len(sisa_target)} | Load: {round(time.time()-t_start, 2)}s  ")
            sys.stdout.flush()
            attempt += 1
            time.sleep(1)

        except KeyboardInterrupt: break
        except Exception: time.sleep(1)

if __name__ == "__main__":
    war_engine_start()