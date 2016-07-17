PokeLocator
===========

- Sign up for a poke club account [HERE](https://club.pokemon.com/us/pokemon-trainer-club/sign-up/). Input your username/password into the environment variables PTC_USERNAME and PTC_PASSWORD.

- [Optional] Sign up for a google account as well to use as a fallback for when poke club authentication is down (frequently happens). Input this username/password into the environment variables GOOG_USERNAME and GOOG_PASSWORD.

### Setup on Heroku with button deploy

- Click the DEPLOY Heroku button below to build the app in the cloud for free (requires Heroku account).

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

### Setup on Heroku manually
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

Now visit your heroku app url in the browser. You must use `https://` instead of `http://` to allow location tracking (modern browsers block it if not https).

### Setup locally
```
- Install git
- Install python 2.7.6
- Install pip (e.g. sudo easy_install pip)
```

Setup environmental variables (google how to do it for your system):
```
PTC_USERNAME=my_pokeclub_username
PTC_PASSWORD=my_pokeclub_password
GOOG_USERNAME=my_google_username
GOOG_PASSWORD=my_google_password
```

```
$ sudo pip install -r requirements.txt
$ python manage.py runserver
Visit http://127.0.0.1:8000/
```

### Notes
- Note that you will need to view the "https" and not "http" version of your herokuapp for most browsers to allow the code to request your location.
- Get an email from gmail saying someone attempted to login to your account from virginia (or wherever)? That would be this app. If you deployed to heroku, then your heroku cloud instance IS logging into your gmail account. You are not getting hacked, if you are worried you can review the code [here](https://github.com/emeth-/pokelocater/blob/master/api/pokelocator_api.py#L167), please don't send me threats.

Pokelocator api from:
https://github.com/leegao/pokemongo-api-demo/tree/simulation
