# Div-Systems-Task

### Get started

- first clone the app
- run pipenv install
- run python manage.py migrate
- run python manage.py update_countries_plus
- run python manage.py run server

## test the end points

- send post request to /signup/
- send post request to /login/ with phone and password to get tokens
- send a get request to /status/ with header authorization => 'Bearer + your access_token'
