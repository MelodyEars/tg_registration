import contextlib
import re
import subprocess

from loguru import logger

from mobile_reger.src.models.vm_manager.pyavd import pyavd

# emulator_path = r'C:\Users\King\AppData\Local\Android\Sdk\tools\emulator.exe'
# avdmanager = r'C:\Users\King\AppData\Local\Android\Sdk\cmdline-tools\latest\bin\avdmanager.bat'
# api_32 = r'C:\Users\King\AppData\Local\Android\Sdk\system-images\android-32\google_apis\x86_64'
# skin = r'C:\Users\King\AppData\Local\Android\Sdk\skins\pixel_6_pro'
proxy = '-http-proxy ' + 'username:password@server:port'





# example: '/Users/janedoe/Library/Android/sdk/emulator/emulator -avd Nexus_5X_API_23 -netdelay none -netspeed full'
# my_cmd = f'''{emulator_path} -avd  TEST_VM_API_32 -no-snapshot-save -memory {memory} -debug all -show-kernel
#              -http-proxy {proxy} -netdelay none -netspeed full -port {port} -accel auto --timezone {timezone}
#               -no-boot-anim -screen multi-touch '''

# avdmanager = r'C:\Users\King\AppData\Local\Android\Sdk\cmdline-tools\latest\bin\avdmanager.bat'
# name_avd = 'TEST_A'
# cmd = {'create': f'{avdmanager} create avd -n {name_avd} -k "system-images;android-32;google_apis;x86_64"',
#        'delete': f'{avdmanager} delete avd -n {name_avd}'}

# delete_cmd = f'{avdmanager} delete avd -n {name_avd}'

memory = '2048'
no_window = False  # a window appeared


@contextlib.contextmanager
def vm_manager(name_avd, vm_proxy=None, timezone='Europe/Paris', vm_port='5554'):
	custom_config = (
		' -no-snapshot-save'
		f' -memory {memory}'
		' -netdelay none'
		' -netspeed full'
		f' -port {vm_port}'  # від 5554 до 5682
		' -accel auto'
		f' -timezone {timezone}'
		' -no-boot-anim'
		' -screen multi-touch'
	)
	if vm_proxy:
		custom_config += f" -http-proxy {vm_proxy}"

	if no_window:
		custom_config += ' -no-window'

	create_param = {
		'name': name_avd,
		'device': pyavd.get_devices()[32],  # Pixel 6 Pro
		'package': "system-images;android-32;google_apis;x86_64",
		# 'skin': skin,
		'force': True,
	}

	logger.debug("creating avd")
	avd = pyavd.create_avd(**create_param)

	logger.debug("starting avd")
	p = avd.start(detach=True, config=custom_config)
	logger.debug("waiting for avd")
	try:
		yield vm_port
	finally:
		logger.debug("stopping avd")
		avd.stop(port=vm_port)
		logger.debug("deleting avd")
		avd.delete()
		logger.debug("done")


if __name__ == '__main__':
	with vm_manager('TEST_A') as port:
		print(port)
		input("Press Enter to exit")


