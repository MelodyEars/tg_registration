from loguru import logger

from mobile_reger.src.models import convert_tgnet_to_session
from mobile_reger.src.models import get_TgnetDat_fromAndroid


@logger.catch
def main():
    path_save = get_TgnetDat_fromAndroid()
    convert_tgnet_to_session(path_save)


if __name__ == '__main__':
    main()
