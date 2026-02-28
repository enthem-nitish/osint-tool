#!/usr/bin/env python3
# main.py
# Developer: Nitish Sharma
# Powered By: Black Enthem

import sys
import json
import requests
from itertools import cycle

# Encoded API endpoint
API_BASE = "68747470733a2f2f6f776e2d6170692d62792d656e7468656d2e6f6e72656e6465722e636f6d2f6170693f6163636573733d454e5448454d266e756d6265723d"

# Gradient colors (ANSI escape codes)
GRADIENT = [
    "\033[91m",  # red
    "\033[93m",  # yellow
    "\033[92m",  # green
    "\033[96m",  # cyan
    "\033[94m",  # blue
    "\033[95m",  # magenta
]
RESET = "\033[0m"
BOLD = "\033[1m"

BANNER_TEXT = r"""
  _   _                 _   _       _           
 | \ | | ___  _ __ ___ | \ | |_   _| | ___  ___ 
 |  \| |/ _ \| '_ ` _ \|  \| | | | | |/ _ \/ __|
 | |\  | ( ) | | | | | | |\  | | | | |\  _/\_ \
 | | \ |\   /| | | | | | | \ |\,/| | | \ | |  /
"""

DEV_INFO = f"""{BOLD}\033[92mDeveloper : Nitish Sharma{RESET}
{BOLD}\033[96mPowered By: Zishan Raza{RESET}
"""

def decode_api_base():
    import base64
    return base64.b64decode(API_BASE).decode('utf-8')

def print_gradient_banner(text: str):
    colors = cycle(GRADIENT)
    out = ""
    for line in text.splitlines():
        colored_line = ""
        for char in line:
            if char.strip():
                colored_line += next(colors) + char + RESET
            else:
                colored_line += char
        out += colored_line + "\n"
    print(out)

def fetch_number_info(num, timeout=15):
    api_url = decode_api_base()
    url = api_url + str(num)
    headers = {"User-Agent": "MyNumInfoTool/2.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def stylish_print(data, indent=0):
    """Print JSON in stylish format"""
    indent_str = " " * indent
    if isinstance(data, dict):
        for k, v in data.items():
            print(f"{indent_str}{BOLD}\033[96m{k}:\033[0m ", end="")
            if isinstance(v, (dict, list)):
                print()
                stylish_print(v, indent + 4)
            else:
                if isinstance(v, bool):
                    color = "\033[92m" if v else "\033[91m"
                    print(color + str(v) + RESET)
                elif isinstance(v, (int, float)):
                    print("\033[93m" + str(v) + RESET)
                elif v is None:
                    print("\033[90mnull" + RESET)
                else:
                    print("\033[97m" + str(v) + RESET)
    elif isinstance(data, list):
        for i, item in enumerate(data, 1):
            print(f"{indent_str}{BOLD}\033[95m[{i}]\033[0m")
            stylish_print(item, indent + 4)
    else:
        print(indent_str + str(data))

def is_valid_number(s):
    s = s.strip()
    if s.startswith("+"):
        s2 = s[1:]
    else:
        s2 = s
    return s2.isdigit() and 6 <= len(s2) <= 15

def main():
    print_gradient_banner(BANNER_TEXT)
    print(DEV_INFO)
    try:
        while True:
            num = input(f"\n{BOLD}Enter Mobile Number : {RESET}").strip()
            if not num:
                print("Empty input detected. Exiting.")
                sys.exit(0)
            if not is_valid_number(num):
                print("Invalid number format. Example: +919876543210 or 9876543210")
                continue

            print("\n\033[93mFetching details... Please wait...\033[0m\n")
            data = fetch_number_info(num)

            print(f"{BOLD}\033[92m--- Result ---{RESET}\n")
            stylish_print(data)
            print(f"\n{BOLD}\033[92m--- End ---{RESET}\n")

            again = input("Query another number? [y/N]: ").strip().lower()
            if again not in ("y", "yes"):
                print("\033[91mGoodbye.\033[0m")
                break
    except KeyboardInterrupt:
        print("\nInterrupted. Bye.")
        sys.exit(0)

if __name__ == "__main__":

    main()
