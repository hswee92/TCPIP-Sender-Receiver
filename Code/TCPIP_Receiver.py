"""
Log data from Sender over TCP/IP and persist to CSV.

Responsibilities:
- Establish TCP/IP connection with Sender.
- Automatically reconnect on disconnection.
"""

# import libraries
import datetime
import socket
import csv
from dataclasses import dataclass
from pathlib import Path


print("Initializing TCPIP Receiver...")

# -----------------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------------
receiver_ip = "127.0.0.1"           # receiver IP address, 127.0.0.1 for localhost
receiver_port = 9005                # Must match sender port
encoding = "utf-8"
folder_name = "Data"                # folder to save CSV files in

# -----------------------------------------------------------------------------------
# LOGGING FUNCTION
# -----------------------------------------------------------------------------------
def save_to_csv(data: str, file_path: Path) -> None:
    """
    Save scanned barcode data to a CSV file.

    Parameters:
    - data: The barcode data to save.
    - file_path: The Path to the CSV file where data will be appended.
    """
    if not file_path.exists():
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "time", "code"])  # header
            print(f"Created new CSV file at \"{file_path}\"")
    
    try:
        with open(file_path, 'a') as f:
            f.write(f"{data}\n")
        print(f"Saved: {data}\n")
    except Exception as e:
        print(f"Failed to save barcode data: {e}")


def main() -> None:
    # get location of current .py file
    code_dir = Path(__file__).resolve().parent 
    main_dir = code_dir.parent

    # -----------------------------------------------------------------------------------
    # Initialize File Storage Directory
    # -----------------------------------------------------------------------------------

    print("Initializing data storage...")
 
    file_dir = main_dir / folder_name

    if not file_dir.exists():
        # create data directory
        file_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created directory \"{file_dir}\"")
    else: 
        print(f"Directory \"{file_dir}\" already exists.")


    # -----------------------------------------------------------------------------------
    # Initialize TCP/IP Connection with Sender
    # -----------------------------------------------------------------------------------
    
    print(f"Establishing TCPIP connection with {receiver_ip}:{receiver_port}")
    
    # establish TCP/IP connection with Sender
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((receiver_ip, receiver_port))
    server_socket.listen(1)


    # -----------------------------------------------------------------------------------
    # MAIN LOOP
    # -----------------------------------------------------------------------------------

    while True:
        try:
            print("Waiting to accept socket connection...")
            conn, addr = server_socket.accept()
            print(f"Sender connected from {addr}")

            while True:
                data = conn.recv(1024)
                if not data:
                    print("Sender disconnected.")
                    break

                payload = data.decode(encoding, errors="ignore").strip()
                code = payload.strip()             
                print(f"Received: {code}")  

                # Format date: DD/MM/YYYY time: HH:MM:SS
                str_date = datetime.datetime.now().strftime("%d/%m/%Y")
                str_time = datetime.datetime.now().strftime("%H:%M:%S")
                file_suffix = datetime.datetime.now().strftime("%Y%m%d")

                # Prepare data filepath
                data_filepath = file_dir / f"receiver_log_{file_suffix}.csv"

                # Append to CSV
                save_to_csv(f"{str_date},{str_time},{code}", file_path=data_filepath)
                    

        except Exception as e:
            print(f"Network error: {e}")

        finally:
            try:
                conn.close()
                print("TCPIP Connection closed.")
            except:
                pass
                


if __name__ == "__main__":
    main()
