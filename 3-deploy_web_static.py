#!/usr/bin/python3
from fabric.api import env, run, put
from datetime import datetime
from os.path import exists


env.hosts = ['100.26.163.136', '54.209189.186']
env.user = 'ubuntu'


def do_pack():
    # Your do_pack code as provided in 1-pack_web_static.py

    def do_deploy(archive_path):
        # Your do_deploy code as provided in 2-deploy_web_static.py

        def deploy():
            """
            Create and distribute an archive to web servers.
            """
    # Create the archive
    archive_path = do_pack()

    # Check if an archive has been created
    if not archive_path:
        return False

    # Deploy the archive to web servers
    return do_deploy(archive_path)
