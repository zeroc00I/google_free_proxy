import threading
import requests
import re
import argparse
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extract_value_from_host(host):
    try:
        #print(f"Fetching {host}...")
        response = requests.get("https://docs.google.com/gview?url="+host+"&embedded=true",verify=False)
        if response.status_code == 200:
            token =  response.text.split('"')[-12].replace("meta?id\\u003d","")
            get_content_with_token_from_google(token)

        """
        else:
            print(f"[-] Failed to fetch {host}. Status code: {response.status_code}")
        """
    except Exception as e:
        print(f"An error occurred while processing {host}: {e}")

def get_content_with_token_from_google(token):
    response = requests.get(f"https://docs.google.com/viewerng/text?id={token}&authuser=0&page=0",verify=False)
    final_response = json.loads(response.text.replace(")]}'",""))["data"].replace("\n","")
    #print(f"[+] Final response {final_response}")
    print(f"{final_response}")

def main():
    parser = argparse.ArgumentParser(description='Extract values from HTML tags in a list of hosts.')
    parser.add_argument('-i', '--input', help='Input file containing list of hosts', required=True)
    args = parser.parse_args()

    with open(args.input, 'r') as file:
        hosts = file.readlines()

    threads = []
    for host in hosts:
        host = host.strip()
        thread = threading.Thread(target=extract_value_from_host, args=(host,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
