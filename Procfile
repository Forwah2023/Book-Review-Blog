web: gunicorn book_review_project.wsgi  --log-file -
release: python manage.py migrate
release: python manage.py collectstatic --noinput

