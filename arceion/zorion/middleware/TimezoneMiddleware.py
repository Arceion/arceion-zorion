try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # We assume the user modle has a timezone field
            # If not, we fall back to the default (Asia/Colombo as per requirements)
            tzname = getattr(request.user, 'timezone', 'Asia/Colombo')
            if tzname:
                try:
                    timezone.activate(ZoneInfo(tzname))
                except Exception:
                    timezone.deactivate()
            else:
                timezone.deactivate()
        else:
            timezone.deactivate()

        return self.get_response(request)
