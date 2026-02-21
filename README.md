# TCP/IP Sender & Receiver 🧰

Small pair of Python scripts that send random 8-character codes over TCP/IP and log them to CSV. The sender repeatedly emits codes; the receiver listens, writes each entry to a dated CSV, and both sides automatically reconnect if the connection drops.

## Project Layout 📁
- `Code/TCPIP_Sender.py` — connects to the receiver and streams random codes at a fixed interval.
- `Code/TCPIP_Receiver.py` — hosts the TCP listener and appends received codes to a CSV under `Data/receiver_log_YYYYMMDD.csv`.
- `Data/` — created on first run to store logs (one file per day).

## Requirements ✅
- Python 3.9+.
- Standard library only; `requirements.txt` is intentionally empty.

## Quick Start 🚀
1) Install Python if needed and open a terminal in the repo root.  
2) Start the receiver (in its own terminal):
   ```bash
   python Code/TCPIP_Receiver.py
   ```
   - Listens on `127.0.0.1:9005` by default.
   - Creates `Data/receiver_log_YYYYMMDD.csv` with headers `date,time,code`.
3) Start the sender (separate terminal):
   ```bash
   python Code/TCPIP_Sender.py
   ```
   - Connects to the receiver, sends a random code every 2 seconds, and reconnects after 5 seconds if disconnected.

## Configuration ⚙️
Edit the config section near the top of each script to match your network:
- IP/port: `receiver_ip`, `receiver_port` in both `Code/TCPIP_Sender.py` and `Code/TCPIP_Receiver.py` must match.
- Sender timing: `send_interval_seconds` (send cadence) and `reconnect_delay`.
- Receiver storage: `folder_name` (defaults to `Data`) and `encoding`.

## CSV Output 🧾
Each run appends to the daily file. Example rows:
```
date,time,code
12/03/2026,14:22:01,9G1Q8Z5A
12/03/2026,14:22:03,KF4LTW9B
```

## Notes ℹ️
- Keep the receiver running before starting the sender so the first connection succeeds.
- Both scripts print connection status and errors to the console for basic monitoring.
- Licensed under the MIT License (`LICENSE`).
