import redis
import uuid
from datetime import datetime
from pytz import timezone, utc
import json


quotes = [
    ("I have not failed. I've just found 10,000 ways that won't work.", "Thomas Alba Edison"),
    ("In the End, we will remember not the words of our enemies, but the silence of our friends.", "Martin Luther King Jr."),
    ("Once you eliminate the impossible, whatever remains, no matter how improbable, must be the truth.", "Sherlock Holmes"),
    ("Only two things are infinite, the universe and human stupidity, and I'm not sure about the former.", "Albert Einstein"),
    ("We didn't lose the game; we just ran out of time.", "Vince Lombardi"),
    ("When one person suffers from a delusion it is called insanity; when many people suffer from a delusion it is called religion.", "Robert Pirsig"),
    ("All are lunatics, but he who can analyze his delusion is called a philosopher.", "Ambrose Bierce"),
    ("C makes it easy to shoot yourself in the foot; C++ makes it harder, but when you do, it blows away your whole leg.", "Bjarne Stroustrup"),
    ("The true measure of a man is how he treats someone who can do him absolutely no good.", "Samuel Johnson"),
    ("I begin by taking. I shall find scholars later to demonstrate my perfect right.", "Frederick (II) the Great"),
    ("I can write better than anybody who can write faster, and I can write faster than anybody who can write better.", "A. J. Liebling"),
    ("I think 'Hail to the Chief' has a nice ring to it.", "John F. Kennedy"),
    ("Dancing is silent poetry.", "Simonides"),
    ("Don't stay in bed, unless you can make money in bed.", "George Burns"),
    ("I'm living so far beyond my income that we may almost be said to be living apart.", "E. E. Cummings"),
    ("He is one of those people who would be enormously improved by death.", "H. H. Munro"),
    ("Facts are the enemy of truth.", "Don Quixote"),
    ("The optimist proclaims that we live in the best of all possible worlds, and the pessimist fears this is true.", "James Branch Cabell"),
    ("A lie gets halfway around the world before the truth has a chance to get its pants on.", "Sir Winston Churchill"),
    ("Not everything that can be counted counts, and not everything that counts can be counted.", "Albert Einstein")
]

def storeGuestbookEntry(red, id, name, message, timestamp):
    obj = {
        'id': id,
        'name': name,
        'message': message,
        'timestamp': timestamp.isoformat()
    }
    json_str = json.dumps(obj)
    print('JSON to insert:'+json_str)
    redis_key = 'guestbook:'+id
    red.set(redis_key, json_str)
    red.lpush('guestbook_list', redis_key)

def current_datetime():
    return datetime.now(utc)

def new_guid():
    return str(uuid.uuid4())

if __name__ == '__main__':
    r = redis.StrictRedis(host='192.168.0.107', port=6379)
    for quote in quotes:
        storeGuestbookEntry(r, new_guid(), quote[1], quote[0], current_datetime())
    print("Completed data load")

