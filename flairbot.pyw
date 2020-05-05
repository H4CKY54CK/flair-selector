import os
import re
import json
import praw
import time
os.chdir(os.path.abspath(os.path.dirname(__file__)))
reddit = praw.Reddit('flairbot')
subreddit = reddit.subreddit(reddit.config.custom['subreddit'])
flairs = json.load(open('flairs.json'))
for msg in reddit.inbox.stream():
    author = str(msg.author)
    if msg.subject == 'flair' and not bool(re.compile(r'[^a-zA-Z0-9-_]').search(author)):
        content = msg.body.split(',', 1)
        if content[0] in flairs:
            flair = flairs[content[0]]
            ftext = f":{flair}:"
            if len(content) > 1:
                ftext = f":{flair}:{content[1].strip()}" if len(f":{flair}:{content[1].strip()}") <= 64 else content[1].strip()
            subreddit.flair.set(author, ftext, flair)
            msg.mark_read()
            with open('logs.txt', 'a') as f:
                log = f"{time.strftime('%D %T', time.localtime())}: User: {author} | Text: {ftext} | Flair: {flair}\n"
                f.write(log)
