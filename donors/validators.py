import re
from donors.exceptions import InvalidPhoneError, InvalidEmailError, InvalidBloodGroupError

PHONE_REGEX = re.compile(r'^(?:\+91|0)?[6-9]\d{9}$')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

BLOOD_GROUP_REGEX = re.compile(r'^(A|B|AB|O)[+-]$')


def validate_phone(phone: str) -> str:
    phone = phone.strip().replace(' ', '').replace('-', '')
    if not PHONE_REGEX.match(phone):
        raise InvalidPhoneError(phone)
    return phone


def validate_email(email: str) -> str:
    email = email.strip()
    if not EMAIL_REGEX.match(email):
        raise InvalidEmailError(email)
    return email.lower()


def validate_blood_group(group: str) -> str:
    group = group.strip().upper()
    if not BLOOD_GROUP_REGEX.match(group):
        raise InvalidBloodGroupError(group)
    return group