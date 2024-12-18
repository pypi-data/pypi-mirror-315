'Check last release can be installed from PyPI and its tests still pass, for use by CI.'
from .checks import EveryVersion
from .projectinfo import ProjectInfo
from .util import bgcontainer, initapt, pyversiontags
from lagoon import git
from lagoon.program import partial
from urllib.request import urlopen
from venvpool import initlogging
import logging, xml.etree.ElementTree as ET

log = logging.getLogger(__name__)

def main():
    from lagoon import docker
    initlogging()
    headinfo = ProjectInfo.seek('.')
    if not headinfo.config.pypi.participant: # XXX: Or look for tags?
        log.info('Not user-installable.')
        return
    project = headinfo.config.name
    # XXX: When building a tag use that same version?
    with urlopen(f"https://pypi.org/rss/project/{project}/releases.xml") as f:
        version = ET.parse(f).find('./channel/item/title').text
    req = f"{project}=={version}"
    upstream_devel_packages = list(headinfo.config.upstream.devel.packages)
    for pyversion in reversed(pyversiontags[3]): # XXX: Why only 3?
        log.info("Python version: %s", pyversion)
        with bgcontainer(f"python:{pyversion}") as container:
            containerexec = docker.exec[partial, print](container)
            if upstream_devel_packages:
                initapt(containerexec)
                containerexec('apt-get', 'update')
                containerexec('apt-get', 'install', '-y', *upstream_devel_packages)
            containerexec('pip', 'install', req)
    git.checkout[print](f"v{version}")
    EveryVersion(ProjectInfo.seek('.'), False, False, [], True, True).nose()

if '__main__' == __name__:
    main()
