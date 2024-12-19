from git import Git
from indexer import Indexer
from utils import parse_repo_name_from_url
from config.config import config


class Pipeline:
    def __init__(self):
        self._clone_path = f"./clone/{parse_repo_name_from_url(config.git_repo)}"
        self._git = Git(self._clone_path)
        self._indexer = Indexer(self._clone_path)
    
    def _pull_files(self):
        try:
            self._git.clone()
        except FileExistsError:
            self._git.pull()
    
    def run(self):
        # self._pull_files()
        self._indexer.index()


if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run()
