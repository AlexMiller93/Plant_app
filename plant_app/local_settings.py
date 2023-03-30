# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

from plant_app.settings import BASE_DIR

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

'''
MySQL settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'plant_app', 
        'USER': 'root',
        'PASSWORD': 'VtC$Az@khsD6V@!H4THN',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {  
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  
        } 
    }
}
'''