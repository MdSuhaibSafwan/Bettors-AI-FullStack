# Referrer
# https://qiita.com/kin292929/items/92aa0f6f5e1fbca553ee
# https://qiita.com/kenkono/items/d95aee6e79f671c67aba
import os
import environ
from django.conf import settings
from django.core.cache import cache
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin
import subprocess
import time
from apps.access_security.models import BlockIpList, AccessSecurity
from common.scripts import RequestUtil, print_color

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, ".env"))

# Measure access within a certain period and block if exceeded
ACCESS_COUNT_SECONDS_TIME = env.get_value(
    "ACCESS_COUNT_SECONDS_TIME", int
)  # Duration in seconds for measuring access (seconds)
N_TIMES_TO_BLOCK_ACCESS = env.get_value(
    "N_TIMES_TO_BLOCK_ACCESS", int
)  # Number of times to block access within the specified duration
N_TIMES_TO_ADD_BLOCKLIST = env.get_value(
    "N_TIMES_TO_ADD_BLOCKLIST", int
)  # Number of times to add to the blocklist within the specified period
BLOCKLIST_EFFECTIVE_DAYS = env.get_value(
    "BLOCKLIST_EFFECTIVE_DAYS", int
)  # Effective duration of the blocklist (days)

# Block access from registered block IP addresses
REGISTERED_BLOCK_IP_LIST_READ_FREC = env.get_value(
    "REGISTERED_BLOCK_IP_LIST_READ_FREC", int
)  # Time interval (in minutes) for re-reading the database

# Lists of IP addresses for different access control purposes
PASS_IP_LIST = "pass_ip_list"  # List of IP addresses allowed to pass
BLOCK_IP_LIST = "block_ip_list"  # List of IP addresses to be blocked
CONTROL_IP_LIST = "control_ip_list"  # Control list for IP addresses

# Default settings for the control IP list
CONTROL_IP_LIST_DEFAULT = {
    PASS_IP_LIST: [],  # Initially, no IP addresses are allowed to pass
    BLOCK_IP_LIST: [],  # Initially, no IP addresses are blocked
}


class AccessSecurityMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        request_util = RequestUtil(request)
        ip = request_util.get_ip()

        # Block access based on registered block IP list▽
        if is_registered_block_ip(ip):
            AccessSecurity.objects.insert_access_log(request, "REGISTERED_IP_BLOCK")
            if settings.DEBUG:
                print_color(
                    "info: config.security.AccessSecurityMiddleware(line 46), REGISTERED_IP_BLOCK",
                    4,
                )
            raise Http404("Page not found")
        # Block access based on registered block IP list△

        # Block access based on excessive access within a certain period▽
        control_ip_list = cache.get(CONTROL_IP_LIST, CONTROL_IP_LIST_DEFAULT)

        # Pass IP list
        if ip in control_ip_list[PASS_IP_LIST]:
            return
        # Deny from blocklist
        if ip in control_ip_list[BLOCK_IP_LIST]:
            # Check the expiration for IPs in the blocklist
            if cache.get("block_ip_" + ip) is None:
                # Remove from blocklist if expired
                control_ip_list[BLOCK_IP_LIST].remove(ip)
                cache.set(CONTROL_IP_LIST, control_ip_list)
            else:
                # Log recording
                AccessSecurity.objects.insert_access_log(request, "IP_BLOCK")
                if settings.DEBUG:
                    print_color(
                        "info: config.security.AccessSecurityMiddleware(line 66), IP_BLOCK",
                        4,
                    )
                raise Http404("Page not found")

        ip_time_list = cache.get(ip, [])
        time_temp = time.time()

        # Remove cached records (updates) before the configured time
        while (
            ip_time_list and (time_temp - ip_time_list[-1]) > ACCESS_COUNT_SECONDS_TIME
        ):
            ip_time_list.pop()
        ip_time_list.insert(0, time_temp)
        cache.set(ip, ip_time_list, timeout=ACCESS_COUNT_SECONDS_TIME)

        # Add to blocklist
        if len(ip_time_list) > N_TIMES_TO_ADD_BLOCKLIST:
            control_ip_list[BLOCK_IP_LIST].append(ip)
            # Block the corresponding IP for the configured duration
            cache.set(
                CONTROL_IP_LIST,
                control_ip_list,
                timeout=60 * 60 * 24 * BLOCKLIST_EFFECTIVE_DAYS,
            )
            cache.set(
                "block_ip_" + ip, "", timeout=60 * 60 * 24 * BLOCKLIST_EFFECTIVE_DAYS
            )
            # Log recording
            AccessSecurity.objects.insert_access_log(request, "SET_BLOCK_IP")
            if settings.DEBUG:
                print_color(
                    "info: config.security.AccessSecurityMiddleware(line 87), SET_BLOCK_IP",
                    4,
                )

        # Access denied
        if len(ip_time_list) > N_TIMES_TO_BLOCK_ACCESS:
            if is_google_bot(ip):
                # Register Googlebot's IP in the pass list
                control_ip_list[PASS_IP_LIST].append(ip)
                cache.set(CONTROL_IP_LIST, control_ip_list, timeout=60 * 60 * 24 * 365)
                # Log recording (Register Googlebot's IP in the pass list: Uncomment if not needed)
                # AccessSecurity.objects.insert_access_log(request, 'SET_PASS_IP')
            else:
                # Log recording
                AccessSecurity.objects.insert_access_log(request, "COUNT_BLOCK")
                if settings.DEBUG:
                    print_color(
                        "info: config.security.AccessSecurityMiddleware(line 101), COUNT_BLOCK",
                        4,
                    )
                raise Http404("Page not found")
        # Block access based on excessive access within a certain period△


# Store the registered block IP list in cache
def is_registered_block_ip(ip) -> bool:
    # Retrieve IPs from the cache.
    registered_block_ips = cache.get("registered_block_ip_objs")

    # If not in the cache, fetch information from the database and store it.
    if registered_block_ips is None:
        registered_block_ips = list(BlockIpList.objects.all())
        cache.set(
            "registered_block_ip_objs",
            registered_block_ips,
            REGISTERED_BLOCK_IP_LIST_READ_FREC * 60,
        )

    registered_black_ip_list = [
        registered_block_ip.ip for registered_block_ip in registered_block_ips
    ]
    return ip in registered_black_ip_list


# Determine if it's Googlebot
def is_google_bot(ip):
    try:
        host = (
            subprocess.run(["host", ip], stdout=subprocess.PIPE)
            .stdout.decode()
            .replace("\n", "")
        )
        return host.endswith(("googlebot.com", "google.com"))
    except:
        return False
