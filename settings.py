INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django_path_converters'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase', # This is where you put the name of the db file.
                 # If one doesn't exist, it will be created at migration time.
    }
}