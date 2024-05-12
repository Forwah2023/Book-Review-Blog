release: python manage.py migrate
release: python manage.py collectstatic --noinput
web: gunicorn Book_Review_Project.wsgi  --log-file -
