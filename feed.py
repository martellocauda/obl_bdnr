import json, redis, time

r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

def create_feed_action(uid, login, message, repo, **data):
    id = r.incr('feed-action:id:')
    data.update({
        'message': message,
        'posted': time.time(),
        'id': id,
        'uid': uid,
        'login': login,
        'repository': repo
    })
    r.hmset('feed-action:%s'%id, data)
    return id

def post_feed_action(uid, login, message, repo, **data):
    id = create_feed_action(uid, login, message, repo, **data)
    posted = r.hget('feed-action:%s'%id, 'posted')
    r.zadd('feed:11', {"%s"%id: float(posted)}) #aqui estamos dejando las referencias al post para todos los followers, 11 es un fixed follower

def get_feed_by_user(uid, cant):
    feed_action_keys=r.zrange('feed:%s'%uid, 0, cant-1)
    feed_actions=[]
    for feed_action_key in feed_action_keys:
        feed_action=r.hgetall('feed-action:%s'%feed_action_key)
        feed_actions.insert(0, feed_action)
    for feed_action in feed_actions:
        feed_action['posted_formatted']=time.ctime(float(feed_action['posted']))
    return feed_actions
