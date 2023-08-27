import os
import subprocess
import time

from loguru import logger
from pynput.mouse import Button, Controller

dnplayer = r'C:\LDPlayer\LDPlayer9\dnplayer.exe'


class LDPlayerManager:
    def __init__(self, ldconsole_path, dnconsole_path):
        self.ldconsole_path = ldconsole_path
        self.dnconsole_path = dnconsole_path

    def run_command(self, cmd):
        if cmd[0] == "touch" or cmd[0] == "adb":
            # Format the command as a string
            cmd_str = " ".join(cmd)
            # Use the dnconsole_path to run the command
            os.system(f"{self.dnconsole_path} {cmd_str}")
        # elif cmd[0] == "adb":
        #     result = subprocess.run([dnplayer] + cmd, capture_output=True, text=True)
        #     return result.stdout
        else:
            # Use the ldconsole_path to run the command
            result = subprocess.run([self.ldconsole_path] + cmd, capture_output=True, text=True)
            return result.stdout

    def list_vms(self):
        cmd = ["list2"]
        result = subprocess.run([self.dnconsole_path] + cmd, capture_output=True, text=True)
        instances = [line.split(",")[1] for line in result.stdout.splitlines()[1:] if line]
        # print(f"list_vms output: {result.stdout}")  # debug print
        return instances

    def get_all_vms_status(self):
        cmd = ['list2']
        result = subprocess.run([self.dnconsole_path] + cmd, capture_output=True, text=True)
        instances = {}
        for line in result.stdout.splitlines():
            data = line.split(',')
            if len(data) >= 6:
                name = data[1].strip()
                started = data[4].strip()
                if started == '1':
                    status = 'running'
                else:
                    status = 'stopped'
            else:
                status = 'unknown'
            instances[name] = status
        return instances

    def print_vm_table(self, instance_statuses, status_filter=None):
        print("\nInstance Dashboard:")
        print("ID".ljust(5), "Instance Name".ljust(30), "Status")
        running_vms = []
        stopped_vms = []
        unknown_vms = []
        for instance, status in instance_statuses.items():
            if status == "running":
                running_vms.append(instance)
            elif status == "stopped":
                stopped_vms.append(instance)
            else:
                unknown_vms.append(instance)
        if status_filter == "running":
            instances = running_vms
        elif status_filter == "stopped":
            instances = stopped_vms
        else:
            instances = running_vms + stopped_vms + unknown_vms
        for idx, instance in enumerate(instances, start=1):
            status = instance_statuses[instance]
            print(str(idx).ljust(5), instance.ljust(30), status)
        print("\nSummary:")
        print(f"{len(running_vms)} instances running")
        print(f"{len(stopped_vms)} instances stopped")
        print(f"{len(unknown_vms)} instances in an unknown state")

    def create_vm(self, vm_name):
        cmd = ["add", "--name", vm_name]
        self.run_command(cmd)

        # Wait for the instance to start up
        time.sleep(5)

    def start_vm(self, vm_name):
        cmd = ["launch", "--name", vm_name]
        self.run_command(cmd)

        # Wait for the instance to start up
        time.sleep(5)

        # cmd = ["adb", "-s", vm_name, '--command', 'shell netcfg']
        # print("devises:\n", self.run_command(cmd))
        # cmd = ['adb', '--name', vm_name, '--command', 'shell getprop']
        cmd = ['adb', '--name', vm_name, '--command', 'devices', '-l']
        result = subprocess.call(" ".join([self.dnconsole_path] + cmd), shell=True)
        # result_list = str(self.run_command(cmd))
        logger.debug(f'devises: {result}')

    def stop_vm(self, vm_name):
        cmd = ["quit", "--name", vm_name]
        self.run_command(cmd)

    def restart_vm(self, vm_name):
        self.stop_vm(vm_name)
        self.start_vm(vm_name)

        # Wait for the instance to start up
        time.sleep(5)


def print_vm_table(instance_statuses):
    print("\nInstance Dashboard:")
    print("ID\tInstance Name\tStatus")
    for idx, (instance, status) in enumerate(instance_statuses.items(), start=1):
        print(f"{idx}\t{instance}\t{status}")


def get_action():
    print("\nActions:")
    print("1. Start instance")
    print("2. Stop instance")
    print("3. Restart instance")
    print("4. Refresh dashboard")
    print("5. Exit")


if __name__ == '__main__':

    ldconsole_path = r'C:\LDPlayer\LDPlayer9\ldconsole.exe'  # Replace with the path to your ldconsole.exe
    dnconsole_path = r'C:\LDPlayer\LDPlayer9\dnconsole.exe'  # Replace with the path to your dnconsole.exe

    manager = LDPlayerManager(ldconsole_path, dnconsole_path)

    instances = manager.list_vms()

    instance_statuses = manager.get_all_vms_status()
    manager.print_vm_table(instance_statuses)

    while True:
        get_action()
        choice = input("Enter your choice: ")
        if choice in ["1", "2", "3"]:
            if choice == "1":
                action = "start"
                valid_vms = [instance for instance, status in instance_statuses.items() if status == "stopped"]
            elif choice == "2":
                action = "stop"
                valid_vms = [instance for instance, status in instance_statuses.items() if status == "running"]
            else:
                action = "restart"
                valid_vms = [instance for instance, status in instance_statuses.items() if status == "running"]
            if not valid_vms:
                print(f"No valid instances to {action}.")
                continue
            print("Instances:")
            for idx, instance in enumerate(valid_vms, start=1):
                print(f"{idx}. {instance}")
            instance_index = int(input("Enter the index of the instance: ")) - 1
            vm_name = valid_vms[instance_index]
            status = instance_statuses[vm_name]
            try:
                if instance_index < 0 or instance_index >= len(valid_vms):
                    print("Invalid instance index.")
                    continue
                vm_name = valid_vms[instance_index]
                status = instance_statuses[vm_name]
            except ValueError:
                print("Invalid instance index.")
                continue
        if choice == "1":
            if status == "stopped":
                manager.start_vm(vm_name)
                instance_statuses[vm_name] = "running"
                print(f"Started instance {vm_name}")
            else:
                print("Instance is already running.")
        elif choice == "2":
            if status == "running":
                manager.stop_vm(vm_name)
                instance_statuses[vm_name] = "stopped"
                print(f"Stopped instance {vm_name}")
            else:
                print("Instance is not running.")
        elif choice == "3":
            if status == "running":
                manager.restart_vm(vm_name)
                print(f"Restarted instance {vm_name}")
            else:
                print("Instance is not running.")
        elif choice == "4":
            instance_statuses = manager.get_all_vms_status()
            manager.print_vm_table(instance_statuses)
        elif choice == "5":
            print("Exiting LDPlayer Dashboard...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

# C:\LDPlayer\LDPlayer9\dnconsole.exe adb --name "Cucaracha" --command root
# C:\LDPlayer\LDPlayer9\dnconsole.exe adb --name "Cucaracha" --command shell

# def ChangeProxy(self, deviceID, proxy):
    # return self.ExecuteCMD("adb -s {0} shell settings put global http_proxy {1}".format(deviceID,proxy))

