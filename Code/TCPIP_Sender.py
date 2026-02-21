"""
Docstring for TCPIP_Sender.py
Sends random 8-character codes over TCP to a specified receiver at regular intervals.
Automatically attempts to reconnect if the connection is lost.
"""

# import libraries
import socket
import time
import random
import string


print("Initializing TCPIP Sender...")

# -----------------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------------
receiver_ip = "127.0.0.1"           # receiver IP address, 127.0.0.1 for localhost
receiver_port = 9005                # Must match receiver port
send_interval_seconds = 2           # Send every N seconds
reconnect_delay = 5                 # Seconds before reconnect attempt
encoding = "utf-8"

# -----------------------------------------------------------------------------------
# RANDOM CHAR GENERATOR FUNCTION
# -----------------------------------------------------------------------------------
def generate_random_char_code(number_of_characters: int = 8) -> str:
    """
    Generate a random string of uppercase letters and digits.

    Parameters:
    - number_of_characters: The number of characters in the generated string. Default is 8.
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=number_of_characters))


def main() -> None:

    print(f"Receiver: {receiver_ip}:{receiver_port}")
    print(f"Send interval: {send_interval_seconds} seconds\n")

    # -----------------------------------------------------------------------------------
    # MAIN AUTO-RECONNECT LOOP
    # -----------------------------------------------------------------------------------

    while True:
        try:
            print(f"Connecting to receiver {receiver_ip}:{receiver_port}")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((receiver_ip, receiver_port))
            print(f"Connected!")

            # --------------------------------------------------------------------------
            # SEND LOOP
            # --------------------------------------------------------------------------
            i = 0
            while True:
                code = generate_random_char_code()
                message = code + "\n"   # newline = end of scan

                sock.sendall(message.encode(encoding))
                print(f"{i} Sent:", code)

                i += 1
                print(f"Sleeping for {send_interval_seconds} seconds...\n")
                time.sleep(send_interval_seconds)

        except Exception as e:
            print("Connection lost:", e)

        finally:
            try:
                sock.close()
            except:
                pass

            print(f"Reconnecting in {reconnect_delay} seconds...\n")
            time.sleep(reconnect_delay)


if __name__ == "__main__":
    main()

