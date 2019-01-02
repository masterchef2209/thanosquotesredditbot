import praw
import re
import os
import random
import time


reddit_username = os.environ['reddit_username']
reddit_password = os.environ['reddit_password']
client_id = os.environ['client_id']
client_secret = os.environ['client_secret']

thanos_quotes = \
    [
        "I know what it's like to lose. To feel so desperately that you're right, yet to fail nonetheless. It’s frightening. Turns the legs to jelly. I ask you, to what end? Dread it. Run from it. Destiny arrives all the same. And now, it's here. Or should I say, I am.",
        "You have my respect, Stark. When I'm done, half of humanity will still be alive. I hope they remember you." + "\n(to Iron Man)",
        "You should have gone for the head." + "\n(to Thor)",
        "Fun isn’t something one considers when balancing the universe. But this… does put a smile on my face.",
        "You’re strong. But I could snap my fingers, and you’d all cease to exist.",
        "The end is near.",
        "You’re a great fighter, Gamora. Come. Let me help you.",
        "I ignored my destiny once, I can not do that again. Even for you. I’m sorry Little one.",
        "With all six stones, I can simply snap my fingers, they would all cease to exist. I call that mercy."
        """Thanos: Daughter.
        Gamora: Did you do it?
        Thanos: Yes.
        Gamora: What did it cost?
        Thanos: Everything.""",
        "Your optimism is misplaced, Asgardian.",
        "The hardest choices require the strongest wills.",
        "You should choose your words wisely",
        "The Tesseract… or your brother’s head. I assume you have a preference?\n(To Loki)",
        "I’m the only one who knows that. At least I’m the only who has the will to act on it. For a time, you had that same will. As you fought by my side, daughter.\n(To Gamora)",
        "Going to bed hungry. Scrounging for scraps. Your planet was on the brink of collapse. I was the one who stopped that. You know what’s happened since then? The children born have known nothing but full bellies and clear skies. It’s a paradise.",
        "You’re not the only one cursed with knowledge...\n(to Iron Man)",
        "A small price to pay for salvation.",
        "Little one, it’s a simple calculus. This universe is finite, its resources, finite… if life is left unchecked, life will cease to exist. It needs correcting.",
        "Fine. I'll do it myself."
    ]


def bot_login():
    print("Loggin in...")
    r = praw.Reddit(username=reddit_username,
                    password=reddit_password,
                    client_id=client_id,
                    client_secret=client_secret,
                    user_agent="thanosquotesbot")
    print("Logged in.")

    return r


def run_bot(r, comments_replied_to):
    for comment in r.subreddit('test').stream.comments():
        if comment.id not in comments_replied_to:
            if re.search("perfectly balanced", comment.body, re.IGNORECASE):
                print(comment.body)
                comment.reply("...as all things should be.")
                comments_replied_to.append(comment.id)
                with open("comments_replied_to.txt", "a") as f:
                    f.write(comment.id + "\n")

            if re.search("thanos quote", comment.body, re.IGNORECASE):
                print(comment.body)
                thanos_reply = random.choice(thanos_quotes)
                comment.reply(thanos_quotes)
                if comment.id not in comments_replied_to:
                    comments_replied_to.append(comment.id)
                    with open("comments_replied_to.txt", "a") as f:
                        f.write(comment.id + "\n")
    print("Sleeping for 10 seconds")
    time.sleep(120)


def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = list(filter(None, comments_replied_to))

    return comments_replied_to


r = bot_login()
comments_replied_to = get_saved_comments()
while True:
    run_bot(r, comments_replied_to)
