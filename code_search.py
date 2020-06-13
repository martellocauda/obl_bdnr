import requests, json
from flask import Flask,render_template, request

from elasticsearch import Elasticsearch
app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def make_es_search(data_to_search):
    response=es.search(index='source_code_data',
        body={
            'query': {
                'match': {
                    'sourceCode': data_to_search
                }
            }
        }
    )
    #adjusting response
    dumped_response = json.dumps(response)
    jsonObject = json.loads(dumped_response)
    jsonObject = jsonObject['hits']
    return jsonObject


@app.route('/', methods=['GET'])
def index():
        return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    ##ver si viene ordenada por score, sino, ordenar
    search_result=make_es_search(request.form['to_search'])
    return render_template('results.html', search_result=search_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
