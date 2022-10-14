from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re


class PasswordRuleValidator:
    def __init__(self, regex=r"^(?=.*[A-Za-z가-힣])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z가-힣\d$@$!%*#?&]{8,}$"):
        self.regex = regex

    def validate(self, password, user=None):
        if not re.fullmatch(self.regex, password):
            raise ValidationError(
                _("비밀번호는 8자 이상이어야 하며 하나 이상의 문자, 숫자, 특수문자를 포함해야 합니다."),
                code='invalid_password',
            )

    def get_help_text(self):
        return _("비밀번호는 8자 이상이어야 하며 하나 이상의 문자, 숫자, 특수문자를 포함해야 합니다.")
