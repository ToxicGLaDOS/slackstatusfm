# Install dependencies

```
pip install -r requirements.txt
```

# Configuration and secrets
Create a file named `config.py` in the same directory as `slackstatusfm.py` and populate it with your configuration like this (see below for details on getting these secrets):

```
# Because this is a python file you can choose how you
# want to import your secrets, for instance you could
# read them from the environment instead of hardcoding them

# API auth for lastfm
LASTFM_API_KEY = "API_KEY_HERE"
LASTFM_API_SECRET = "API_SECRET_HERE"

# User you want to check the current playing song for
USERNAME = "myusername"

# Auth stuff for slack
SLACK_TOKEN = "xoxc-XXXXXXXX..."
COOKIE = "d=xoxd-XXXXX;..."

# Delay between calls to lastfm/slack in seconds
# Basically how often to check in
UPDATE_DELAY = 10
```

# Getting lastfm API access

Go to [https://www.last.fm/api/account/create](https://www.last.fm/api/account/create) and fill out the form. Callback URL and Application Homepage don't seem to be required. There doesn't seem to be an approval process, so you should get your api key and secret instantly.

# Getting slack token and cookie

## SLACK_TOKEN
Go to [https://slack.com/customize](https://slack.com/customize) open the developer tools (CTRL+SHIFT+i on chrome), navigate to the console and run `TS.boot_data.api_token` that is your `SLACK_TOKEN`.

## COOKIE

Go to [https://api.slack.com/methods/auth.test/test](https://api.slack.com/methods/auth.test/test), open the developer tools (CTRL+SHIFT+i on chrome), navigate to the network tab. Now, enter your `SLACK_TOKEN` in the box under "Or, provide your own token:" and press the "Test method" button. This should make exactly one call and add one entry in your network tab, click that new entry and find the `cookie:` field under `Request Headers`. Copy the cookie exactly. Don't use the "Copy value" option in chrome, it will URL decode the cookie and we don't want that, instead highlight and CTRL+C. To know if you did it right you should see some percent signs in the `d=xoxd-XXXXX` section right at the beginning.

# Usage

```
./slackstatusfm.py
```
