from unittest import TestCase, main

from mobile_reger.src.models.decode_tgnet_dat import convert_tgnet_to_session


class TestConverterSession(TestCase):
    def test_converter_session(self):
        file = r'C:\Users\King\PycharmProjects\tg_registration\mobile_reger\output_files\tgnets\380500555555.dat'
        self.assertEquals(convert_tgnet_to_session(file), None)


if __name__ == '__main__':
    main()

r'adb pull /data/data/org.telegram.messenger.web/files/tgnet.dat C:\Users\King\PycharmProjects\tg_registration\mobile_reger\output_files\tgnets\380500555555.dat'