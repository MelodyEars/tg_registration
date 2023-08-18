"""
Telegram android session auth key scrapper

This is a code that scrap all data (auth_key, datacenter_id etc.) from tgnet.dat file
tgnet.dat is telegram's session file on android

There are 4 locations of this file:
/data/data/org.telegram.messenger.web/files/tgnet.dat
/data/data/org.telegram.messenger.web/files/account1/tgnet.dat
/data/data/org.telegram.messenger.web/files/account2/tgnet.dat
/data/data/org.telegram.messenger.web/files/account3/tgnet.dat

Creator https://github.com/batreller/
Code https://github.com/batreller/telegram_android_session_converter
"""
from mobile_reger.src.models.decode_tgnet_dat.telegram_android_session_converter.BufferWrapper import BufferWrapper


def convert_tgnet_to_session(tgnet_path: str) -> None:
    # tgnet_path = 'tgnets/tgnet.dat'

    with open(tgnet_path, 'rb') as f:
        buffer = BufferWrapper(f.read())

    tgdata = buffer.get_tg_android_session()
    valid_session = tgdata.datacenters[tgdata.headers.currentDatacenterId-1]
    print('auth key:', valid_session.auth.authKeyPerm)
    print('telethon string session:', valid_session.telethon_string_session)
    print(valid_session)


if __name__ == '__main__':
    file = r'C:\Users\King\PycharmProjects\tg_registration\mobile_reger\output_files\tgnets\380500555555.dat'
    convert_tgnet_to_session(file)
