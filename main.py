import requests
from colorama import Fore
import os

url = 'http://httpbin.org/ip'

print("# PROXY CHECK\n# Github: https://github.com/ahmadxp/proxy-check\n")

proxies = input('Input your proxy list: ')
if not proxies.endswith('.txt'):
    proxies += '.txt'

def check():
    live = 0
    bad = 0
    try:
        with open(proxies, 'r') as proxy:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Start checking...")
            for proxy in proxy:
                proxy = proxy.strip()
                try:
                    # Send a GET request to the URL
                    response = requests.get(url, proxies={'http': proxy, 'https': proxy}, timeout=5)
                    if response.status_code == 200: # If the request was successful
                        live += 1
                        ip_origin = response.json()['origin']
                        loc = requests.get(f'https://ipinfo.io/{ip_origin}/json')
                        if loc.status_code == 200:
                            print(f"{Fore.GREEN}[LIVE - {loc.json()['country']}] {Fore.RESET}{proxy}") # Print proxy and country
                            with open('result.txt', 'a') as f:
                                f.write(f"{proxy}\n")
                        else:
                            print(f"{Fore.GREEN}[LIVE] {Fore.RESET}{proxy}")
                            with open('result.txt', 'a') as f:
                                f.write(f"{proxy}\n")
                    elif response.status_code == 407:
                        bad += 1
                        print(f"{Fore.YELLOW}[Invalid Auth] {Fore.RESET}{proxy}") # 407 Proxy Authentication Required
                    elif response.status_code == 429:
                        bad += 1
                        print(f"{Fore.YELLOW}[Too Many Requests] {Fore.RESET}{proxy}") # Too Many Requests
                except requests.exceptions.ConnectionError:
                    bad += 1
                    print(f"{Fore.RED}[BAD] {Fore.RESET}{proxy}")  # Connection errors
                except requests.exceptions.Timeout:
                    bad += 1
                    print(f"{Fore.YELLOW}[Timeout] {Fore.RESET}{proxy}")  # Timeouts
                except requests.exceptions.RequestException as e:
                    bad += 1
                    print(f"{Fore.RED}[BAD] {Fore.RESET}{proxy} {e}")
        
            print(f"\nTotal Proxy ~ {Fore.GREEN}Live:{live} {Fore.RED}Bad:{bad}") # Print the number of good and bad proxies
            print(f"{Fore.RESET}Live proxy list saved in result.txt")

    except FileNotFoundError:
        print(f"{Fore.RED}{proxies} file not found.")

if __name__ == '__main__':
    check()