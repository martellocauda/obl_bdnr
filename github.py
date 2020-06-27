import requests, json, redis, time, math
from flask import Flask,render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
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

def make_es_search(data_to_search, licence_to_search, language_to_search, startDate_to_search, endDate_to_search):
    if startDate_to_search == "":
        response=es.search(index='source_code_data',
            body={
                'query': { 
                    'bool' : {
                        'must' : [
                            {'match': { 'sourceCode': data_to_search } },
                            {'wildcard':{ 'licence.keyword': licence_to_search } },
                            {'wildcard':{ 'codeLenguage.keyword': language_to_search } }#cambiar a codeLanguage cuando cambie en ES
                        ] 
                    }
                }
            }
        )
    else:
        response=es.search(index='source_code_data',
            body={
                'query': {
                    'bool' : {
                        'must' : [
                            {'match': { 'sourceCode': data_to_search } },
                            {'wildcard':{ 'licence.keyword': licence_to_search } },
                            {'wildcard':{ 'codeLenguage.keyword': language_to_search } },#cambiar a codeLanguage cuando cambie en ES
                            {"range": {
                                "creationDate": {
                                    "gte": startDate_to_search,
                                    "lte": endDate_to_search,
                                    "format": "yyyy-MM-dd"
                                 }
                            }}
                        ]
                    }
                }
            }
        )
    #adjusting response
    dumped_response = json.dumps(response)
    jsonObject = json.loads(dumped_response)
    jsonObject = jsonObject['hits']
    return jsonObject

def get_distinct_licence_types():
    response=es.search(index='source_code_data',
        body={
            "size":"0",
                "aggs":{
                    "uniq_licence" : {
                        "terms" : {"field":"licence.keyword"}
                    }
                }
        }
    )
    #adjusting response
    dumped_response = json.dumps(response)
    jsonObject = json.loads(dumped_response)
    jsonObject = jsonObject['aggregations']['uniq_licence']['buckets']
    return jsonObject 

def get_distinct_languages():
    response=es.search(index='source_code_data',
        body={
            "size":"0",
                "aggs":{
                    "uniq_language" : {
                        "terms" : {"field":"codeLenguage.keyword"}#cambiar a codeLanguage cuando cambie en es
                    }
                }
        }
    )
    #adjusting response
    dumped_response = json.dumps(response)
    jsonObject = json.loads(dumped_response)
    jsonObject = jsonObject['aggregations']['uniq_language']['buckets']
    return jsonObject

@app.route('/', methods=['GET'])
def index():
    licences=get_distinct_licence_types()
    languages=get_distinct_languages()
    return render_template('index.html', licences=licences, languages=languages)
    
@app.route('/feed', methods=['GET', 'POST'])
def feed_get():
    if request.method == 'POST':
        post_feed_action(r, 1, "Covid Perez", "Peruanadas") #cambiar valores, poner esto en un boton y tener un set de posteos distintos
    feed_of_logged_user=get_feed_by_user(r, 11, 0) #ver este 11, hay que tomar el id del usuario logueado
    cant_feed_actions=len(feed_of_logged_user)
    feed_actions_per_page=5
    pages=math.ceil(cant_feed_actions/feed_actions_per_page)
    pages_arr=range(1, pages+1, 1)
    activepage=request.args.get('pag')
    if activepage:
        activepage=int(activepage)
    cont=1
    put_page=1
    for feed_action in feed_of_logged_user:
        if cont > 5:
            cont=1
            put_page+=1
        feed_action['page']=put_page
        feed_action['posted_formatted']=time.ctime(float(feed_action['posted']))
        cont+=1
    return render_template('feed.html', feed_of_logged_user=feed_of_logged_user, pages=pages_arr, activepage=activepage)

@app.route('/codesearch', methods=['POST'])
def search():
    if request.form['hasadvancedsearch'] == "yes":
        search_result=make_es_search(request.form['data_to_search'], request.form['licence_to_search'], request.form['language_to_search'], request.form['startDate_to_search'], request.form['endDate_to_search'])
    else:
        search_result=make_es_search(request.form['data_to_search'], "*", "*", "", request.form['endDate_to_search'])
    return render_template('results.html', search_result=search_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
