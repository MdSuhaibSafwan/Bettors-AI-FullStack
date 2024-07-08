import os
import environ
from django.conf import settings

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))

STRIPE_PUBLISHABLE_KEY = env.get_value("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = env.get_value("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = env.get_value("STRIPE_WEBHOOK_SECRET")
