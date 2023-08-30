import logging
from .account.models import Account
from api.exceptions import TenancyException

logger = logging.getLogger()

def tenant_func(request):
    """
    The tenant is the account this user is associated with. 
    If it is not set, tenancy will not be applied. 
    We raise an exception here if the user is not staff
    and tenant is not set.
    """
    tenant=get_user_account(request)
    if not tenant and not request.user.is_staff:
        raise TenancyException()
    logger.debug(f"TENANT SET INTO THREAD: {tenant}")
    return tenant

def get_user_account(request):
    """
    Helper function to get user account for the logged-in user
    """
    try:
        account=None
        accounts=Account.objects.all().filter(users=request.user)
        # First, look in the user's record for the active account
        if request.user.active_account_id:
            account = accounts.get(id=request.user.active_account_id)
        if not account:
            # If no active account is found, set the tenant to the first one found in the M2M relationship
            account = accounts.first()
        return account
    except Exception:
        logger.warn(f"Unable to find account for username: {request.user}")
    