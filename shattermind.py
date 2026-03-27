#!/usr/bin/env python3

import requests
import socket
import dns.resolver
import whois
import re
import subprocess
import threading
import time
import os
from bs4 import BeautifulSoup
from colorama import Fore, init

init(autoreset=True)

# =========================
# 🎨 BANNER
# =========================
def banner():
    print(Fore.CYAN + r"""
███████╗██╗  ██╗ █████╗ ████████╗████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗██████╗ 
██╔════╝██║  ██║██╔══██╗╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗
███████╗███████║███████║   ██║      ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║██║  ██║
╚════██║██╔══██║██╔══██║   ██║      ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██║  ██║
███████║██║  ██║██║  ██║   ██║      ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██████╔╝
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝ 

        🔥 SHATTERMIND - Next Generation Recon Framework 🔥
        🧠 OSINT | RECON | VULN INTELLIGENCE | AUTOMATION
    """)

    print(Fore.YELLOW + "Version: 2.0 | Mode: Recon Framework\n")
    print(Fore.GREEN + "Developed by: Fawad Qureshi")
    print(Fore.MAGENTA + "Instagram: @h4cker_fawad\n")


# =========================
# 📁 SAVE SYSTEM
# =========================
def save_file(folder, filename, data):
    os.makedirs(folder, exist_ok=True)
    with open(f"{folder}/{filename}", "a") as f:
        f.write(data + "\n")


# =========================
# ⏳ LOADING
# =========================
def loading(text):
    print(Fore.YELLOW + f"[~] {text}", end="")
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="")
    print("\n")


# =========================
# 🌐 WEBSITE INFO
# =========================
def website_info(target):
    loading("Fetching website info")

    try:
        r = requests.get(target, timeout=5)
        title = re.findall("<title>(.*?)</title>", r.text)

        print(Fore.GREEN + f"[+] Title: {title[0] if title else 'N/A'}")
        print(Fore.GREEN + f"[+] Server: {r.headers.get('Server')}")

        save_file("results", "info.txt", f"{target} | {title}")

    except:
        print(Fore.RED + "[-] Error fetching site")

    try:
        ip = socket.gethostbyname(target.replace("http://","").replace("https://",""))
        print(Fore.GREEN + f"[+] IP: {ip}")
        save_file("results", "ips.txt", ip)
    except:
        pass


# =========================
# ☁️ CLOUDFLARE
# =========================
def cloudflare_detect(target):
    loading("Checking Cloudflare")

    try:
        r = requests.get(target)
        if "cloudflare" in str(r.headers).lower():
            print(Fore.GREEN + "[+] Cloudflare Detected")
        else:
            print(Fore.RED + "[-] No Cloudflare")
    except:
        pass


# =========================
# 🔎 SUBDOMAIN ENUM
# =========================
subs_found = []

def check_sub(domain, sub):
    try:
        full = f"{sub}.{domain}"
        socket.gethostbyname(full)
        print(Fore.GREEN + f"[+] {full}")
        subs_found.append(full)
    except:
        pass


def subdomain_enum(domain):
    loading("Running Subdomain Enumeration")

    subs = ["www","mail","dev","test","api","admin","vpn","ftp"]

    threads = []

    for sub in subs:
        t = threading.Thread(target=check_sub, args=(domain, sub))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    for s in subs_found:
        save_file("results", "subdomains.txt", s)


# =========================
# 🧠 WHOIS + DNS
# =========================
def whois_lookup(domain):
    loading("WHOIS lookup")

    try:
        info = whois.whois(domain)
        print(Fore.GREEN + f"[+] Org: {info.org}")
    except:
        pass


def dns_info(domain):
    loading("DNS lookup")

    try:
        result = dns.resolver.resolve(domain, 'A')
        for ip in result:
            print(Fore.GREEN + f"[+] DNS: {ip}")
            save_file("results", "dns.txt", str(ip))
    except:
        pass


# =========================
# 🛡 NMAP
# =========================
def nmap_scan(domain):
    loading("Running Nmap Scan")
    subprocess.call(["nmap", "-F", domain])


# =========================
# 📡 CRAWLER
# =========================
def crawler(target):
    loading("Crawling website")

    try:
        r = requests.get(target)
        soup = BeautifulSoup(r.text, "html.parser")

        for a in soup.find_all("a"):
            link = a.get("href")
            if link:
                print(Fore.GREEN + link)
                save_file("results", "urls.txt", link)

    except:
        pass


# =========================
# 🧩 CMS DETECTION
# =========================
def cms_detect(target):
    loading("Detecting CMS")

    try:
        r = requests.get(target).text.lower()

        if "wp-content" in r:
            print(Fore.GREEN + "[+] WordPress")
        elif "joomla" in r:
            print(Fore.GREEN + "[+] Joomla")
        elif "drupal" in r:
            print(Fore.GREEN + "[+] Drupal")
        else:
            print(Fore.RED + "[-] Unknown CMS")
    except:
        pass


# =========================
# 🌍 IP INTELLIGENCE (NEW)
# =========================
def ip_intelligence(domain):
    loading("IP Intelligence")

    try:
        ip = socket.gethostbyname(domain)
        print(Fore.CYAN + f"[+] IP: {ip}")

        r = requests.get(f"http://ip-api.com/json/{ip}").json()

        print(Fore.GREEN + "\n[IP INTEL]")
        print("[+] Country:", r.get("country"))
        print("[+] City:", r.get("city"))
        print("[+] ISP:", r.get("isp"))
        print("[+] Org:", r.get("org"))
        print("[+] ASN:", r.get("as"))
    except:
        pass


# =========================
# 🔐 HEADERS ANALYSIS (NEW)
# =========================
def headers_analysis(target):
    loading("Security Headers")

    try:
        r = requests.get(target)
        h = r.headers

        print(Fore.MAGENTA + "\n[HEADERS]")

        headers = [
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Frame-Options",
            "X-XSS-Protection",
            "X-Content-Type-Options"
        ]

        for head in headers:
            print(f"[+] {head}: {h.get(head, 'MISSING')}")
    except:
        pass


# =========================
# 🔎 PARAMETER FINDER (NEW)
# =========================
def parameter_finder(target):
    loading("Finding Parameters")

    try:
        r = requests.get(target)
        params = re.findall(r"\?(\w+)=", r.text)

        print(Fore.GREEN + "\n[PARAMETERS]")

        if params:
            for p in set(params):
                print("[+] ?", p)
        else:
            print("[-] None found")
    except:
        pass


# =========================
# 📜 JS EXTRACTOR (NEW)
# =========================
def js_extractor(target):
    loading("Extracting JS files")

    try:
        r = requests.get(target)
        soup = BeautifulSoup(r.text, "html.parser")

        for script in soup.find_all("script"):
            src = script.get("src")
            if src and ".js" in src:
                print(Fore.GREEN + "[+] " + src)
                save_file("results", "js.txt", src)
    except:
        pass


# =========================
# 📋 MENU
# =========================
def menu():
    print(Fore.CYAN + """
[1] Website Info
[2] Cloudflare Detection
[3] DNS Lookup
[4] WHOIS Lookup
[5] Subdomain Enumeration
[6] Nmap Scan
[7] Web Crawler
[8] CMS Detection
[9] Full Recon
[10] IP Intelligence
[11] Security Headers
[12] Parameter Finder
[13] JS Extractor
[14] Exit
    """)


# =========================
# 🚀 MAIN
# =========================
def main():
    banner()

    target = input(Fore.YELLOW + "Enter Target (https://example.com): ")
    domain = target.replace("http://","").replace("https://","")

    while True:
        menu()
        choice = input(Fore.YELLOW + "Select >> ")

        if choice == "1":
            website_info(target)

        elif choice == "2":
            cloudflare_detect(target)

        elif choice == "3":
            dns_info(domain)

        elif choice == "4":
            whois_lookup(domain)

        elif choice == "5":
            subdomain_enum(domain)

        elif choice == "6":
            nmap_scan(domain)

        elif choice == "7":
            crawler(target)

        elif choice == "8":
            cms_detect(target)

        elif choice == "9":
            print(Fore.YELLOW + "[*] Running Full Recon...\n")
            website_info(target)
            cloudflare_detect(target)
            dns_info(domain)
            whois_lookup(domain)
            subdomain_enum(domain)
            cms_detect(target)
            ip_intelligence(domain)
            headers_analysis(target)
            parameter_finder(target)
            js_extractor(target)
            nmap_scan(domain)
            crawler(target)

        elif choice == "10":
            ip_intelligence(domain)

        elif choice == "11":
            headers_analysis(target)

        elif choice == "12":
            parameter_finder(target)

        elif choice == "13":
            js_extractor(target)

        elif choice == "14":
            print(Fore.RED + "Exiting SHATTERMIND...")
            break

        else:
            print(Fore.RED + "Invalid option")


if __name__ == "__main__":
    main()
