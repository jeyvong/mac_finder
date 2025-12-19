from modules.mac_finder import find_mac
from modules.lldp_parser import get_lldp_neighbor_ip
from modules.cdp_parser import get_cdp_neighbor_ip
from modules.arp_finder import get_arp_neighbor_ip
from modules.etherchannel_parser import get_etherchannel_ports

def traceroute_mac(start_ip, username, password, target_mac, visited=None):
    if visited is None:
        visited = set()

    if start_ip in visited:
        print(f"[⚠️] Цикл обнаружен: {start_ip} уже посещен")
        return

    visited.add(start_ip)
    print(f"[🔗] Подключение к {start_ip} ...")

    port, is_port_channel, macs = find_mac(start_ip, username, password, target_mac)

    if not port:
        print(f"[❌] MAC {target_mac} не найден на {start_ip}")
        return

    print(f"[✅] MAC {target_mac} найден на порту {port}")

    physical_ports = [port]
    if is_port_channel:
        print(f"[🔄] Порт {port} — Port-Channel, разбираем состав...")
        physical_ports = get_etherchannel_ports(start_ip, username, password, port)
        if not physical_ports:
            print(f"[❌] Не удалось получить физические порты для {port}")
            physical_ports = []

    neighbor_ip = None
    for phys_port in physical_ports:
        # LLDP с target_mac
        neighbor_ip = get_lldp_neighbor_ip(start_ip, username, password, phys_port, target_mac)
        if neighbor_ip:
            print(f"[✅] LLDP: Сосед {neighbor_ip} на порту {phys_port}")
            break

    if not neighbor_ip:
        for phys_port in physical_ports:
            # CDP с target_mac
            neighbor_ip = get_cdp_neighbor_ip(start_ip, username, password, phys_port, target_mac)
            if neighbor_ip:
                print(f"[✅] CDP: Сосед {neighbor_ip} на порту {phys_port}")
                break

    if not neighbor_ip:
        # ARP без проверки, last resort
        neighbor_ip = get_arp_neighbor_ip(start_ip, username, password, target_mac)
        if neighbor_ip:
            print(f"[✅] ARP: Сосед {neighbor_ip} по MAC {target_mac}")

    if neighbor_ip and neighbor_ip not in visited:
        traceroute_mac(neighbor_ip, username, password, target_mac, visited)
    else:
        print(f"[🎯] Найден конечный порт на {start_ip}: {port} (физические: {physical_ports})")
        if not neighbor_ip:
            print("[⚠️] Нет IP соседа для дальнейшего перехода")