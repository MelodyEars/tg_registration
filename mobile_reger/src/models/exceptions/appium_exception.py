from .base_execeptions import TgRegerAppiumException


class SendPhoneNumberException(TgRegerAppiumException):
    """
     After send the number of phone, get Error as
     'Ошибка: Слишком много запросов. Попробуйте снова через 4 часа. Вы можете сообщить нам о проблеме.'
     """


class NoCodeSentException(TgRegerAppiumException):
    """Telegram not send code to smsActivate"""


class BannedPhoneNumberException(TgRegerAppiumException):
    """This phone number is banned."""
