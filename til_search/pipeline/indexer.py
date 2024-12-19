import os
import hashlib

from elasticsearch import Elasticsearch, helpers

from markdown_parser import MarkdownParser
from config.config import config


class Indexer:

    def __init__(self, clone_path: str):
        self._es_client = Elasticsearch(config.elasticsearch_urls)
        self._clone_path = clone_path
        self._parser = MarkdownParser()
        self._tmp = set()

    def _index(self, path, docs: list[dict]):
        bulk_data = []
        for doc in docs:
            doc["path"] = path
            bulk_data.append({
                "_index":"markdown_search",
                "_id": hashlib.sha256(("".join(doc["title"])+path).encode()).hexdigest(),
                "_source": doc})
        helpers.bulk(self._es_client, bulk_data)
    
    def index(self, path: str=""):
        for sub_path in os.listdir(f"{self._clone_path}{path}"):
            new_path = f"{self._clone_path}{path}/{sub_path}"
            if os.path.isdir(new_path):
                self.index(path + "/" +sub_path)
            else:
                if new_path.endswith(".md") and not new_path.endswith("README.md"):
                    self._index(f"{path}/{sub_path}", self._parser.parse(new_path))