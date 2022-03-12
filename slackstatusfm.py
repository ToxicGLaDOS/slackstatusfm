#!/usr/bin/env python

import pylast, requests, json, time, config


content_type = "application/json; charset=utf-8"
network = pylast.LastFMNetwork(
        api_key=config.LASTFM_API_KEY,
        api_secret=config.LASTFM_API_SECRET,
    )
slack_api_url = "https://slack.com/api/users.profile.set"

while True:
    user = network.get_user(config.LASTFM_USERNAME)
    now_playing = user.get_now_playing()


    data = {
        "profile": {
                    "status_text": f"Listening to {now_playing}",
                    "status_emoji": ":musical_note:"
                }
    }

    headers = {}
    headers["authorization"] = f"Bearer {config.SLACK_TOKEN}"
    headers["cookie"] = config.COOKIE
    headers["content-type"] = content_type

    response = requests.post(slack_api_url, data=json.dumps(data), headers=headers)

    if not response.json()["ok"]:
        raise Exception(f"Got error from slack. Here's the response: {response.text}")

    time.sleep(config.UPDATE_DELAY)
