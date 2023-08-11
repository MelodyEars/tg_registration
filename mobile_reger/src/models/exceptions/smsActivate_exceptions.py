from .base_execeptions import SmsActivateException


class NoCodeSentException(SmsActivateException):
    """Telegram not send code to smsActivate"""