#!/usr/bin/python3

import socket
import threading
import time
from queue import Queue
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# 🔥 Clear old results
open("results.txt", "w").close()

# 🔥 FULL SERVICE DATABASE (your version)
service_db = {
    20: "FTP Data", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 67: "DHCP", 68: "DHCP", 69: "TFTP", 80: "HTTP",
    110: "POP3", 119: "NNTP", 123: "NTP", 137: "NetBIOS", 138: "NetBIOS",
    139: "NetBIOS Session", 143: "IMAP", 161: "SNMP", 179: "BGP",
    389: "LDAP", 443: "HTTPS", 445: "SMB", 465: "SMTPS", 500: "ISAKMP",
    514: "Syslog", 515: "LPD", 520: "RIP", 587: "SMTP Submission",
    636: "LDAPS", 989: "FTPS", 990: "FTPS", 993: "IMAPS", 995: "POP3S",
    1433: "MSSQL", 1521: "Oracle DB", 2049: "NFS", 2082: "cPanel",
    2083: "cPanel SSL", 2181: "Zookeeper", 2222: "SSH Alt", 2375: "Docker",
    2483: "Oracle", 2484: "Oracle SSL", 3000: "Dev Server",
    3306: "MySQL", 3389: "RDP", 3690: "Subversion", 4444: "Metasploit",
    4567: "Ruby", 5000: "Flask/Dev", 5432: "PostgreSQL", 5601: "Kibana",
    5672: "RabbitMQ", 5900: "VNC", 5985: "WinRM", 5986: "WinRM SSL",
    6379: "Redis", 6667: "IRC", 7001: "WebLogic", 7002: "WebLogic SSL",
    8000: "HTTP Alt", 8008: "HTTP Proxy", 8009: "AJP", 8080: "HTTP Proxy",
    8081: "HTTP Alt", 8086: "InfluxDB", 8087: "Simplify",
    8090: "HTTP Alt", 8091: "Couchbase", 8443: "HTTPS Alt",
    8888: "Jupyter", 9000: "SonarQube", 9042: "Cassandra",
    9092: "Kafka", 9200: "Elasticsearch", 9418: "Git",
    9999: "Java Debug", 27017: "MongoDB"
}

# 🔥 UI Banner
print(Fore.CYAN + "=" * 55)
print(Fore.YELLOW + "   JATHIN ADVANCED NETWORK SCANNER")
print(Fore.CYAN + "=" * 55)

# 🔥 Input
target = input(Fore.GREEN + "Enter target IP or URL: ")

try:
    t_ip = socket.gethostbyname(target)
except:
    print(Fore.RED + "Invalid target!")
    exit()

start_port = int(input(Fore.GREEN + "Start port: "))
end_port = int(input(Fore.GREEN + "End port: "))

print(Fore.CYAN + "-" * 60)
print(Fore.YELLOW + f"Scanning {t_ip}")
print(Fore.YELLOW + f"Time: {datetime.now()}")
print(Fore.CYAN + "-" * 60)

socket.setdefaulttimeout(1)

print_lock = threading.Lock()
discovered_ports = []
q = Queue()

# 🔥 PORT SCAN FUNCTION
def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((t_ip, port))

        with print_lock:
            print(Fore.GREEN + f"[✔ OPEN] Port {port}")
            discovered_ports.append(port)

            with open("results.txt", "a") as f:
                f.write(f"Open port: {port}\n")

            banner = ""

            # 🔥 HTTP probing
            if port == 80:
                try:
                    s.send(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
                except:
                    pass

            # 🔥 Banner grabbing
            try:
                banner = s.recv(1024).decode(errors="ignore")
            except:
                banner = ""

            if banner:
                lines = banner.split("\n")
                found = False

                for line in lines:
                    clean = line.strip()
                    if "HTTP" in clean or "Server" in clean:
                        if not found:
                            print(Fore.MAGENTA + "[SERVICE]")
                            found = True
                        print(Fore.WHITE + clean)

                        with open("results.txt", "a") as f:
                            f.write(clean + "\n")

                if not found:
                    print(Fore.MAGENTA + "[SERVICE] Unknown")
            else:
                print(Fore.MAGENTA + "[SERVICE] Unknown")

            # 🔥 SERVICE DATABASE MAPPING
            if port in service_db:
                print(Fore.CYAN + f"[INFO] {service_db[port]} service detected")
            else:
                print(Fore.CYAN + "[INFO] Unknown service")

            # 🔥 SECURITY ALERT
            if port == 3306:
                print(Fore.RED + "[WARNING] Database exposed!")

        s.close()

    except:
        pass


# 🔥 THREAD WORKER
def threader():
    while True:
        worker = q.get()
        portscan(worker)
        q.task_done()


# 🔥 CREATE THREADS
for x in range(100):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()


# 🔥 ADD PORTS
for port in range(start_port, end_port + 1):
    q.put(port)

start_time = time.time()
q.join()
end_time = datetime.now()

print(Fore.CYAN + "-" * 60)
print(Fore.YELLOW + f"Completed in: {end_time - datetime.fromtimestamp(start_time)}")
print(Fore.CYAN + "-" * 60)

# 🔥 NMAP SUGGESTION
if discovered_ports:
    ports = ",".join(map(str, discovered_ports))
    print(Fore.GREEN + "Suggested Nmap command:")
    print(Fore.WHITE + f"nmap -p{ports} -sV -sC -T4 -Pn {target}")
else:
    print(Fore.RED + "No open ports found.")
