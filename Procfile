release: sh -c 'cd innosoft_api && python manage.py setup'
web: sh -c 'cd innosoft_api && gunicorn innosoft_api.wsgi --log-file -'