from django.conf import settings
from django.http import HttpResponseForbidden
from common.scripts import RequestUtil, print_color

class AdminProtect:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        url = request.get_full_path()
        
        if settings.ADMIN_PATH in url and not settings.DEBUG:

            ip = RequestUtil.get_ip(self, request)

            # Remove the port from the allowed IPs
            allowed_ips = [ip.split(':')[0] for ip in settings.ALLOWED_IP_ADMIN]

            if ip not in allowed_ips:
                return HttpResponseForbidden()

        if settings.ADMIN_PATH in url and settings.DEBUG:
            ip = RequestUtil.get_ip(self, request)
            print(settings.ALLOWED_IP_ADMIN)
            print_color('*'*10 + '[this print config.admin_protect.AdminProtect line:28]' + '*'*10, 4)
            print_color(f'* config.admin_protect.AdominProtect DEBUG CODE [admin access]: {ip}'   , 4)

            # Remove the port from the allowed IPs
            allowed_ips = [ip.split(':')[0] for ip in settings.ALLOWED_IP_ADMIN]

            if ip not in allowed_ips:
                return HttpResponseForbidden()

        response = self.get_response(request)

        return response