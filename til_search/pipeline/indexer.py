import os

from elasticsearch import Elasticsearch, helpers

from model.document import Document
from markdown_parser import MarkdownParser
from til_search.config.config import config


class Indexer:

    def __init__(self, clone_path: str):
        self._es_client = Elasticsearch(config.elasticsearch_urls)
        self._clone_path = clone_path
        self._parser = MarkdownParser()
        self._tmp = set()

    def _index(self, docs: list[Document]):
        bulk_data = []
        for doc in docs:
            bulk_data.append({
                "_index": config.index_name,
                "_id": doc.id,
                "_source": doc.model_dump_json(exclude=["id"])})
        helpers.bulk(self._es_client, bulk_data)
    
    def index(self, path: str=""):
        for sub_path in os.listdir(f"{self._clone_path}{path}"):
            new_path = f"{self._clone_path}{path}/{sub_path}"
            if os.path.isdir(new_path):
                self.index(path + "/" +sub_path)
            else:
                if new_path.endswith(".md") and not new_path.endswith("README.md"):
                    self._index(self._parser.parse(f"{path}/{sub_path}", new_path))