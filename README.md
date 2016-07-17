PokeLocator
===========

Sign up for a poke club account here (that where the PTC_USERNAME and PTC_PASSWORD come from):
https://club.pokemon.com/us/pokemon-trainer-club/sign-up/

Also can sign up for a google account to use as a fallback for when poke club authentication is down (frequently happens), and input those into GOOG_USERNAME and GOOG_PASSWORD

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

##### TO SETUP LOCALLY
```
- Install heroku toolbelt (https://toolbelt.heroku.com/)
- Install git
- Install python 2.7.6
- Install pip (e.g. sudo easy_install pip)
```

```
<clone our app to a local git repository>
$ sudo pip install -r requirements.txt
$ heroku apps:create pokelocator-demo
$ heroku config:set IS_HEROKU_SERVER=1
$ heroku config:set PTC_USERNAME=my_pokeclub_username
$ heroku config:set PTC_PASSWORD=my_pokeclub_password
$ heroku config:set GOOG_USERNAME=my_google_username
$ heroku config:set GOOG_PASSWORD=my_google_password
$ git push heroku master
```

##### Run Server Locally
```
$ python manage.py runserver
Visit http://127.0.0.1:8000/static/index.html
```

Pokelocator api from:
https://github.com/leegao/pokemongo-api-demo/tree/simulation

TODO
- Add google auth (automatically fail over to it if poke club auth failed)
- cache auth token somewhere