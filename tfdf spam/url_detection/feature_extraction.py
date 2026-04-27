import re
from urllib.parse import urlparse

def extract_features(url):
    """
    Extracts numerical features from a URL for ML training and prediction.
    Features:
    - url_length
    - num_dots
    - has_special_chars (0 or 1)
    - num_suspicious_keywords
    """
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    parsed = urlparse(url)
    domain_path = parsed.netloc + parsed.path
    
    url_length = len(url)
    num_dots = domain_path.count('.')
    
    # special chars meaning chars often used in obfuscation
    special_chars = re.compile(r'[@\-?=\+_%]')
    has_special_chars = 1 if special_chars.search(domain_path) else 0
    
    suspicious_keywords = [
        'login', 'secure', 'account', 'update', 'verify', 'bank', 
        'paypal', 'signin', 'free', 'bonus', 'claim', 'prize'
    ]
    num_suspicious_keywords = sum(1 for keyword in suspicious_keywords if keyword in url.lower())
    
    return [url_length, num_dots, has_special_chars, num_suspicious_keywords]
