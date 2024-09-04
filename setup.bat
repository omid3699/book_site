echo off
cd C:\Users\sun\Desktop\book_site
echo "checking for updates"

git pull

echo "installing depencies"
pip install -r requirements.txt

python manage.py migrate