import socket
import requests
from urllib.parse import urlparse

def analyze_ip(url):
    """
    Extracts the IP and performs external lookup.
    Uses ip-api.com for basic Geolocation info.
    Returns a list of warning strings if suspicious origin, else empty list.
    """
    warnings = []
    
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        
    parsed = urlparse(url)
    domain = parsed.netloc.split(':')[0]
    
    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror:
        return ["Could not resolve IP"]

    try:
        # Use ip-api's free endpoint (no key required, max 45 requests per min)
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                country = data.get('country', 'Unknown')
                
                # Mock AbuseIPDB logic / Warning thresholds
                # For demo purposes, flag if hosted in certain regions
                suspicious_countries = ['Russia', 'North Korea', 'Bulgaria', 'Seychelles']
                if country in suspicious_countries:
                    warnings.append(f"IP Geolocation warning: Hosted in {country}")
                    
                # Placeholder for VirusTotal / AbuseIPDB integration:
                # header = {'Key': 'YOUR_API_KEY'}
                # vt_response = requests.get(f"https://api.abuseipdb.com/api/v2/check", headers=header, params={"ipAddress": ip})
    except requests.RequestException:
        pass # Non-critical if lookup fails
        
    return warnings
