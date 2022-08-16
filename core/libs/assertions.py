from .exceptions import FyleError
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError

def base_assert(error_code, msg):
    raise FyleError(status_code=error_code, message=msg)

def validation_assert(msg):
    raise ValidationError(message=msg)

    
def assert_enum(_obj, msg="Invalid Grade"):
    if _obj not in ["A","B","C", "D" ]:
        validation_assert(msg=msg)


def assert_auth(cond, msg='UNAUTHORIZED'):
    if cond is False:
        base_assert(401, msg)


def assert_true(cond, msg='FORBIDDEN'):
    if cond is False:
        base_assert(403, msg)


def assert_valid(cond, msg='BAD_REQUEST'):
    if cond is False:
        base_assert(400, msg)


def assert_found(_obj, msg='NOT_FOUND'):
    if _obj is None:
        base_assert(404, msg)
