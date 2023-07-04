from django.contrib.auth.decorators import user_passes_test
from django.urls import path

from botmanager.views import user_statistics


urlpatterns = [
    path('', user_passes_test(
        lambda u: u.is_superuser
    )(user_statistics), name='statistics'),
]
