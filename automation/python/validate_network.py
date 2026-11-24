from napalm import get_network_driver
import sys


def validate_device():
    # 1. Define the device details
    # (When your lab is ready, you will change this IP to your router's IP)
    device_details = {
        'hostname': '192.168.1.1',
        'username': 'admin',
        'password': 'admin',
        'optional_args': {'secret': 'admin'}  # Enable password
    }

    print(f"[*] Connecting to {device_details['hostname']} via NAPALM...")

    # 2. Get the IOS driver and instantiate the connection
    driver = get_network_driver('ios')
    device = driver(
        hostname=device_details['hostname'],
        username=device_details['username'],
        password=device_details['password'],
        optional_args=device_details['optional_args']
    )

    try:
        # 3. Open the connection
        device.open()
        print("[+] Connection successful!\n")

        # 4. Pull structured facts and interfaces
        print("--- VALIDATING INTERFACES ---")
        interfaces = device.get_interfaces()

        # 5. Write Assertions (The core of validation)
        # Let's check if GigabitEthernet0/1 is up and has the right description
        target_intf = 'GigabitEthernet0/1'

        if target_intf in interfaces:
            intf_data = interfaces[target_intf]
            print(f"Interface: {target_intf}")
            print(f"  Is Up: {intf_data['is_up']}")
            print(f"  Description: {intf_data['description']}")
            print(f"  MAC Address: {intf_data['mac_address']}")

            # The Assertion (If this fails, the script throws an error)
            assert intf_data['is_up'] is True, f"CRITICAL: {target_intf} is DOWN!"
            assert intf_data['description'] == "Uplink to ISP", f"CRITICAL: Wrong description on {target_intf}!"

            print(f"\n[✅] Validation PASSED for {target_intf}.")
        else:
            print(f"[!] Interface {target_intf} not found on device.")

        # 6. Close the connection
        device.close()

    except Exception as e:
        print(f"\n[!] Could not connect or validate: {e}")
        print("    (If you don't have a running lab, this is expected for Day 3).")
        sys.exit(1)


if __name__ == '__main__':
    validate_device()