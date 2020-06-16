import requests, json, redis
from flask import Flask,render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
r = redis.Redis(host='localhost', port=6379, db=0)

def make_es_search(data_to_search, licence_to_search, language_to_search, startDate_to_search, endDate_to_search):
    #response=es.search(index='source_code_data', body={'query': { 'match': { 'sourceCode': data_to_search } } })
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


@app.route('/search', methods=['POST'])
def search():
    if request.form['hasadvancedsearch'] == "yes":
        search_result=make_es_search(request.form['data_to_search'], request.form['licence_to_search'], request.form['language_to_search'], request.form['startDate_to_search'], request.form['endDate_to_search'])
    else:
        search_result=make_es_search(request.form['data_to_search'], "*", "*", "", request.form['endDate_to_search'])
    return render_template('results.html', search_result=search_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
