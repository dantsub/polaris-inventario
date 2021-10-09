import re
from validate_email import validate_email

pass_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$"
# Esta expresión de password indica que el debe tener mínimo 8 caracteres, una mayúscula, una minuscula, un número y un caracter:@$!%*?&.
user_regex = "^[a-zA-Z0-9_.-]+$"
# ^ matches the beginning of the string
# $ matches the end of the string
# + means the previous expression matches once or more
# Esta expresión de user indica que el nombre de usuario solo puede tener letras may o min, números y estos tres caracter: ._-

F_ACTIVE = 'ACTIVE'
F_INACTIVE = 'INACTIVE'
EMAIL_APP = 'EMAIL_APP'
REQ_ACTIVATE = 'REQ_ACTIVATE'
REQ_FORGOT = 'REQ_FORGOT'
U_UNCONFIRMED = 'UNCONFIRMED'
U_CONFIRMED = 'CONFIRMED'

def isEmailValid(email):
    is_valid = validate_email(email)

    return is_valid

def isUsernameValid(user):
    if re.search(user_regex, user):
        return True
    else:
        return False

def isPasswordValid(password):
    if re.search(pass_regex, password):
        return True
    else:
        return False