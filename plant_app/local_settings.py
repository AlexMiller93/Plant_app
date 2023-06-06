# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

from plant_app.settings import BASE_DIR

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

