'Pin requires to their minimum allowed versions.'
from .projectinfo import ProjectInfo
from pathlib import Path
from venvpool import initlogging

def main():
    initlogging()
    info = ProjectInfo.seek('.')
    minreqs = [r.minstr() for r in info.parsedrequires()]
    with Path(info.projectdir, 'project.arid').open('a') as f:
        print(f"requires = $list({' '.join(minreqs)})", file = f)
    Path(info.projectdir, 'requirements.txt').write_text(''.join(f"{r}\n" for r in minreqs) if minreqs else '# This file blank.\n')

if '__main__' == __name__:
    main()
