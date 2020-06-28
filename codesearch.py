import requests, json, math
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def make_es_search(data_to_search, licence_to_search, language_to_search, startDate_to_search, endDate_to_search):
    if startDate_to_search == "":
        response=es.search(index='source_code_data',
            body={
                'query': {
                    'bool' : {
                        'must' : [
                            {'match': { 'sourceCode': data_to_search } },
                            {'wildcard':{ 'licence.keyword': licence_to_search } },
                            {'wildcard':{ 'codeLanguage.keyword': language_to_search } }
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
                            {'wildcard':{ 'codeLanguage.keyword': language_to_search } },
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
                        "terms" : {"field":"codeLanguage.keyword"}
                    }
                }
        }
    )
    dumped_response = json.dumps(response)
    jsonObject = json.loads(dumped_response)
    jsonObject = jsonObject['aggregations']['uniq_language']['buckets']
    return jsonObject
