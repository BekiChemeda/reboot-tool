import os
import time
import subprocess

ADB_PATH = os.path.join(os.path.dirname(__file__), 'tools', 'adb', 'adb.exe')

def wait_for_device():
    print("Waiting for a device to be connected...")

    while True:
        devices_output = subprocess.getoutput(f"{ADB_PATH} devices")

        devices = devices_output.splitlines()[1:]

        for device in devices:
            if "\tdevice" in device:
                print(f"Device connected: {device.split()[0]}")
                return device.split()[0]

        time.sleep(1)

def reboot_into_recovery(device_id):
    print(f"Rebooting {device_id} into recovery mode...")
    
    os.system(f"{ADB_PATH} -s {device_id} reboot recovery")
    
    time.sleep(10)
    
    retries = 0
    max_retries = 2

    while retries < max_retries:
        devices_output = subprocess.getoutput(f"{ADB_PATH} devices")

        if "recovery" in devices_output:
            print("Device is now in recovery mode.")
            return True
        
        print(f"Waiting for device to enter recovery mode... Attempt {retries + 1}/{max_retries}")
        time.sleep(3)
        retries += 1

    print("Device not detected in recovery mode. Please check the device manually.")
    return False

if __name__ == "__main__":
    try:
        while True:
            device_id = wait_for_device()
            success = reboot_into_recovery(device_id)  
            
            if success:
                print("Reboot complete. You can now manually perform a factory reset in recovery mode.")
            else:
                print("Manual intervention needed to proceed with the factory reset.")
            
            print("Restarting to wait for another device...\n")
    
    except KeyboardInterrupt:
        print("Program stopped by user.")
