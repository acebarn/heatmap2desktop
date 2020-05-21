import requests, json
import subprocess
import sys
import yaml
import oauth2
import os
import json


with open("config.yml", "r") as configfile:
    config = yaml.load(configfile)

AUTHORIZE_URL = "https://www.strava.com/oauth/authorize"
TOKEN_URL = "https://www.strava.com/oauth/token"
CALLBACK_URL = "http://localhost"
TEST_API_URL = "https://www.strava.com/api/v3/athlete/"

EXPORT_DIRECTORY = "gpx"

    
def authorize():

    access_token = None
    refresh_token = None

    #check if access token is present
    if not os.path.exists("access.token"):
        token_obj = get_access_token()
        with open("access.token", "w") as tokenfile:
            json.dump(token_obj, tokenfile)

    #read present tokens from store
    with open("access.token") as json_file:
        tokens = json.load(json_file)
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]
    
    #check if access token is valid
    test_token_headers = {'Authorization': 'Bearer ' + access_token}
    test_token_response = requests.get(TEST_API_URL, headers=test_token_headers, verify=False)
    test_token_response_obj = test_token_response.json()
    
    if test_token_response.status_code == 401:
        print("Error while testing token validity")
        print(test_token_response_obj)
        sys.exit()
        #TODO handle expired token refresh

    print("finished authorizing")
    return access_token
    

def get_access_token(): # Returns Token response Json Object
    #client (application) credentials - located at apim.byu.edu
    client_id = config["strava_client_id"]
    client_secret = config["strava_client_secret"]

    #step A - simulate a request from a browser on the authorize_url - will return an authorization code after the user is
    # prompted for credentials.
    authorization_redirect_url = AUTHORIZE_URL + '?response_type=code&client_id=' + str(client_id) + '&redirect_uri=' + CALLBACK_URL + '&scope=activity:read'
    print("go to the following url on the browser and enter the code from the returned url: ")
    print("---  " + authorization_redirect_url + "  ---")
    authorization_code = input('code: ')

    # step I, J - turn the authorization code into a access token, etc
    data = {
        'grant_type': 'authorization_code', 
        'code': authorization_code, 
        'redirect_uri': CALLBACK_URL,
        'client_id': client_id,
        'client_secret': client_secret
        }
    print("requesting access token")
    access_token_response = requests.post(TOKEN_URL, data=data, verify=False, allow_redirects=False)
    # access_token_response = requests.post(TOKEN_URL, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))

    print ("response")
    print (access_token_response.headers)
    print ('body: ' + access_token_response.text)

    return json.loads(access_token_response.text)
    

def get_activity_ids(token, count):
    print("Retrieving activities from Strava...")
    activity_ids = []

    for i in range(0, count // 200 + 1):
        fetch_size = 200
        if count <= fetch_size * i: #TODO Paging korrigieren
            fetch_size = count
        response = requests.get("https://www.strava.com/api/v3/athlete/activities/", headers={'Authorization': 'Bearer ' + token}, params={"page": i+1, "per_page": fetch_size}, verify=False)
        for activity in json.loads(response.text):
            activity_ids.append(str(activity["id"]))
    print("Found %s activities" % len(activity_ids) )
    return activity_ids

def get_activity_stream(token, id):
    # check if activity has already been downloaded
    if os.path.exists(EXPORT_DIRECTORY + "/" + id):
        print("activity "+ id + " already exists")
        return
    # download activity stream
    print("Downloading activity %s" % id)
    response = requests.get("https://www.strava.com/api/v3/activities/"+id+"/streams", headers={'Authorization': 'Bearer ' + token}, params={"keys": "latlng"}, verify=False)
    return json.loads(response.text)

def export(count):
    if not os.path.isdir(EXPORT_DIRECTORY):
        os.makedirs(EXPORT_DIRECTORY)
    token = authorize()
    activities = get_activity_ids(token, count)
    print("Downloading activity streams...")
    for activity_id in activities:
        activity_json = get_activity_stream(token, activity_id)
        with open(EXPORT_DIRECTORY + "/" + activity_id + ".json", "w+") as activity_file:
            json.dump(activity_json, activity_file)

if __name__ == '__main__':
    export()


