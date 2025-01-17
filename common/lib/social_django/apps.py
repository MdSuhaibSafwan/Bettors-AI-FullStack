from django.apps import AppConfig


class PythonSocialAuthConfig(AppConfig):
    # Explicitly set default auto field type to avoid migrations in Django 3.2+
    default_auto_field = "django.db.models.BigAutoField"
    # Full Python path to the application eg. 'django.contrib.admin'.
    name = "common.lib.social_django"
    # Last component of the Python path to the application eg. 'admin'.
    label = "social_django"
    # Human-readable name for the application eg. "Admin".
    verbose_name = "Social_Login"
