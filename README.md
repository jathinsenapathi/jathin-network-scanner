# 🔐 Multi-Threaded Network Scanner

A Python-based tool that performs fast port scanning using multi-threading and identifies potentially risky exposed services.

---

## 🚀 Features

* Multi-threaded port scanning
* Detects open ports
* Basic service detection (HTTP, SSH, MySQL)
* Security warning for exposed databases
* Saves results to file

---

## ⚙️ Requirements

* Python 3.x

---

## ▶️ How to Run

1. Clone the repository:

```bash
git clone https://github.com/jathinsenapathi/jathin-network-scanner.git
cd jathin-network-scanner
```

2. Run the scanner:

```bash
python3 threader3000.py
```

3. Enter target:

```
127.0.0.1
```

---

## 📌 Example Output

```
[✔ OPEN] Port 80
[INFO] Web server detected

[✔ OPEN] Port 3306
[INFO] MySQL database detected
[WARNING] Database exposed! Potential security risk
```

---

## ⚠️ Disclaimer

This tool is intended for educational purposes and authorized security testing only.
