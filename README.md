Hackathon-kit
===========

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

##### SETUP
```
- Install heroku toolbelt (https://toolbelt.heroku.com/)
- Install git
- Install python 2.7.6
- Install pip (e.g. sudo easy_install pip)
```

```
<clone our app to a local git repository>
$ sudo pip install -r requirements.txt
$ heroku apps:create hackathon-demo 
$ heroku config:set PTC_USERNAME=my_pokeclub_username
$ heroku config:set PTC_PASSWORD=my_pokeclub_password
$ git push heroku master
```

##### Migrations
Create new migrations
```
$ python manage.py makemigrations
```

Run migrations
```
$ python manage.py migrate
```

##### Run Server
```
$ python manage.py runserver
Visit http://127.0.0.1:8000/static/index.html
```

##### Admin Panel
Create a superuser
```
$ python manage.py createsuperuser
Visit http://127.0.0.1:8000/admin/
```

Sign up for a poke club account here (that where the PTC_USERNAME and PTC_PASSWORD come from):
https://club.pokemon.com/us/pokemon-trainer-club/sign-up/