import re
from modules.ssh_client import ssh_execute_command
from modules.utils import normalize_mac  # Новый импорт

def get_lldp_neighbor_ip(ip, username, password, interface, target_mac):  # Добавлен target_mac
    command = f"show lldp neighbors {interface} detail"
    output = ssh_execute_command(ip, username, password, command)
    if not output:
        return None

    for line in output.splitlines():
        print(f"[🔎] LLDP строка: {line}")

    # Парсим Chassis ID
    chassis_match = re.search(r"Chassis id: (\S+)", output)
    if chassis_match:
        chassis_id = chassis_match.group(1)
        norm_chassis = normalize_mac(chassis_id)
        norm_target = normalize_mac(target_mac)
        if norm_chassis == norm_target:
            print(f"[⚠️] Chassis ID {chassis_id} совпадает с target MAC {target_mac} — это конечное устройство, не переходим")
            return None

    # Парсим IP
    match = re.search(r"Management Addresses:\s+IP:\s+([\d.]+)", output)
    return match.group(1) if match else None