from elasticsearch import Elasticsearch, helpers
from typing import List


class Indexer:
    def __init__(self):
        self.es_client = Elasticsearch("http://localhost:9200")

    def _split_text(self, text: List[str]):
        paragraphs = []
        st = 0
        for i, line in enumerate(text):
            if line.startswith("# ") and st != i:
                paragraphs.append(text[st:i])
                st = i
        if text:
            text[-1].rstrip()
        
        if st != 0:
            paragraphs.append(text[st:])
        return paragraphs
                

    def index(self):
        with open("./test.md", "r") as f:
            text = f.readlines()
        
        paragraphs = self._split_text(text)

        bulk_data = []
        for paragraph in paragraphs:
            bulk_data.append({
                "_index":"test",
                "_source":{
                    "title":paragraph[0][2:].strip(),
                    "content":"".join(paragraph).rstrip()
                }        
            })
        helpers.bulk(self.es_client, bulk_data)


if __name__ == "__main__":
    indexer = Indexer()
    indexer.index()