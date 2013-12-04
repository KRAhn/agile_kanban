class AcurosCustomError(Exception):
    pass


class IntegrityError(AcurosCustomError):
    pass


class NoParameterError(AcurosCustomError):
    pass


class InvalidParameterError(AcurosCustomError):
    pass


class UnsupportedMethodError(AcurosCustomError):
    pass


class PermissionDeniedError(AcurosCustomError):
    pass


class DBError(AcurosCustomError):
    pass


class NoLoginError(AcurosCustomError):
    pass
