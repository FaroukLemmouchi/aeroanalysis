#!/usr/bin/python3.6
import sys
#mode = sys.argv[1]

from aeros5p_analysis.index import server as app
if __name__ == '__main__':
    app.run()
