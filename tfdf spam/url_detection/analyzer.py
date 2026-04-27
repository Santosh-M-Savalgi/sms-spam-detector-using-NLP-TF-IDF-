from url_detection.ml_model import predict_url
from url_detection.network_analysis import check_network
from url_detection.ip_analysis import analyze_ip

def analyze_url(url):
    """
    Coordinates all checks for a single URL and determines overall risk.
    """
    ml_prediction, confidence = predict_url(url)
    network_warnings = check_network(url)
    ip_warnings = analyze_ip(url)
    
    all_warnings = network_warnings + ip_warnings
    
    # Determine risk level based on ML & warnings
    if ml_prediction == "fraud":
        risk_level = "High"
    elif len(all_warnings) > 1:
        risk_level = "Medium"
    elif confidence >= 0.3 and len(all_warnings) > 0:
        risk_level = "Medium"
    else:
        risk_level = "Low"
        
    return {
        "url": url,
        "prediction": ml_prediction,
        "risk_level": risk_level,
        "confidence": confidence,
        "warnings": all_warnings
    }
