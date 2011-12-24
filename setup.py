import os
import sys

usage = """setup.py <command>
  - clear: remove unnecessary files
"""

def clean():
    patterns = ['MANIFEST', '*~', '*flymake*', '*.pyc', '*.h']
    cwd = os.getcwd()
    import fnmatch
    for path, subdirs, files in os.walk(cwd):
        for pattern in patterns:
            matches = fnmatch.filter(files, pattern)
            if matches:
                def delete(p):
                    print 'removing %s' % p
                    os.remove(p)
                map(delete ,[os.path.join(path, m) for m in matches])

if __name__ == '__main__':
    actions = {'clean': clean}

    if len(sys.argv) < 2 or sys.argv[1] not in actions:
        print usage
        sys.exit(1)

    actions[sys.argv[1]]()
