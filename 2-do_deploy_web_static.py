#!/usr/bin/python3
""" Deploying Archive"""

from fabric.api import env, run, put
import os

env.hosts = ['100.26.163.136', '54.209.189.186']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distribute an archive to web servers and deploy it.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Get the archive filename without extension
        archive_filename = os.path.basename(archive_path)
        archive_name_noext = os.path.splitext(archive_filename)[0]

        # Create the directory structure for deployment
        release_folder = '/data/web_static/releases/' + archive_name_noext
        run('mkdir -p {}'.format(release_folder))

        # Uncompress the archive to the release folder
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_folder))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Create a new symbolic link
        current_link = '/data/web_static/current'
        run('rm -f {}'.format(current_link))
        run('ln -s {} {}'.format(release_folder, current_link))

        print('New version deployed!')
        return True
    except Exception as e:
        print('Deployment failed:', e)
        return False
