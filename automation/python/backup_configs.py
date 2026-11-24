import os
import datetime
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException
import git


def get_device_config():
    """Attempts to pull config from router. Falls back to mock data if unreachable."""
    device = {
        'device_type': 'cisco_ios',
        'host': '192.168.1.1',
        'username': 'admin',
        'password': 'admin',
    }

    try:
        print(f"[*] Attempting to connect to {device['host']}...")
        net_connect = ConnectHandler(**device, timeout=5)
        config = net_connect.send_command('show running-config')
        net_connect.disconnect()
        print("[+] Successfully pulled live configuration.")
        return config

    except NetmikoTimeoutException:
        print("\n[!] Device unreachable. (Expected on this Mac).")
        print("[*] Generating MOCK configuration for testing Git automation...\n")
        mock_config = (
            "hostname R1-Core\n"
            "!\n"
            "interface GigabitEthernet0/1\n"
            " description Uplink to ISP\n"
            " ip address 203.0.113.1 255.255.255.252\n"
            "!\n"
            "end\n"
        )
        return mock_config


def backup_and_commit():
    """Saves the config and commits it to Git."""
    config_data = get_device_config()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")

    # FIX: Calculate the absolute path to the root 'backups' folder
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    backup_dir = os.path.join(base_dir, 'backups')

    # Ensure the directory exists (just in case)
    os.makedirs(backup_dir, exist_ok=True)

    filename = os.path.join(backup_dir, f"r1_backup_{timestamp}.cfg")

    # Write the config to the file
    with open(filename, 'w') as f:
        f.write(config_data)
    print(f"[+] Backup saved to {filename}")

    # Automate Git
    print("[*] Committing backup to Git...")
    try:
        repo = git.Repo(base_dir)
        repo.git.add(filename)

        commit_message = f"chore: automated config backup for r1 ({timestamp})"
        repo.index.commit(commit_message)

        print(f"[✅] Git commit successful: '{commit_message}'")
    except Exception as e:
        print(f"[!] Git error: {e}")


if __name__ == '__main__':
    print("--- Starting Nightly Config Backup ---")
    backup_and_commit()