import os
import subprocess
import time

from loguru import logger

ldconsole = r'C:\LDPlayer\LDPlayer9\ldconsole.exe'
dnconsole = r'C:\LDPlayer\LDPlayer9\dnconsole.exe'
dnplayer = r'C:\LDPlayer\LDPlayer9\dnplayer.exe'


def _cmd_exec(cmd):
    result = subprocess.run([ldconsole, cmd], capture_output=True, text=True)
    return result.stdout


def execute_command(cmd: str, run_and_forgate=False):
    if run_and_forgate:
        os.system(dnconsole + " " + cmd)
    else:
        out = _cmd_exec(cmd)
        print(out)
        return out


def execute_cmd_for_result(path_exe: str, cmd: str, timeout=10000, retry=2):
    try:
        process = subprocess.Popen([path_exe, cmd],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE,
                                   shell=True,
                                   text=True)

        while retry >= 0:
            retry -= 1
            process.poll()

            if process.returncode is None:
                process.kill()
            else:
                break

        text = process.communicate(timeout=timeout)[0]
        result = text

    except Exception as e:
        logger.error(e)
        result = None

    return result


class LDPlayer:

    def __init__(self, name):
        self.name = name

    def open(self):
        logger.info(f"Opening LDPlayer")
        cmd = f"launch --name {self.name}"
        execute_command(cmd, run_and_forgate=True)

        logger.debug("isrunning")
        cmd = f"isrunning --name {self.name}"

        execute_command(cmd)

    def create(self):
        logger.info(f"Creating LDPlayer")
        cmd = f"add --name {self.name}"
        execute_command(cmd, run_and_forgate=True)

    # def watch_list(self):
        # logger.info(f"runninglist")
        # cmd = f"runninglist"
        # execute_command(cmd, run_and_forgate=True)
        #
        # logger.info(f"list")
        # cmd = f"list"
        # execute_command(cmd)

    def close_vm(self):
        logger.info(f"Closing LDPlayer")
        cmd = f"quit --name {self.name}"
        execute_command(cmd, run_and_forgate=True)

    def remove_vm(self):
        logger.info(f"Remove VM {self.name}")
        cmd = f"remove --name {self.name}"
        execute_command(cmd, run_and_forgate=True)

    def list_instances(self):
        cmd = ["list2"]
        result = subprocess.run([dnconsole] + cmd, capture_output=True, text=True)
        instances = [line.split(",")[1] for line in result.stdout.splitlines()[1:] if line]
        logger.debug(f"list_instances output: {result.stdout}")  # debug print
        logger.debug(f"list_instances output: {instances}")
        return instances

    def get_all_instances_status(self):
        name = ''

        cmd = ['list2']
        result = subprocess.run([dnconsole] + cmd, capture_output=True, text=True)
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

        logger.debug(f"list_instances output: {instances}")
        return instances

    def print_instance_table(self, instance_statuses, status_filter=None):
        print("\nInstance Dashboard:")
        print("ID".ljust(5), "Instance Name".ljust(30), "Status")
        running_instances = []
        stopped_instances = []
        unknown_instances = []
        for instance, status in instance_statuses.items():
            if status == "running":
                running_instances.append(instance)
            elif status == "stopped":
                stopped_instances.append(instance)
            else:
                unknown_instances.append(instance)
        if status_filter == "running":
            instances = running_instances
        elif status_filter == "stopped":
            instances = stopped_instances
        else:
            instances = running_instances + stopped_instances + unknown_instances
        for idx, instance in enumerate(instances, start=1):
            status = instance_statuses[instance]
            print(str(idx).ljust(5), instance.ljust(30), status)
        print("\nSummary:")
        print(f"{len(running_instances)} instances running")
        print(f"{len(stopped_instances)} instances stopped")
        print(f"{len(unknown_instances)} instances in an unknown state")


if __name__ == '__main__':
    ld = LDPlayer("Cucaracha")
    ld.open()
    time.sleep(10)
    logger.debug("IES")
    ld.list_instances()
    instances = ld.get_all_instances_status()
    ld.print_instance_table(instances)
    ld.close_vm()
