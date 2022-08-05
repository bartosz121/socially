import os

class RemoveFileMixin:
    def remove_file(self, path: str):
        if os.path.isfile(path):
            os.remove(path)