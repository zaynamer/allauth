from django_multitenant.utils import set_current_tenant, unset_current_tenant
from api.utils import get_user_account

class MultitenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user and not request.user.is_anonymous:
            set_current_tenant(get_user_account(request))

        # Call the view
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        """
        The following unsetting of the tenant is essential because of how webservers work
        Since the tenant is set as a thread local, the thread is not killed after the request is processed
        So after processing of the request, we need to ensure that the tenant is unset
        Especially required if you have public users accessing the site 
        
        This is also essential if you have admin users not related to a tenant (not possible in actual citus env)
        """
        unset_current_tenant()

        return response
    