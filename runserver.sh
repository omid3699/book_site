cd /home/ict/book_site

source .venv/bin/activate

gunicorn --workers 3 --bind unix:/home/ict/book_site/gunicorn.sock core.wsgi:application