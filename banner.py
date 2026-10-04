#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import time
from datetime import datetime
import pyfiglet

# কালার কোড (ANSI Escape Codes)
C = '\033[1;36m' # Cyan
G = '\033[1;32m' # Green
Y = '\033[1;33m' # Yellow
M = '\033[1;35m' # Magenta
W = '\033[1;37m' # White
R = '\033[1;31m' # Red
NC = '\033[0m'   # No Color

CONFIG_FILE = os.path.expanduser("~/.mybanner_config.json")

def run_cmd(cmd):
    """Termux কমান্ড রান করে আউটপুট রিটার্ন করার হেল্পার ফাংশন"""
    try:
        result = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
        return result if result else "Unknown"
    except subprocess.CalledProcessError:
        return "Unknown"

def setup_banner():
    """ইউজারের কাছ থেকে কাস্টম ইনফরমেশন নেওয়ার ফাংশন"""
    os.system('clear')
    print(f"{C}========================================={NC}")
    print(f"{Y}     ⚙️  BANNER SETUP WIZARD  ⚙️{NC}")
    print(f"{C}========================================={NC}")
    
    user_name = input(f"{W}Enter Your Name: {NC}")
    team_name = input(f"{W}Enter Team Name: {NC}")
    custom_msg = input(f"{W}Enter Custom Message: {NC}")
    
    config_data = {
        "user_name": user_name,
        "team_name": team_name,
        "custom_msg": custom_msg
    }
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_data, f, indent=4)
        
    print(f"\n{G}[✔] Setup Saved Successfully!{NC}")
    time.sleep(1.5)

def display_banner():
    """সব ডেটা কালেক্ট করে সুন্দর করে ব্যানার ডিসপ্লে করার ফাংশন"""
    # কনফিগারেশন লোড করা
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"{R}[!] No configuration found. Starting setup...{NC}")
        time.sleep(1)
        setup_banner()
        return display_banner()

    os.system('clear')
    
    # ১. হেডার সেকশন (নাম এবং টিম)
    print(f"{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
    
    # PyFiglet দিয়ে নাম ডিজাইন করা
    ascii_art = pyfiglet.figlet_format(config['user_name'], font="slant")
    print(f"{C}{ascii_art}{NC}")
    
    print(f"{M}             [ Team: {config['team_name']} ]{NC}")
    print(f"{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{NC}")
    
    # ২. কাস্টম স্ট্যাটাস
    print(f"{Y}[!] Status   : {W}{config['custom_msg']}{NC}")
    print(f"{C}───────────────────────────────────────────────────{NC}")

    # ৩. তারিখ ও সময়
    now = datetime.now()
    time_str = now.strftime("%I:%M:%S %p")
    date_str = now.strftime("%A, %d %B %Y")
    
    print(f"{G}[*] Time     : {W}{time_str}{NC}")
    print(f"{G}[*] Date     : {W}{date_str}{NC}")

    # ৪. ডিভাইস ইনফরমেশন (Termux getprop কমান্ডের মাধ্যমে)
    model = run_cmd("getprop ro.product.model")
    android_ver = run_cmd("getprop ro.build.version.release")
    uptime = run_cmd("uptime -p | sed 's/up //'")
    
    print(f"{G}[*] Device   : {W}{model}{NC}")
    print(f"{G}[*] Android  : {W}Android {android_ver}{NC}")
    print(f"{G}[*] Uptime   : {W}{uptime}{NC}")

    # ৫. নেটওয়ার্ক এবং স্টোরেজ
    local_ip = run_cmd("ifconfig wlan0 2>/dev/null | grep 'inet ' | awk '{print $2}'")
    if not local_ip or local_ip == "Unknown":
        local_ip = "Disconnected"
        
    df_output = run_cmd("df -h /data | tail -n 1").split()
    storage = f"{df_output[3]} Free / {df_output[1]} Total" if len(df_output) >= 4 else "Unknown"

    print(f"{G}[*] Local IP : {W}{local_ip}{NC}")
    print(f"{G}[*] Storage  : {W}{storage}{NC}")
    print(f"{C}───────────────────────────────────────────────────{NC}")

    # ৬. লোডিং অ্যানিমেশন
    print(f"{C}[*] System Booting... {NC}", end="", flush=True)
    for _ in range(4):
        print(f"{G}█{NC}", end="", flush=True)
        time.sleep(0.2)
    print(f"\n\n{G}[✔] Welcome back, {config['user_name']}!{NC}\n")

if __name__ == "__main__":
    # যদি ইউজার --setup বা -s দেয়, তবে সেটআপ রান হবে
    if len(sys.argv) > 1 and sys.argv[1] in ['-s', '--setup']:
        setup_banner()
        
    display_banner()