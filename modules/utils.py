def normalize_mac(mac_str):
    """Normalize MAC by removing separators and lowercasing."""
    return mac_str.lower().replace('.', '').replace(':', '').replace('-', '')