web: gunicorn config.wsgi:application
worker: celery worker --app=jd-ph-cms.taskapp --loglevel=info
