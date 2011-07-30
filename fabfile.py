
import os

from fabric.api import *


PROJECT_DIRNAME = "/home/dash/%s" % os.path.dirname(os.path.abspath(
                                        __file__)).split(os.sep)[-1]

env.user = "dash"
env.hosts = ["drawnby.jupo.org"]


def push():
    local("hg push")

def pull():
    with cd(PROJECT_DIRNAME):
        run("hg pull")
        run("hg up -C")

def migrate():
    with cd(PROJECT_DIRNAME):
        run("python manage.py syncdb")
        run("python manage.py migrate")

def install():
    with cd(PROJECT_DIRNAME):
        sudo("pip install -r requirements.txt")

def restart():
    with cd(PROJECT_DIRNAME):
        run("supervisorctl restart drawnby_app")

def deploy():
    push()
    pull()
    install()
    migrate()
    restart()
