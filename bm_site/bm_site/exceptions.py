from django.db import IntegrityError


class DuplicateKeyError(IntegrityError):
    pass


class RecordSaveError(IntegrityError):
    pass


class UnknownError(IntegrityError):
    pass
