# B2CBackend

Here are the exact commands to run (inside your project root, where manage.py is located):

# 1. Make initial migrations 
python manage.py makemigrations 

# 2. Apply all migrations to the database
python manage.py migrate

# 3. Create superuser to log in admin panel
python manage.py createsuperuser


During createsuperuser, Django will ask for:

Username

Email (optional depending on settings)

Password

After that, you can start your dev server:

python manage.py runserver


Now open 👉 http://127.0.0.1:8000/admin
 and log in with your superuser credentials.
