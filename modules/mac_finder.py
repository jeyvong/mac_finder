import re
from modules.ssh_client import ssh_execute_command

def find_mac(ip, username, password, target_mac):
    command = f"show mac address-table | include {target_mac}"
    output = ssh_execute_command(ip, username, password, command)
    if not output:
        return None, False, {}

    found = False
    for line in output.splitlines():
        print(f"[🔎] Обработка строки MAC-таблицы: {line}")
        match = re.search(rf"{target_mac}\s+\w+\s+(\S+)", line)
        if match:
            port = match.group(1)
            is_port_channel = port.lower().startswith('po')  # Проверяем, Po ли это (Port-Channel)
            print(f"[✅] Найден порт {port} для MAC {target_mac} (Port-Channel: {is_port_channel})")
            return port, is_port_channel, [target_mac]

    return None, False, {}