import yaml
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

# --- SAFETY SWITCH ---
# Set this to False ONLY when you are ready to push to a real device!
DRY_RUN = True

def generate_config():
    """Reads YAML and renders the Jinja2 template."""
    # Notice the ../../ - this goes up two folders to find the root
    with open('../../inventory/r1_data.yml', 'r') as file:
        device_data = yaml.safe_load(file)

    env = Environment(loader=FileSystemLoader('../../templates'))
    template = env.get_template('router_config.j2')
    return template.render(device_data)

def push_to_device(config_commands):
    """Connects to the device and pushes the config."""

    # For now, this is a dummy IP. When your lab is ready, change this.
    device = {
        'device_type': 'cisco_ios',
        'host': '192.168.1.1',     # We will change this to your lab IP later
        'username': 'admin',
        'password': 'admin',
        'secret': 'admin',         # Enable secret
        'session_log': 'netmiko_session.log' # Keeps a log of the SSH session
    }

    print(f"\n[+] Connecting to {device['host']}...")

    try:
        # Establish SSH connection
        net_connect = ConnectHandler(**device)

        # Enter enable mode
        net_connect.enable()

        print("[+] Sending configuration commands...")
        # Split the generated config into a list of lines for Netmiko
        commands_list = config_commands.splitlines()

        # Push the config
        output = net_connect.send_config_set(commands_list)
        print("\n--- DEVICE OUTPUT ---")
        print(output)

        # Save the running config to startup config
        net_connect.save_config()

        net_connect.disconnect()
        print("\n[+] Success! Configuration applied.")

    except NetmikoAuthenticationException:
        print("\n[!] Authentication failed. Check your username/password.")
    except NetmikoTimeoutException:
        print("\n[!] Connection timed out. Is the device reachable?")
    except Exception as e:
        print(f"\n[!] An error occurred: {e}")

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