import socket
import requests
from urllib.parse import urlparse
import ssl

def check_network(url):
    """
    Performs basic network analysis on the URL.
    Checks DNS availability, HTTP redirects, and SSL status.
    Returns a list of warning strings if anomalies are found, else empty list.
    """
    warnings = []
    
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        
    parsed = urlparse(url)
    domain = parsed.netloc.split(':')[0] # Remove port if exists
    
    # 1. DNS Lookup Check
    try:
        socket.gethostbyname(domain)
    except socket.gaierror:
        warnings.append("DNS record unavailable (domain might be fake or offline)")
        
    # 2. Redirect / Status Check
    try:
        # Use a short timeout so we don't block the API deeply
        response = requests.head(url, allow_redirects=True, timeout=2)
        if len(response.history) > 2:
            warnings.append(f"Multiple redirects detected ({len(response.history)})")
        if response.status_code >= 400:
            warnings.append(f"HTTP Error {response.status_code}")
    except requests.RequestException:
        warnings.append("Connection failed or timed out")
        
    # 3. SSL Check (very basic port 443 connectivity)
    if url.startswith('https://'):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=2) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    ssock.version()
        except Exception:
            warnings.append("Invalid or missing SSL certificate for HTTPS")

    return warnings
