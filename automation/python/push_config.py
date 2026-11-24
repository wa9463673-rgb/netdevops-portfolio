import os
import yaml
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

# --- SAFETY SWITCH ---
DRY_RUN = True


def generate_config():
    """Reads YAML and renders the Jinja2 template using absolute paths."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

    inventory_file = os.path.join(base_dir, 'inventory', 'r1_data.yml')
    template_dir = os.path.join(base_dir, 'templates')

    with open(inventory_file, 'r') as file:
        device_data = yaml.safe_load(file)

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('router_config.j2')
    return template.render(device_data)


def push_to_device(config_commands):
    """Connects to the device and pushes the config."""
    device = {
        'device_type': 'cisco_ios',
        'host': '192.168.1.1',
        'username': 'admin',
        'password': 'admin',
        'secret': 'admin',
        'session_log': 'netmiko_session.log'
    }

    print("\n[+] Connecting to " + device['host'] + "...")

    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()

        print("[+] Sending configuration commands...")
        commands_list = config_commands.splitlines()

        output = net_connect.send_config_set(commands_list)
        print("\n--- DEVICE OUTPUT ---")
        print(output)

        net_connect.save_config()
        net_connect.disconnect()
        print("\n[+] Success! Configuration applied.")

    except NetmikoAuthenticationException:
        print("\n[!] Authentication failed. Check your username/password.")
    except NetmikoTimeoutException:
        print("\n[!] Connection timed out. Is the device reachable?")
    except Exception as e:
        print("\n[!] An error occurred: " + str(e))


if __name__ == '__main__':
    print("--- Starting Network Automation Script ---")
    config_to_push = generate_config()

    if DRY_RUN:
        print("\n[DRY RUN MODE] - No changes will be pushed to the device.")
        print("--- Generated Configuration ---")
        print(config_to_push)
        print("-------------------------------")
        print("[!] To push this, set DRY_RUN = False")
    else:
        push_to_device(config_to_push)