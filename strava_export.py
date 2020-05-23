import json
import os
import subprocess
import sys

import certifi
import urllib3

import oauth2
import yaml


AUTHORIZE_URL = "https://www.strava.com/oauth/authorize"
TOKEN_URL = "https://www.strava.com/oauth/token"
CALLBACK_URL = "http://localhost"
TEST_API_URL = "https://www.strava.com/api/v3/athlete/"
TOKEN_FILE  = "access.token"

ACTIVITY_FETCH_SIZE = 200

with open("config.yml", "r") as configfile:
    config = yaml.load(configfile, Loader=yaml.FullLoader)

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())


def authorize():

    access_token = None
    refresh_token = None

    #check if access token is present
    if not os.path.exists(TOKEN_FILE):
        token_obj = get_access_token()
        with open(TOKEN_FILE, "w") as tokenfile:
            json.dump(token_obj, tokenfile)

    #read present tokens from store
    with open(TOKEN_FILE) as json_file:
        tokens = json.load(json_file)
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]

    #check if access token is valid
    test_token_headers = {'Authorization': 'Bearer ' + access_token}
    test_token_response = http.request("GET",
                                       TEST_API_URL,
                                       headers=test_token_headers)
    test_token_response_obj = test_token_response.data.decode('utf-8')

    if test_token_response.status == 401:
        print("Token is expired. Trying to refresh Token")
        refresh_result = send_refresh_token(refresh_token)
        with open(TOKEN_FILE, "w") as tokenfile:
            json.dump(refresh_result, tokenfile)

    print("finished authorizing")
    return access_token


def get_access_token():  # Returns Token response Json Object
    client_id = config["strava_client_id"]
    client_secret = config["strava_client_secret"]

    authorization_redirect_url = AUTHORIZE_URL + '?response_type=code&client_id=' + str(
        client_id) + '&redirect_uri=' + CALLBACK_URL + '&scope=activity:read'
    print(
        "go to the following url on the browser and enter the code from the returned url: "
    )
    print("---  " + authorization_redirect_url + "  ---")
    authorization_code = input('code: ')

    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': CALLBACK_URL,
        'client_id': client_id,
        'client_secret': client_secret
    }
    print("requesting access token")
    access_token_response = http.request("POST", TOKEN_URL, fields=data)

    print("response")
    print(access_token_response.headers)
    print('body: ' + access_token_response.data.decode('utf-8'))

    return json.loads(access_token_response.data.decode('utf-8'))

def send_refresh_token(refresh_token):
    client_id = config["strava_client_id"]
    client_secret = config["strava_client_secret"]
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }
    print("requesting access token")
    refresh_token_response = http.request("POST", TOKEN_URL, fields=data)

    return json.loads(refresh_token_response.data.decode('utf-8'))


def get_activity_ids(token, count):
    print("Retrieving activities from Strava...")
    activity_ids = []
    fetched = 0

    for i in range(1, count // ACTIVITY_FETCH_SIZE + 2):
        if count <= ACTIVITY_FETCH_SIZE:
            fetch_size = count
        else:
            if fetched <= ACTIVITY_FETCH_SIZE:
                fetch_size = ACTIVITY_FETCH_SIZE
            else:
                fetch_size = ACTIVITY_FETCH_SIZE % count

        response = http.request(
            "GET",
            "https://www.strava.com/api/v3/athlete/activities/",
            fields={
                "page": i,
                "per_page": fetch_size
            },
            headers={'Authorization': 'Bearer ' + token})
        fetched += fetch_size

        for activity in json.loads(response.data.decode('utf-8')):
            activity_ids.append(str(activity["id"]))
    print("Found %s activities" % len(activity_ids))
    return activity_ids


def get_activity_stream(token, id, export_dir):
    # check if activity has already been downloaded
    if os.path.exists(export_dir + "/" + id + ".json"):
        print("activity " + id + " already exists")
        with open(export_dir + "/" + id + ".json") as existing_file:
            return json.load(existing_file)

    # download activity stream
    print("Downloading activity %s" % id)
    response = http.request("GET",
                            "https://www.strava.com/api/v3/activities/" + id +
                            "/streams",
                            fields={"keys": "latlng"},
                            headers={'Authorization': 'Bearer ' + token})
    return json.loads(response.data.decode('utf-8'))

# This method validates that the downloaded Stream contains correct gpx data
def hasGpxData(activity_json):
    if isinstance(activity_json, list) and len(activity_json) > 1:
        if "type" in activity_json[0] and activity_json[0]["type"] == "latlng":
            return True
    return False

def export(count, export_dir):
    if not os.path.isdir(export_dir):
        os.makedirs(export_dir)
    token = authorize()
    activities = get_activity_ids(token, count)
    print("Downloading activity streams...")
    for activity_id in activities:
        activity_json = get_activity_stream(token, activity_id, export_dir)
        if hasGpxData(activity_json):
            with open(export_dir + "/" + activity_id + ".json",
                      "w+") as activity_file:
                json.dump(activity_json, activity_file)
    return activities




if __name__ == '__main__':
    export()
