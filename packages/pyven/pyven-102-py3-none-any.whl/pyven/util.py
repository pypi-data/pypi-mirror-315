from contextlib import contextmanager
import os, re, sys

pyversiontags = {2: ['2'], 3: ['3.9', '3.10', '3.11', '3.12', '3.13']}

def stderr(obj):
    sys.stderr.write(str(obj))
    sys.stderr.write(os.linesep)

class Excludes:

    def __init__(self, globs):
        def disjunction():
            sep = re.escape(os.sep)
            star = f"[^{sep}]*"
            def components():
                for word in glob.split('/'):
                    if '**' == word:
                        yield f"(?:{star}{sep})*"
                    else:
                        yield star.join(re.escape(part) for part in word.split('*'))
                        yield sep
            for glob in globs:
                concat = ''.join(components())
                assert concat.endswith(sep)
                yield concat[:-len(sep)]
        self.pattern = re.compile(f"^{'|'.join(disjunction())}$")

    def __contains__(self, relpath):
        return self.pattern.search(relpath) is not None

class Seek(str):

    @classmethod
    def seek(cls, dirpath, name):
        while True:
            path = cls(os.path.join(dirpath, name))
            if os.path.exists(path):
                path.parent = dirpath
                return path
            parent = os.path.join(dirpath, '..')
            if os.path.abspath(parent) == os.path.abspath(dirpath):
                break
            dirpath = parent

@contextmanager
def bgcontainer(*dockerrunargs):
    from lagoon import docker
    from lagoon.program import NOEOL
    container = docker.run._d[NOEOL](*dockerrunargs + ('sleep', 'inf'))
    try:
        yield container
    finally:
        docker.rm._f[print](container)

def initapt(dockerexec):
    dockerexec('mkdir', '-pv', '/etc/apt/keyrings')
    dockerexec('curl', '-fsSL', 'https://download.docker.com/linux/debian/gpg', '-o', '/etc/apt/keyrings/docker.asc')
    dockerexec('sh', '-c', 'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list')
