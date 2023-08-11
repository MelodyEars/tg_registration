from pathlib import Path

from telethon.sync import TelegramClient
from telethon import functions


def get_tg_session_telethon_sync(phone_number: str, api_id: str, api_hash: str):
    # C:\Users\King\PycharmProjects\tg_registration\mobile_reger
    global_project_path = Path(__file__).parent.parent.parent.parent
    folder = global_project_path / 'output_files'
    folder.mkdir(exist_ok=True)
    name = str(folder / f"{phone_number}")
    with TelegramClient(name, int(api_id), api_hash) as client:
        print(client.get_me().username)



if __name__ == '__main__':
    project_path = Path(__file__).parent.parent.parent.parent
    print(project_path)
