emulator_path = r'C:\Users\King\AppData\Local\Android\Sdk\tools\emulator.exe'
api_32 = r'C:\Users\King\AppData\Local\Android\Sdk\system-images\android-32\google_apis\x86_64'
skin = r'C:\Users\King\AppData\Local\Android\Sdk\skins\pixel_6_pro'
proxy = 'username:password@server:port'
port = '5556'  # від 5554 до 5682
memory = '2048'
timezone = 'Europe/Paris'
no_window = '-no-window'

# example: '/Users/janedoe/Library/Android/sdk/emulator/emulator -avd Nexus_5X_API_23 -netdelay none -netspeed full'
my_cmd = f'''{emulator_path} -avd  TEST_VM_API_32 -no-snapshot-save -memory {memory} -debug all -show-kernel 
             -http-proxy {proxy} -netdelay none -netspeed full -port {port} -accel auto --timezone {timezone}
              -no-boot-anim -screen multi-touch '''

avdmanager = r'C:\Users\King\AppData\Local\Android\Sdk\cmdline-tools\latest\bin\avdmanager.bat'
name_avd = 'TEST_VM_API_32'
cmd = {'create': f'{avdmanager} create avd -n {name_avd} -k "system-images;android-32;google_apis;x86_64"',
 'delete': 'delete avd -n name'}

print(cmd['create'])

delete_cmd = f'{avdmanager} delete avd -n {name_avd}'

