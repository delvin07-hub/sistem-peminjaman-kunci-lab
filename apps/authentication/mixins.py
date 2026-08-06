from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Hanya superuser yang boleh mengakses halaman web ini."""

    raise_exception = True

    def test_func(self):
        return self.request.user.is_superuser


def admin_required(view_func):
    """Hanya superuser yang boleh mengakses fungsi view ini."""

    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden(
                'Hanya admin yang dapat mengakses halaman ini.'
            )
        return view_func(request, *args, **kwargs)

    return wrapper
