import paramiko
import time

def ssh_execute_command(ip, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(ip, username=username, password=password, timeout=10)
        shell = client.invoke_shell()
        shell.send("terminal length 0\n")
        time.sleep(0.5)
        shell.send(command + "\n")
        time.sleep(1)
        output = shell.recv(99999).decode("utf-8")
        print(f"[📥] Ответ от {ip} на команду '{command}':\n{output}")  # добавлен вывод команды
        client.close()
        return output
    except Exception as e:
        print(f"[❌] SSH error to {ip}: {e}")
        return None