# Div-Systems-Task

this project built using django and rest framework
and using 3rd party packages like

- django-countries-plus
- django-corsheaders
- restframework-simplejwt
- django-admin-interface

### Get started

- first clone the app
- run cd div-systems-assessment
- run pipenv shell & pipenv install
- or run pip install requirements.txt
- run python manage.py migrate
- run python manage.py update_countries_plus
- run python manage.py run server

## test the end points

- send post request to /signup/
- send post request to /login/ with phone and password to get tokens
- send a get request to /status/ with header authorization => 'Bearer + your access_token'
