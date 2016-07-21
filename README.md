PokeLocator
===========

![](http://teachthe.net/topclipbox/2016-07-19_03-12-450E0G3L.png)

The [stabile-mobile](https://github.com/emeth-/pokelocater/tree/stabile-mobile) branch has a stable version of the app, with a smaller scan radius around your immediate area that works great on mobile and heroku.

The master branch has the latest develop version, which may or may not be stabile. It will have a larger scan radius, but may not work on Heroku due to Heroku's 30 second timeouts.

### Things you will need

[Google Maps API Key](https://developers.google.com/maps/documentation/javascript/get-api-key#key)

[Pokemon Trainer Club Account](https://club.pokemon.com/us/pokemon-trainer-club/sign-up/) OR Google Account (a throwaway)

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
$ heroku config:set GMAPS_API_KEY=my_google_maps_api_key
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
GMAPS_API_KEY=my_google_maps_api_key
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
