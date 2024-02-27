import argparse
import os
import requests
import sys
import time
from urllib.parse import urlparse
from multiprocessing.dummy import Pool as ThreadPool
from collections import defaultdict

max_workers = 40

def read_hosts(filename):
    hosts = []
    try:
        with open(filename, 'r') as file:
            hosts = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print("Please provide a valid .txt file name")
    return hosts

def check_status(hosts, follow_redirects):
    print("SCAN STARTED.....")
    results = defaultdict(list)

    def process_host(host):
        try:
            # Make the HTTP request
            response = requests.get(host, allow_redirects=follow_redirects)
            
            # Get the final URL after following redirects
            final_url = response.url
            
            # Store the final URL
            results[response.status_code].append(final_url)
        except Exception as e:
            print(f"Error processing {host}: {e}")

    pool = ThreadPool(max_workers)
    pool.map(process_host, hosts)
    pool.close()
    pool.join()

    for status_code, final_urls in results.items():
        print(f"{len(final_urls)} domains have resolved to status code {status_code}")
        with open(f"{status_code}.txt", 'w') as file:
            for final_url in final_urls:
                file.write(f"{final_url}\n")

def main():
    parser = argparse.ArgumentParser(description="URL Scanner")
    parser.add_argument("-file", required=True, help="path to the input file")
    parser.add_argument("-redirects", action="store_true", help="follow redirects")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print("Please provide a valid input file path.")
        sys.exit(1)

    print_ascii_art()
    hosts = read_hosts(args.file)
    check_status(hosts, args.redirects)

def print_ascii_art():
    print("""
__________        ________                        .__           _________.__  .__                     
\______   \___.__.\______ \   ____   _____ _____  |__| ____    /   _____/|  | |__| ____  ___________  
 |     ___<   |  | |    |  \ /  _ \ /     \\__  \ |  |/    \   \_____  \ |  | |  |/ ___\/ __ \_  __ \ 
 |    |    \___  | |    `   (  <_> )  Y Y  \/ __ \|  |   |  \  /        \|  |_|  \  \__\  ___/|  | \/ 
 |____|    / ____|/_______  /\____/|__|_|  (____  /__|___|  / /_______  /|____/__|\___  >___  >__|    
           \/             \/             \/     \/        \/          \/              \/    \/ 
    """)

if __name__ == "__main__":
    main()
