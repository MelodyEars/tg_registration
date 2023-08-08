class ProjectException(Exception):
    """Generic exception that all other YouTube errors are children of."""

    def __init__(self, *args):
        self.message = args[0] if args else None
        super().__init__(self.message)

    def __str__(self):
        return f'Project -> {self.message}'


class TgRegerAppiumException(ProjectException):
    """ This Base Exception for Tg registration """

    def __str__(self):
        return f'Appium Tg registration -> {self.message}'



class SmsActivateException(ProjectException):
    """ This Base Exception for smsActivate """

    def __str__(self):
        return f'for smsActivate -> {self.message}'
