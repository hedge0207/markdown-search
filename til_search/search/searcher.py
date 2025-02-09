from elasticsearch import Elasticsearch

from til_search.config.config import config


class Searcher:

    def __init__(self):
        self._es_client = Elasticsearch(config.elasticsearch_urls)
    
    def _make_query(self, from_=0, size=10, term=None):
        query = {
            "from": from_,
            "size": size,
            "query": {
                "match_all":{}
            },
            "highlight":{
                "fields":{
                    "content":{}
                }
            }
        }
        if term:
            query["query"] = {
                "match":{
                    "content": term
                }
            }
        return query
    
    def search(self):
        print("Please enter query:", end=" ")
        term = input()
        res = self._es_client.search(index=config.index_name, body=self._make_query(term=term))
        for doc in res["hits"]["hits"]:
            print("Path:", doc["_source"]["path"])
            print("Title:", doc["_source"]["title"])
            print(doc["highlight"])
            print("-"*100)
