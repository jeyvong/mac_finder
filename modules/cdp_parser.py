import re
from modules.ssh_client import ssh_execute_command
from modules.utils import normalize_mac  # Новый импорт

def get_cdp_neighbor_ip(ip, username, password, interface, target_mac):  # Добавлен target_mac
    command = f"show cdp neighbors {interface} detail"
    output = ssh_execute_command(ip, username, password, command)
    if not output:
        return None

    for line in output.splitlines():
        print(f"[🔎] CDP строка: {line}")

    # Парсим Device ID (может содержать MAC)
    device_match = re.search(r"Device ID: (\S+)", output)
    if device_match:
        device_id = device_match.group(1)
        # Проверяем, содержит ли Device ID MAC-подобную строку
        mac_like = re.search(r"([0-9a-fA-F]{4}[.:-]?){3}", device_id)  # Грубый поиск MAC
        if mac_like:
            norm_device = normalize_mac(mac_like.group(0))
            norm_target = normalize_mac(target_mac)
            if norm_device == norm_target:
                print(f"[⚠️] Device ID {device_id} содержит target MAC {target_mac} — это конечное устройство, не переходим")
                return None

    # Парсим IP
    match = re.search(r"Management address\(es\):\s+IP address:\s+([\d.]+)", output)
    return match.group(1) if match else None