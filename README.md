# reddit-post-notifier-bot

Simple reddit/discord bot to dm users when new posts appear for a specific subreddit.

## Running Locally

Setup a `.env` file based on `example.env`, install requirements and run!

```
$ cp example.env .env
$ vim .env
<do ya thing>
$ pip install -r requirements.txt 
$ python bot.py 
[init]: pc-sales-bot (id: 633509824495222815)
[listening to]: r/buildapcsales
```

## Docker (and compose)

Just build and run! You may want to specify the .env file (`--env-file=.env`), and it may be useful to mount your json db to your container (`-v ${PWD}/db.json:/bot/db.json`).

## TODO

- filter notifications to be based on keywords in post title
- watch multiple subreddits