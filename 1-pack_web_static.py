#!/usr/bin/python3
<<<<<<< HEAD
'''Fabric the script to generate the .tgz archive'''

from fabric.api import local
from datetime import datetime

from fabric.decorators import runs_once
=======
"""Fabric script that generates a .tgz archive."""
import os
from datetime import datetime
from fabric.api import local, runs_once
>>>>>>> 855e1594e620874ebcbc7ecab6055a6839e634c5


@runs_once
def do_pack():
<<<<<<< HEAD
    '''generating the .tgz archive from contents of a web_static folder'''
    local("mkdir -p versions")
    path = ("versions/web_static_{}.tgz"
            .format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")))
    result = local("tar -cvzf {} web_static"
                   .format(path))

    if result.failed:
        return None
    return path
=======
    """Protatype to archive static files."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    d_time = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        d_time.year,
        d_time.month,
        d_time.day,
        d_time.hour,
        d_time.minute,
        d_time.second
    )
    try:
        print("Packing web_static to {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, size))
    except Exception:
        output = None
    return output
>>>>>>> 855e1594e620874ebcbc7ecab6055a6839e634c5
