from os import environ as env
import asyncio
import signal

from praw import Reddit
from dotenv import load_dotenv
from discord.ext import commands
from tinydb import TinyDB, Query


class RedditBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = TinyDB(f"{env['DB_NAME']}.json")
        self.reddit = Reddit(user_agent=f"{env['REDDIT_BOT_NAME']} (by /u/{env['REDDIT_USERNAME']})",
                             client_id=env['REDDIT_CLIENT_ID'], client_secret=env['REDDIT_SECRET'],
                             username=env['REDDIT_USERNAME'], password=env['REDDIT_PASSWORD'])

    async def listen_reddit(self):
        subreddit = self.reddit.subreddit(env['REDDIT_SUBREDDIT'])
        print(f"[listening to]: r/{env['REDDIT_SUBREDDIT']}")
        for post in subreddit.stream.submissions(skip_existing=True, pause_after=-1):
            if post:
                print("[new post]:", post.title)
                for user in self.db:
                    d_user = self.get_user(user['id'])
                    await d_user.send(f"{post.title}\n{post.url}")
            await asyncio.sleep(30)

    async def on_ready(self):
        print(f"[init]: {self.user.name} (id: {self.user.id})")
        self.loop.create_task(self.listen_reddit())


def init_commands(bot):
    @bot.command()
    async def ping(ctx):
        """test for liveness"""
        print("[ping'd by]:", ctx.author.name)
        await ctx.send("pong")

    @bot.command()
    async def notifyme(ctx):
        """adds a user to notification list"""
        bot.db.insert({'id': ctx.author.id, 'name': ctx.author.name})
        msg = f"hey {ctx.author.name}, I'll notify you about new posts on r/buildapcsales\nif you ever want to stop, just say `>removeme`"
        print("[add user]:", ctx.author.name)
        await ctx.send(msg)

    @bot.command()
    async def removeme(ctx):
        """removes a user from notification list"""
        User = Query()
        bot.db.remove(User.id == ctx.author.id)
        print("[del user]:", ctx.author.name)
        await ctx.send("i'll no longer notify you about sales")


if __name__ == '__main__':
    load_dotenv()
    desc = f"i'll spam you will all the posts from r/{env['REDDIT_SUBREDDIT']}"
    bot = RedditBot(command_prefix=">", description=desc)
    init_commands(bot)
    try:
        bot.run(env['DISCORD_BOT_TOKEN'])
        bot.command()
    except KeyboardInterrupt:
        pass
    finally:
        bot.loop.close()
