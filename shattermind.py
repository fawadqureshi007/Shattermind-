#!/usr/bin/env python3
import requests
import socket
import os
import sys
import subprocess
import re
from urllib.parse import urlparse

# ================= COLOR =================
G="\033[92m"
R="\033[91m"
Y="\033[93m"
B="\033[94m"
C="\033[96m"
W="\033[0m"

class ShatterMind:

    def __init__(self):
        self.target = None

    # ================= UI =================
    def banner(self):
        os.system("clear")
        print(f"""{C}
███████╗██╗  ██╗ █████╗ ████████╗████████╗███████╗
SHATTERMIND FULL FRAMEWORK (PY EDITION)
{W}
Type 'help'
""")

    def help(self):
        print(f"""
{C}COMMANDS:{W}

set <url>        Set target
info             Basic scan (title, ip, server, cms, robots)
whois            WHOIS lookup
geoip            Geo IP lookup
dns              DNS lookup
headers          HTTP headers
subnet           Subnet calculator
nmap             Port scan (requires nmap)
subdomains       Subdomain scanner
reverseip        Reverse IP lookup
sqli             Basic SQL injection test
wordpress        WP scanner
crawl            Simple crawler
exit
""")

    # ================= UTIL =================
    def normalize(self, url):
        if not url.startswith("http"):
            url = "http://" + url
        return url

    def domain(self):
        return urlparse(self.normalize(self.target)).netloc

    # ================= BASIC INFO =================
    def info(self):
        url = self.normalize(self.target)
        dom = self.domain()

        print(Y+"\n[ BASIC INFO ]"+W)

        try:
            r = requests.get(url, timeout=6)
            text = r.text

            title = re.search("<title>(.*?)</title>", text, re.I)
            if title:
                print(G+"Title: "+title.group(1)+W)

            print(G+"IP: "+socket.gethostbyname(dom)+W)

            headers = r.headers
            print(G+"Server: "+headers.get("Server","Unknown")+W)

            if "wp-content" in text:
                print(G+"CMS: WordPress"+W)
            elif "joomla" in text:
                print(G+"CMS: Joomla"+W)
            else:
                print(R+"CMS: Unknown"+W)

            if "robots.txt" in text:
                print(G+"robots.txt detected"+W)

        except Exception as e:
            print(R+"Error: "+str(e)+W)

    # ================= WHOIS =================
    def whois(self):
        dom=self.domain()
        r=requests.get(f"https://api.hackertarget.com/whois/?q={dom}")
        print(r.text)

    # ================= GEOIP =================
    def geoip(self):
        dom=self.domain()
        r=requests.get(f"https://api.hackertarget.com/geoip/?q={dom}")
        print(r.text)

    # ================= DNS =================
    def dns(self):
        dom=self.domain()
        r=requests.get(f"https://api.hackertarget.com/dnslookup/?q={dom}")
        print(r.text)

    # ================= HEADERS =================
    def headers(self):
        r=requests.get(self.normalize(self.target))
        for k,v in r.headers.items():
            print(k+":",v)

    # ================= SUBNET =================
    def subnet(self):
        ip = socket.gethostbyname(self.domain())
        print("[+] IP:",ip)

        base=".".join(ip.split(".")[:3])
        print("[+] /24 range:")

        for i in range(1,20):
            print(base+"."+str(i))

    # ================= NMAP =================
    def nmap(self):
        dom=self.domain()
        ip=socket.gethostbyname(dom)
        print("[+] Scanning:",ip)
        os.system(f"nmap -F {ip}")

    # ================= SUBDOMAINS =================
    def subdomains(self):
        dom=self.domain()
        words=["www","mail","ftp","api","dev","test","admin","blog","ns1","ns2"]

        for w in words:
            host=f"{w}.{dom}"
            try:
                socket.gethostbyname(host)
                print("[FOUND]",host)
            except:
                pass

    # ================= REVERSE IP =================
    def reverseip(self):
        dom=self.domain()
        r=requests.get(f"https://api.hackertarget.com/reverseiplookup/?q={dom}")
        print(r.text)

    # ================= SQLI CHECK =================
    def sqli(self):
        url=self.normalize(self.target)+"'"
        try:
            r=requests.get(url)
            errors=["sql","mysql","syntax","warning","error"]
            if any(e in r.text.lower() for e in errors):
                print(R+"[!] Possible SQL Injection"+W)
            else:
                print(G+"[-] No obvious SQLi detected"+W)
        except:
            print(R+"Request failed"+W)

    # ================= WORDPRESS =================
    def wordpress(self):
        url=self.normalize(self.target)
        r=requests.get(url).text

        if "wp-content" in r:
            print(G+"WordPress detected"+W)

            checks=["/wp-login.php","/xmlrpc.php","/wp-json"]
            for c in checks:
                rr=requests.get(url+c)
                print(c, rr.status_code)
        else:
            print(R+"Not WordPress"+W)

    # ================= CRAWLER =================
    def crawl(self):
        url=self.normalize(self.target)
        links=set()

        r=requests.get(url)
        found=re.findall('href=["\'](.*?)["\']',r.text)

        for f in found:
            if self.domain() in f or f.startswith("/"):
                links.add(f)

        print("[+] Links found:")
        for l in list(links)[:30]:
            print(l)

    # ================= RUN =================
    def run(self):
        self.banner()

        while True:
            cmd=input("shattermind> ")

            if cmd.startswith("set "):
                self.target=cmd.split(" ",1)[1]
                print("[+] Target set")

            elif cmd=="info":
                self.info()

            elif cmd=="whois":
                self.whois()

            elif cmd=="geoip":
                self.geoip()

            elif cmd=="dns":
                self.dns()

            elif cmd=="headers":
                self.headers()

            elif cmd=="subnet":
                self.subnet()

            elif cmd=="nmap":
                self.nmap()

            elif cmd=="subdomains":
                self.subdomains()

            elif cmd=="reverseip":
                self.reverseip()

            elif cmd=="sqli":
                self.sqli()

            elif cmd=="wordpress":
                self.wordpress()

            elif cmd=="crawl":
                self.crawl()

            elif cmd=="exit":
                sys.exit()

            else:
                print("unknown command")


if __name__=="__main__":
    ShatterMind().run()
