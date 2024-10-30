cd /home/ict/book_site

git pull

python manage.py migrate

python manage.py collectstatic --noinput

cp book_site.conf /etc/nginx/conf.d/book_site.conf

