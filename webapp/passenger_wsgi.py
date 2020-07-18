import os
import sys

from run import app as application

INTERP = "/home/eproject/anaconda3/envs/algo101/bin/python"
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

sys.path.extend([
    '/home2/eproject/veehuen/python/algo102/helpers',
    '/home2/eproject/veehuen/python/algo102/lib',
    '/home2/eproject/veehuen/python/algo102/webapp/app',
    '/home2/eproject/veehuen/python/algo102/webapp',
    '/home2/eproject/veehuen/python/algo102',
    '/home/eproject/veehuen/python/algo102'
])

if __name__ == "__main__":
    application.run()
    # Set this application constants here
    # with application.app_context():
    #     pass
