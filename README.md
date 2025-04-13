# To access API Please Use Postman 

django-admin startproject myproject
cd myproject
python manage.py startapp users


# settings.py
INSTALLED_APPS = [
    'users',
]
# I am using in built Abstract USer in my model here..

## Tell django that i am overriding and using User Role..
    AUTH_USER_MODEL = 'users.CustomUser'


# Write Serilaier and Views and add urls in setting for user creation.



