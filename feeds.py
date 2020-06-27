import requests, json, redis, time
from flask import Flask,render_template, request

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

def create_feed_action(conn, uid, login, message, **data):
    id = conn.incr('feed-action:id:')
    data.update({
        'message': message,
        'posted': time.time(),
        'id': id,
        'uid': uid,
        'login': login,
    })
    conn.hmset('feed-action:%s'%id, data)
    return id

def post_feed_action(conn, uid, login, message, **data):
    id = create_feed_action(conn, uid, login, message, **data)
    posted = conn.hget('feed-action:%s'%id, 'posted')
    conn.zadd('feed:11', {"%s"%id: float(posted)}) #en lugar de 10 iria el id del follower(s)

def get_feed_by_user(conn, uid, cant):
    feed_action_keys=conn.zrange('feed:%s'%uid, 0, cant-1)
    feed_actions=[]
    for feed_action_key in feed_action_keys:
        feed_action=conn.hgetall('feed-action:%s'%feed_action_key)
        feed_actions.append(feed_action)
    return feed_actions

post_feed_action(r, 1, "Covid Perez", "Hello world agaiin")
print(get_feed_by_user(r, 11, 0))

#for key in r.scan_iter("feed:*"):
#    print(key)
