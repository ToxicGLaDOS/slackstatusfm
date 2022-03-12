#!/usr/bin/env python

import pylast, requests, json, time, config

network = pylast.LastFMNetwork(
        api_key=config.LASTFM_API_KEY,
        api_secret=config.LASTFM_API_SECRET
)
content_type = "application/json; charset=utf-8"
slack_set_profile_url = "https://slack.com/api/users.profile.set"
slack_get_profile_url = "https://slack.com/api/users.profile.get"
headers = {}
headers["authorization"] = f"Bearer {config.SLACK_TOKEN}"
headers["cookie"] = config.COOKIE
headers["content-type"] = content_type


while True:
    response = requests.get(slack_get_profile_url, headers=headers)

    # Only do stuff if the users status emoji is :musical_note:
    # This functions as an on/off switch in slack.
    # We don't want to overwrite it if someone set their status as
    # out to lunch or out of office.
    if response.json()["profile"]["status_emoji"] == ":musical_note:":
        user = network.get_user(config.LASTFM_USERNAME)
        now_playing = user.get_now_playing()
        # We add an extra minute because slack seems to only have 1 minute
        # resolution with checking "status_expiration" so any lower
        # and the status might expire before we get to the next iteration
        # (I tried 20 seconds and that wasn't enough)
        expiration_time = int(time.time()) + config.UPDATE_DELAY + 60

        data = {}
        if now_playing:
            data = {
                "profile": {
                            "status_text": f"Listening to {now_playing}",
                            "status_emoji": ":musical_note:",
                            # We set the expiration so that if you end the program your status will get removed
                            "status_expiration": expiration_time
                        }
            }
        else:
            data = {
                "profile": {
                            "status_text": "Nothing playing :(",
                            "status_emoji": ":musical_note:",
                            # If the status is already nothing playing then we still need to increment the expiriation
                            "status_expiration": expiration_time
                        }
            }

        response = requests.post(slack_set_profile_url, data=json.dumps(data), headers=headers)

        if not response.json()["ok"]:
            raise Exception(f"Got error from slack. Here's the response: {response.text}")



    time.sleep(config.UPDATE_DELAY)
