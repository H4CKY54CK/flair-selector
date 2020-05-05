import os
import re
import sys
import json
import praw
import time
import socket
import argparse
def match(strg, search=re.compile(r'[^a-zA-Z0-9-_]').search):
    return not bool(search(strg))
def start(args=None):
    if args.remote:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.connect(('192.168.0.13',1234))
    reddit = praw.Reddit('flairbot')
    subreddit = reddit.subreddit(reddit.config.custom['subreddit'])
    flairs = json.load(open('flairs.json')) # You need a JSON file full of your flairs.
    for msg in reddit.inbox.stream(pause_after=0):
        if msg is None:
            continue
        author = str(msg.author)
        valid_user = match(author)
        if msg.subject == 'flair' and valid_user:
            content = msg.body.split(',', 1)
            flair_id = content[0]
            if flair_id in flairs:
                flair = flairs[flair_id]
                addon = f":{flair}:"
                ftext = addon
                if len(content) > 1:
                    text = content[1].strip()
                    ftext = f"{addon}{text}" if len(addon) + len(text) <= 64 else text
                # print(f"Relevant Data\n -------------\n  User: {author} ({type(author)})\n  Flair Text: {ftext} ({type(ftext)})\n  Flair: {flair} ({type(flair)})\nFlair in `flairs.json`? {flair_id in flairs}")
                subreddit.flair.set(author, ftext, flair)
                msg.mark_read()
                with open('logs.txt', 'a') as f:
                    log = f"{time.strftime('%D %T', time.localtime())}: User: {author} | Text: {ftext} | Flair: {flair}\n"
                    f.write(log)
                if args.remote:
                    ss.send(log.encode())
def main(argv=None):
    argv = (argv or sys.argv)[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--remote', dest='remote', action='store_true', help='whether or not to send log entries back home')
    parser.set_defaults(func=start)
    args = parser.parse_args(argv)
    args.func(args)
if __name__ == '__main__':
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    sys.exit(main())