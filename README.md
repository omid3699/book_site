# پروژه وبسایت دانلود کتاب با جنگو

## clone the project
```sh
git clone https://github.com/omid3699/book_site.git
```

## go to project dirctory
```sh
cd book_site
```
## create and activate virtualenv
```sh
virttalenv .venv
# in linux
source .venv/bin/activate
# in windows
.venv\scripts\activate
```
## migrate the database
```sh
python manage.py migrate
```

## run development server
```sh
python mange.py runserver
```


