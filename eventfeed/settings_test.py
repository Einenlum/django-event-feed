from .settings import *

CELERY_ALWAYS_EAGER = True
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "temp/emails")
