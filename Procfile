web: gunicorn proxy_manager_web.wsgi --log-file -
worker: celery worker --app=proxy_manager_web --loglevel=info
heroku ps:scale worker=1
