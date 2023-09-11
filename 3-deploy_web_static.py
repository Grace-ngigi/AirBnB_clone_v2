#!/usr/bin/python3
from fabric.api import env, run, put
from datetime import datetime
from os.path import exists


env.hosts = ['100.26.163.136', '54.209189.186']
env.user = 'ubuntu'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    # Get the current timestamp for the archive name
    now = datetime.utcnow()
    archive_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(now.year,
                                                                 now.month,
                                                                 now.day,
                                                                 now.hour,
                                                                 now.minute,
                                                                 now.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(archive_name)).failed is True:
        return None
    return archive_name


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
