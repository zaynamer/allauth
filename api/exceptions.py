from rest_framework.exceptions import APIException

class TenancyException(APIException):
    status_code = 403
    default_detail = 'Authorization error. Tenancy is invalid. Ensure User has a valid Account or is superuser.'
    default_code = 'tenancy_invalid'

class AuthorizationException(APIException):
    status_code = 403
    default_detail = 'Authorization error.'
    default_code = 'unauthorized'