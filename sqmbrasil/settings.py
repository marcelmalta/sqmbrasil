from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# Segurança
# =========================
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
DEBUG = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# =========================
# Apps instalados
# =========================
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Sites (necessário para allauth)
    "django.contrib.sites",

    # Seu app
    "core",

    # Estilização de formulários
    "crispy_forms",
    "crispy_tailwind",

    # Widget tweaks para add_class nos templates
    "widget_tweaks",

    # django-allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",  # opcional

    # Storage externo (R2/S3)
    "storages",
]

SITE_ID = 1

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# =========================
# Middlewares
# =========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serve estáticos no Render
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # obrigatório para allauth
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sqmbrasil.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # pasta global
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # necessário p/ allauth
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "sqmbrasil.wsgi.application"

# =========================
# Banco de dados
# =========================
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
    )
}

# =========================
# Validação de senha
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =========================
# Internacionalização
# =========================
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# =========================
# Arquivos estáticos
# =========================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"  # usado no deploy (collectstatic)

# =========================
# Arquivos de mídia (Cloudflare R2 / local)
# =========================
USE_S3 = os.environ.get("USE_S3") == "True"

STORAGES = {
    # Arquivos estáticos (admin, CSS, JS)
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    # Arquivos de mídia (uploads de usuário)
    "default": {
        "BACKEND": (
            "storages.backends.s3boto3.S3Boto3Storage"
            if USE_S3
            else "django.core.files.storage.FileSystemStorage"
        ),
    },
}

if USE_S3:
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL")
    AWS_S3_SIGNATURE_VERSION = "s3v4"  # obrigatório no Cloudflare R2
    MEDIA_URL = "https://media.sqmbrasil.com.br/"
else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

# =========================
# Autenticação (allauth)
# =========================
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# =========================
# Configuração de e-mail
# =========================
if DEBUG:
    # Desenvolvimento: imprime e-mail no console
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    # Produção: SendGrid
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.sendgrid.net"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = "apikey"  # literal
    EMAIL_HOST_PASSWORD = os.environ.get("SENDGRID_API_KEY")
    DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "adminntato@sqmbrasil.com.br")

# =========================
# Padrão para chaves primárias
# =========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
