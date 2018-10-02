web: gunicorn proxy_manager_web.wsgi --log-file -
main_worker: python manage.py proxy_manager_web worker --beat --without-gossip --without-mingle --without-heartbeat --loglevel=info