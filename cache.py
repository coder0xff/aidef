import json
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Dict


CACHE_DIR = "ai"


@contextmanager
def cached(type: str, name: str, ext: str, meta: Dict[str, str], reldir: str = ""):
    entry = _CacheEntry(type, name, ext, meta, reldir)
    yield entry
    entry.save()

class _CacheEntry:
    def __init__(self, type: str, name: str, ext: str, meta: Dict[str, str], reldir: str):
        self._type = type
        self._name = name
        self._ext = ext
        self._meta = meta
        self._result = None
        self.has_value = False

        Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)
        self.file_name = os.path.join(CACHE_DIR, os.path.join(reldir, f"ai_{self._type}_{self._name}.{self._ext}"))
        self.json_name = self.file_name + ".meta"

        # if the cache file exists
        try:
            with open(self.file_name, "r") as cached:
                # and the json exists, and its contents match
                try:
                    with open(self.json_name, "r") as meta_file:
                        data = json.load(meta_file)
                        if data == self._meta:
                            # the result is cached
                            self.has_value = True
                except FileNotFoundError:
                    pass
        except FileNotFoundError:
            pass

    def set(self, result: str):
        self._result = result
        self.has_value = True
        return self

    def save(self):
        if not self.has_value or not self._result:
            return
        with open(self.file_name, "w") as cached:
            cached.write(self._result)
        with open(self.json_name, "w") as meta_file:
            json.dump(self._meta, meta_file)        
