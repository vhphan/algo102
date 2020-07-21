import os
import sys

from run import app as application

INTERP = "/home/eproject/anaconda3/envs/algo101/bin/python"
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)
algo102_path = '/home/eproject/vee-h-phan.com/algo102'
sys.path.extend([
    f'{algo102_path}/helpers',
    f'{algo102_path}/lib',
    f'{algo102_path}/webapp/app',
    f'{algo102_path}/webapp',
    f'{algo102_path}',
])

if __name__ == "__main__":
    application.run()
    # Set this application constants here
    # with application.app_context():
    #     pass
