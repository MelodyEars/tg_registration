from faker import Faker
from loguru import logger

from mobile_reger.src.models.sms_activate import InfoNumberPhone


def gen_personality(dict_info_PhoneNumber: InfoNumberPhone) -> tuple[str, str]:
    logger.info('personality is being generated')

    country = dict_info_PhoneNumber["language"] + "_" + dict_info_PhoneNumber["abbreviated_country"]
    logger.info(country)
    fake = Faker(country)
    first_name = fake.first_name()
    last_name = fake.last_name()

    print(f"и нарекли его {first_name}, а фамилия его бьіла {last_name}")

    return first_name, last_name
