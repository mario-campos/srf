#!/usr/bin/env python

import fnmatch
import json
import sys

def main(input, pattern, invert=False):
    sarif_file = json.loads(input.read())

    for run in sarif_file['runs']:
        for result in run['results'][:]:
            for location in result['locations']:
                filepath = location['physicalLocation']['artifactLocation']['uri']
                if invert == fnmatch.fnmatchcase(filepath, pattern):
                    run['results'].remove(result)
                    break

    print(json.dumps(sarif_file))

if __name__ == '__main__':
    if len(sys.argv) not in [2,3,4]:
        print(f'usage: {sys.argv[0]} [-v] <pattern> [<filename>]', file=sys.stderr)
        sys.exit(1)

    # ./sarif-grep.py <pattern>
    if len(sys.argv) == 2:
        main(sys.stdin, sys.argv[1])

    elif len(sys.argv) == 3:
        # ./sarif-grep.py -v <pattern>
        if sys.argv[1] == '-v':
            main(sys.stdin, sys.argv[2], True)

        # ./sarif-grep.py <pattern> <file>
        else:
            main(open(sys.argv[2]), sys.argv[1])

    # ./sarif-grep.py -v <pattern> <file>
    else:
        main(open(sys.argv[3]), sys.argv[2], True)
