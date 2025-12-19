import re
from modules.ssh_client import ssh_execute_command

def get_arp_neighbor_ip(ip, username, password, target_mac):
    command = f"show ip arp | include {target_mac}"
    output = ssh_execute_command(ip, username, password, command)
    if not output:
        return None

    escaped_mac = re.escape(target_mac)  # Делаем MAC literal (эскейпим точки и т.д.)
    for line in output.splitlines():
        print(f"[🔎] ARP строка: {line}")
        # Более гибкий regex: учитывает множественные пробелы/табы, и текст после MAC
        match = re.search(r"Internet\s+([\d.]+)\s+\d+\s+" + escaped_mac + r"\s*", line, re.IGNORECASE)
        if match:
            return match.group(1)

    return None