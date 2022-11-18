# twitter to mastodon

## Scope
This script will check against a specific user in twitter, then post the tweet to a Mastodon server. The main goal of this is to "repost" breaking news, so you don't have to watch multiple threads.

## Usage

- You need to edit the [config.toml](./config.toml) with the settings.
  - `server` = The domain name of the server
  - `bot_token` = The bot token to post as
  - `bearer_token` = The token from the Twitter v2 API
  - `name` = The name of the account from Twitter
  - `index` = The "namespace" for this instance on the redis machine. Defaults to 5, but if you run this on mulitple times on the same machine, change this index.
- You need to have `redis` running, either install via `brew` or whatever to store posts this bot has done.
- You should also create a `cronjob` that runs this every min.
```cron
* * * * *      python ~/src/python-twitter-to-mastodon/app.py 
```


```text
Copyright:: 2022- IBM, Inc

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```