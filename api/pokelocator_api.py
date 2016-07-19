# -*- coding: utf-8 -*-
import requests
import re
import struct
import json
import argparse
import pokemon_pb2
import time
import os
from collections import OrderedDict

from google.protobuf.internal import encoder

from datetime import datetime
from geopy.geocoders import GoogleV3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from s2sphere import *

def encode(cellid):
    output = []
    encoder._VarintEncoder()(output.append, cellid)
    return ''.join(output)

def getNeighbors():
    origin = CellId.from_lat_lng(LatLng.from_degrees(FLOAT_LAT, FLOAT_LONG)).parent(15)
    walk = [origin.id()]
    # 10 before and 10 after
    next = origin.next()
    prev = origin.prev()
    for i in range(10):
        walk.append(prev.id())
        walk.append(next.id())
        next = next.next()
        prev = prev.prev()
    return walk



API_URL = 'https://pgorelease.nianticlabs.com/plfe/rpc'
LOGIN_URL = 'https://sso.pokemon.com/sso/login?service=https%3A%2F%2Fsso.pokemon.com%2Fsso%2Foauth2.0%2FcallbackAuthorize'
LOGIN_OAUTH = 'https://sso.pokemon.com/sso/oauth2.0/accessToken'

SESSION = requests.session()
SESSION.headers.update({'User-Agent': 'Niantic App'})
SESSION.verify = False

DEBUG = False
COORDS_LATITUDE = 0
COORDS_LONGITUDE = 0
COORDS_ALTITUDE = 0
FLOAT_LAT = 0
FLOAT_LONG = 0

def f2i(float):
  return struct.unpack('<Q', struct.pack('<d', float))[0]

def f2h(float):
  return hex(struct.unpack('<Q', struct.pack('<d', float))[0])

def h2f(hex):
  return struct.unpack('<d', struct.pack('<Q', int(hex,16)))[0]

def set_location(location_name):
    geolocator = GoogleV3()
    loc = geolocator.geocode(location_name)

    print('[!] Your given location: {}'.format(loc.address.encode('utf-8')))
    print('[!] lat/long/alt: {} {} {}'.format(loc.latitude, loc.longitude, loc.altitude))
    set_location_coords(loc.latitude, loc.longitude, loc.altitude)

def set_location_coords(lat, long, alt):
    global COORDS_LATITUDE, COORDS_LONGITUDE, COORDS_ALTITUDE
    global FLOAT_LAT, FLOAT_LONG
    FLOAT_LAT = lat
    FLOAT_LONG = long
    COORDS_LATITUDE = f2i(lat) # 0x4042bd7c00000000 # f2i(lat)
    COORDS_LONGITUDE = f2i(long) # 0xc05e8aae40000000 #f2i(long)
    COORDS_ALTITUDE = f2i(alt)

def get_location_coords():
    return (COORDS_LATITUDE, COORDS_LONGITUDE, COORDS_ALTITUDE)

def api_req(login_type, api_endpoint, access_token, *mehs, **kw):
    try:
        p_req = pokemon_pb2.RequestEnvelop()
        p_req.rpc_id = 1469378659230941192

        p_req.unknown1 = 2

        p_req.latitude, p_req.longitude, p_req.altitude = get_location_coords()

        p_req.unknown12 = 989

        if 'useauth' not in kw or not kw['useauth']:
            print "api_req: login_type", login_type
            p_req.auth.provider = login_type
            p_req.auth.token.contents = access_token
            p_req.auth.token.unknown13 = 14
        else:
            p_req.unknown11.unknown71 = kw['useauth'].unknown71
            p_req.unknown11.unknown72 = kw['useauth'].unknown72
            p_req.unknown11.unknown73 = kw['useauth'].unknown73

        for meh in mehs:
            p_req.MergeFrom(meh)

        protobuf = p_req.SerializeToString()

        r = SESSION.post(api_endpoint, data=protobuf, verify=False)

        p_ret = pokemon_pb2.ResponseEnvelop()
        p_ret.ParseFromString(r.content)

        if DEBUG:
            print("REQUEST:")
            print(p_req)
            print("Response:")
            print(p_ret)
            print("\n\n")

        print("Sleeping for 2 seconds to get around rate-limit.")
        time.sleep(2)
        return p_ret
    except Exception, e:
        if DEBUG:
            print(e)
        return None

def get_profile(login_type, access_token, api, useauth, *reqq):
    req = pokemon_pb2.RequestEnvelop()

    req1 = req.requests.add()
    req1.type = 2
    if len(reqq) >= 1:
        req1.MergeFrom(reqq[0])

    req2 = req.requests.add()
    req2.type = 126
    if len(reqq) >= 2:
        req2.MergeFrom(reqq[1])

    req3 = req.requests.add()
    req3.type = 4
    if len(reqq) >= 3:
        req3.MergeFrom(reqq[2])

    req4 = req.requests.add()
    req4.type = 129
    if len(reqq) >= 4:
        req4.MergeFrom(reqq[3])

    req5 = req.requests.add()
    req5.type = 5
    if len(reqq) >= 5:
        req5.MergeFrom(reqq[4])

    return api_req(login_type, api, access_token, req, useauth = useauth)

def get_api_endpoint(login_type, access_token, api = API_URL):
    p_ret = get_profile(login_type, access_token, api, None)
    try:
        return ('https://%s/rpc' % p_ret.api_url)
    except:
        return None

def login_google(email,passw):
    reqses = requests.session()
    reqses.headers.update({'User-Agent':'Niantic App'})
    reqses.headers.update({'User-Agent':'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H143'})
    first='https://accounts.google.com/o/oauth2/auth?client_id=848232511240-73ri3t7plvk96pj4f85uj8otdat2alem.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&response_type=code&scope=openid%20email%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email'
    second='https://accounts.google.com/AccountLoginInfo'
    third='https://accounts.google.com/signin/challenge/sl/password'
    last='https://accounts.google.com/o/oauth2/token'
    r=reqses.get(first)
    
    GALX= re.search('<input type="hidden" name="GALX" value=".*">',r.content)
    gxf= re.search('<input type="hidden" name="gxf" value=".*:.*">',r.content)
    cont = re.search('<input type="hidden" name="continue" value=".*">',r.content)
    
    GALX=re.sub('.*value="','',GALX.group(0))
    GALX=re.sub('".*','',GALX)
    
    gxf=re.sub('.*value="','',gxf.group(0))
    gxf=re.sub('".*','',gxf)
    
    cont=re.sub('.*value="','',cont.group(0))
    cont=re.sub('".*','',cont)
    
    data1={'Page':'PasswordSeparationSignIn',
            'GALX':GALX,
            'gxf':gxf,
            'continue':cont,
            'ltmpl':'embedded',
            'scc':'1',
            'sarp':'1',
            'oauth':'1',
            'ProfileInformation':'',
            '_utf8':'?',
            'bgresponse':'js_disabled',
            'Email':email,
            'signIn':'Next'}
    r1=reqses.post(second,data=data1)
    
    profile= re.search('<input id="profile-information" name="ProfileInformation" type="hidden" value=".*">',r1.content)
    gxf= re.search('<input type="hidden" name="gxf" value=".*:.*">',r1.content)
    gxf=re.sub('.*value="','',gxf.group(0))
    gxf=re.sub('".*','',gxf)
    
    profile=re.sub('.*value="','',profile.group(0))
    profile=re.sub('".*','',profile)
    data2={'Page':'PasswordSeparationSignIn',
            'GALX':GALX,
            'gxf':gxf,
            'continue':cont,
            'ltmpl':'embedded',
            'scc':'1',
            'sarp':'1',
            'oauth':'1',
            'ProfileInformation':profile,
            '_utf8':'?',
            'bgresponse':'js_disabled',
            'Email':email,
            'Passwd':passw,
            'signIn':'Sign in',
            'PersistentCookie':'yes'}
    r2=reqses.post(third,data=data2)
    fourth=r2.history[len(r2.history)-1].headers['Location'].replace('amp%3B','').replace('amp;','')
    r3=reqses.get(fourth)
    
    client_id=re.search('client_id=.*&from_login',fourth)
    client_id= re.sub('.*_id=','',client_id.group(0))
    client_id= re.sub('&from.*','',client_id)
    
    state_wrapper= re.search('<input id="state_wrapper" type="hidden" name="state_wrapper" value=".*">',r3.content)
    state_wrapper=re.sub('.*state_wrapper" value="','',state_wrapper.group(0))
    state_wrapper=re.sub('"><input type="hidden" .*','',state_wrapper)
    connect_approve=re.search('<form id="connect-approve" action=".*" method="POST" style="display: inline;">',r3.content)
    connect_approve=re.sub('.*action="','',connect_approve.group(0))
    connect_approve=re.sub('" me.*','',connect_approve)
    data3 = OrderedDict([('bgresponse', 'js_disabled'), ('_utf8', '?'), ('state_wrapper', state_wrapper), ('submit_access', 'true')])
    r4=reqses.post(connect_approve.replace('amp;',''),data=data3)
    code= re.search('<input id="code" type="text" readonly="readonly" value=".*" style=".*" onclick=".*;" />',r4.content)
    code=re.sub('.*value="','',code.group(0))
    code=re.sub('" style.*','',code)
    data4={'client_id':client_id,
        'client_secret':'NCjF1TLi2CcY6t5mt0ZveuL7',
        'code':code,
        'grant_type':'authorization_code',
        'redirect_uri':'urn:ietf:wg:oauth:2.0:oob',
        'scope':'openid email https://www.googleapis.com/auth/userinfo.email'}
    r5 = reqses.post(last,data=data4)
    return json.loads(r5.content)['id_token']


def login_ptc(username, password):
    print('[!] login for: {}'.format(username))
    head = {'User-Agent': 'niantic'}
    r = SESSION.get(LOGIN_URL, headers=head)
    jdata = json.loads(r.content)
    data = {
        'lt': jdata['lt'],
        'execution': jdata['execution'],
        '_eventId': 'submit',
        'username': username,
        'password': password,
    }
    r1 = SESSION.post(LOGIN_URL, data=data, headers=head)

    ticket = None
    try:
        ticket = re.sub('.*ticket=', '', r1.history[0].headers['Location'])
    except e:
        print(r1.json()['errors'][0])
        return None

    data1 = {
        'client_id': 'mobile-app_pokemon-go',
        'redirect_uri': 'https://www.nianticlabs.com/pokemongo/error',
        'client_secret': 'w8ScCUXJQc6kXKw8FiOhd8Fixzht18Dq3PEVkUCP5ZPxtgyWsbTvWHFLm2wNY0JR',
        'grant_type': 'refresh_token',
        'code': ticket,
    }
    r2 = SESSION.post(LOGIN_OAUTH, data=data1)
    print r2.content
    access_token = re.sub('&expires.*', '', r2.content)
    access_token = re.sub('.*access_token=', '', access_token)
    return access_token

def heartbeat(api_endpoint, access_token, response, login_type):
    m4 = pokemon_pb2.RequestEnvelop.Requests()
    m = pokemon_pb2.RequestEnvelop.MessageSingleInt()
    m.f1 = int(time.time() * 1000)
    m4.message = m.SerializeToString()
    m5 = pokemon_pb2.RequestEnvelop.Requests()
    m = pokemon_pb2.RequestEnvelop.MessageSingleString()
    m.bytes = "05daf51635c82611d1aac95c0b051d3ec088a930"
    m5.message = m.SerializeToString()

    walk = sorted(getNeighbors())

    m1 = pokemon_pb2.RequestEnvelop.Requests()
    m1.type = 106
    m = pokemon_pb2.RequestEnvelop.MessageQuad()
    m.f1 = ''.join(map(encode, walk))
    m.f2 = "\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"
    m.lat = COORDS_LATITUDE
    m.long = COORDS_LONGITUDE
    m1.message = m.SerializeToString()
    response = get_profile(
        login_type,
        access_token,
        api_endpoint,
        response.unknown7,
        m1,
        pokemon_pb2.RequestEnvelop.Requests(),
        m4,
        pokemon_pb2.RequestEnvelop.Requests(),
        m5)
    payload = response.payload[0]
    heartbeat = pokemon_pb2.ResponseEnvelop.HeartbeatPayload()
    heartbeat.ParseFromString(payload)
    return heartbeat

def main(location=None, direction=None):
    
    pokemons = json.load(open('api/pokemon.json'))
    ptc_username = os.environ.get('PTC_USERNAME', "Invalid")
    ptc_password = os.environ.get('PTC_PASSWORD', "Invalid")
            
    set_location(location)
    
    login_type = "ptc"
    access_token = "fake"
    
    try:
        f = open('access_token.json','r')
        cached_token_info = json.loads(f.read())
        f.close()
        login_type = cached_token_info['login_type']
        access_token = cached_token_info['access_token']
    except:
        pass
    
    api_endpoint = get_api_endpoint(login_type, access_token)
    if api_endpoint == "https:///rpc":
        print "BAD CACHE"
    
        login_type = "ptc"
        try:
            access_token = login_ptc(ptc_username, ptc_password)
        except:
            access_token = None
        print "access_token", access_token
        if access_token is None:
            print('[-] Trouble logging in via PTC')
            
            print('[+] Authentication with google...')
            goog_username = os.environ.get('GOOG_USERNAME', "Invalid")
            goog_password = os.environ.get('GOOG_PASSWORD', "Invalid")
            access_token = login_google(goog_username, goog_password)
            login_type = "google"
            
        f = open('access_token.json','w')
        f.write(json.dumps({
            "access_token": access_token,
            "login_type": login_type
        })) 
        f.close()
        
        print('[+] RPC Session Token: {} ...'.format(access_token[:25]))

        api_endpoint = get_api_endpoint(login_type, access_token)
    else:
        print "Login cache is good!"
        
    print "api_endpoint", api_endpoint
        
    if api_endpoint is None:
        print('[-] RPC server offline')
        return
    print('[+] Received API endpoint: {}'.format(api_endpoint))

    response = get_profile(login_type, access_token, api_endpoint, None)
    if response is not None:
        print('[+] Login successful')

        payload = response.payload[0]
        profile = pokemon_pb2.ResponseEnvelop.ProfilePayload()
        profile.ParseFromString(payload)
        print('[+] Username: {}'.format(profile.profile.username))

        creation_time = datetime.fromtimestamp(int(profile.profile.creation_time)/1000)
        print('[+] You are playing Pokemon Go since: {}'.format(
            creation_time.strftime('%Y-%m-%d %H:%M:%S'),
        ))

        for curr in profile.profile.currency:
            print('[+] {}: {}'.format(curr.type, curr.amount))
    else:
        print('[-] Ooops...')

    nearby_pokes = []

    original_lat = FLOAT_LAT
    original_long = FLOAT_LONG
    
    if direction == "south":
        original_lat = original_lat-0.002
    elif direction == "west":
        original_long = original_long-0.002
    elif direction == "north":
        original_lat = original_lat+0.002
    elif direction == "east":
        original_long = original_long+0.002
        
    print "Scanning...", original_lat, original_long
    
    origin = LatLng.from_degrees(original_lat, original_long)
    parent = CellId.from_lat_lng(LatLng.from_degrees(original_lat, original_long)).parent(15)

    h = heartbeat(api_endpoint, access_token, response, login_type)
    hs = [h]
    seen = set([])
    for child in parent.children():
        latlng = LatLng.from_point(Cell(child).get_center())
        set_location_coords(latlng.lat().degrees, latlng.lng().degrees, 0)
        hs.append(heartbeat(api_endpoint, access_token, response, login_type))
    set_location_coords(original_lat, original_long, 0)

    visible = []

    for hh in hs:
        for cell in hh.cells:
            for wild in cell.WildPokemon:
                hash = wild.SpawnPointId + ':' + str(wild.pokemon.PokemonId)
                if (hash not in seen):
                    visible.append(wild)
                    seen.add(hash)

    print('')
    for cell in h.cells:
        if cell.NearbyPokemon:
            other = LatLng.from_point(Cell(CellId(cell.S2CellId)).get_center())
            diff = other - origin
            # print(diff)
            difflat = diff.lat().degrees
            difflng = diff.lng().degrees
            direction = (('N' if difflat >= 0 else 'S') if abs(difflat) > 1e-4 else '')  + (('E' if difflng >= 0 else 'W') if abs(difflng) > 1e-4 else '')
            print("Within one step of %s (%sm %s from you):" % (other, int(origin.get_distance(other).radians * 6366468.241830914), direction))
            for poke in cell.NearbyPokemon:
                print('    (%s) %s' % (poke.PokedexNumber, pokemons[poke.PokedexNumber - 1]['Name']))

    print('')
    for poke in visible:
        other = LatLng.from_degrees(poke.Latitude, poke.Longitude)
        diff = other - origin
        # print(diff)
        difflat = diff.lat().degrees
        difflng = diff.lng().degrees
        direction = (('N' if difflat >= 0 else 'S') if abs(difflat) > 1e-4 else '')  + (('E' if difflng >= 0 else 'W') if abs(difflng) > 1e-4 else '')

        nearby_pokes.append({
            "id": poke.pokemon.PokemonId,
            "name": pokemons[poke.pokemon.PokemonId - 1]['Name'],
            "latitude": poke.Latitude,
            "longitude": poke.Longitude,
            "time_left": poke.TimeTillHiddenMs / 1000,
            "distance": int(origin.get_distance(other).radians * 6366468.241830914),
            "direction": direction
        })

        print("(%s) %s is visible at (%s, %s) for %s seconds (%sm %s from you)" % (poke.pokemon.PokemonId, pokemons[poke.pokemon.PokemonId - 1]['Name'], poke.Latitude, poke.Longitude, poke.TimeTillHiddenMs / 1000, int(origin.get_distance(other).radians * 6366468.241830914), direction))
        
    print('')

    return nearby_pokes

if __name__ == '__main__':
    main()
    
