import requests
from colorama import Fore
import os

url = 'http://httpbin.org/ip'

print("# PROXY CHECK WITH TYPE\n# Github: https://github.com/ahmadxp/proxy-check\n")

proxies = input('Input your proxy list: ')
if not proxies.endswith('.txt'):
    proxies += '.txt'

def detect_proxy_type(ip):
    """Detect proxy type using IP analysis"""
    try:
        # Check 1: Detect hosting/datacenter IP
        response = requests.get(f'https://ipapi.co/{ip}/json/', timeout=5)
        data = response.json()
        
        if 'error' not in data:
            # Check for datacenter/hosting IP
            if data.get('org', '').lower() in ('google', 'amazon', 'microsoft', 'digitalocean', 'linode', 'ovh', 'alibaba', 'tencent', 'vultr'):
                return "Hosting"
            # Check for ASN patterns common in datacenters
            asn = data.get('asn', '').lower()
            if any(keyword in asn for keyword in ['hosting', 'cloud', 'server', 'datacenter']):
                return "Hosting"
            # Check 2: Detect residential IP
            ipinfo = requests.get(f'https://ipinfo.io/{ip}/json', timeout=5).json()
            if ipinfo.get('org', '').lower() in ('isp', 'internet service provider'):
                return "Residential"
            # Check for mobile IPs
            if ipinfo.get('mobile', False):
                return "Residential (Mobile)"
            # If none of the above, consider it anonymous
            return "Anonymous"
        
    except Exception:
        pass
    
    # Fallback to simple detection (Dead API, will change the API soon)
    # try:
        # Check if the IP is from known cloud providers
        # rdns = requests.get(f'https://rdns.apimon.de/{ip}', timeout=3).json()
        # if rdns.get('rdns', ''):
            # if any(domain in rdns['rdns'].lower() for domain in ['.google.', '.amazonaws.', '.azure.', '.cloud.', '.hosting.']):
                # return "Hosting"
    # except Exception:
        # pass
    
    # return "Unknown"

def check():
    live = 0
    bad = 0
    try:
        with open(proxies, 'r') as proxy:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Start checking...")
            for proxy in proxy:
                proxy = proxy.strip()
                if not proxy:
                    continue
                try:
                    # Send a GET request to the URL
                    response = requests.get(url, proxies={'http': proxy, 'https': proxy}, timeout=5)
                    if response.status_code == 200:
                        live += 1
                        # Get location and proxy type
                        ip_origin = response.json()['origin']
                        loc = requests.get(f'https://ipinfo.io/{ip_origin}/json', timeout=5)
                        proxy_type = detect_proxy_type(ip_origin)
                        
                        if loc.status_code == 200:
                            loc_data = loc.json()
                            country = loc_data.get('country', 'Unknown')
                            org = loc_data.get('org', 'Unknown')[:30]  # Truncate long org names
                            
                            print(f"{Fore.GREEN}[LIVE - {country} - {proxy_type}] {Fore.RESET}{proxy} {Fore.CYAN}({org}){Fore.RESET}")
                            with open('result-2.txt', 'a') as f:
                                f.write(f"{proxy} | Country: {country} | Type: {proxy_type} | Org: {org}\n")
                        else:
                            print(f"{Fore.GREEN}[LIVE - {proxy_type}] {Fore.RESET}{proxy}")
                            with open('result-2.txt', 'a') as f:
                                f.write(f"{proxy} | Type: {proxy_type}\n")
                                
                    elif response.status_code == 407:
                        bad += 1
                        print(f"{Fore.YELLOW}[Invalid Auth] {Fore.RESET}{proxy}") # 407 Proxy Authentication Required
                    elif response.status_code == 429:
                        bad += 1
                        print(f"{Fore.YELLOW}[Too Many Requests] {Fore.RESET}{proxy}") # To Many Request
                        
                except requests.exceptions.ConnectionError:
                    bad += 1
                    print(f"{Fore.RED}[BAD] {Fore.RESET}{proxy}") # Connection errors
                except requests.exceptions.Timeout:
                    bad += 1
                    print(f"{Fore.YELLOW}[Timeout] {Fore.RESET}{proxy}") # Timeouts
                except requests.exceptions.RequestException as e:
                    bad += 1
                    print(f"{Fore.RED}[BAD] {Fore.RESET}{proxy} {e}")
        
        print(f"\nTotal Proxy ~ {Fore.GREEN}Live: {live} {Fore.RED}Bad: {bad}") # Print the number of good and bad proxies
        print(f"{Fore.RESET}Live proxy list saved in result-2.txt")

    except FileNotFoundError:
        print(f"{Fore.RED}{proxies} file not found.{Fore.RESET}")

if __name__ == '__main__':
    check()