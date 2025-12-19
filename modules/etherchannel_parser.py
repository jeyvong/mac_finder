import re
from modules.ssh_client import ssh_execute_command

def get_etherchannel_ports(ip, username, password, port_channel):
    # Извлекаем номер Po, напр. Po5 -> 5
    po_match = re.search(r'po(\d+)', port_channel.lower(), re.IGNORECASE)
    if not po_match:
        return []

    po_num = po_match.group(1)
    group_prefix = f"{po_num} "  # Для поиска строки вроде "5 Po5(SU) ..."

    command = "show etherchannel summary"
    output = ssh_execute_command(ip, username, password, command)
    if not output:
        return []

    physical_ports = []
    parsing_table = False
    for line in output.splitlines():
        print(f"[🔎] EtherChannel строка: {line}")
        stripped_line = line.strip()

        # Начинаем парсинг после заголовка таблицы
        if "------" in stripped_line:
            parsing_table = True
            continue

        if parsing_table and stripped_line.startswith(group_prefix):
            # Ищем все порты с (P) — bundled, игнорируя (D) и другие
            ports = re.findall(r'(\w+/\d+(?:/\d+)?)\(P\)', stripped_line)
            physical_ports.extend(ports)
            break  # Останавливаемся после нахождения нашей строки

    print(f"[✅] Физические порты в {port_channel}: {physical_ports}")
    return physical_ports