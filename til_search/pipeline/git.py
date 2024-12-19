import os
import subprocess

from config.config import config


class Git:

    def __init__(self, clone_path: str):
        self._clone_path = clone_path
    
    def clone(self):
        clone_path = self._clone_path
        if os.path.exists(clone_path):
            raise FileExistsError
        subprocess.run(["git", "clone", config.git_repo, clone_path])

    def pull(self):
        subprocess.run(["git", "pull", "origin", config.branch], cwd=self._clone_path)
        

