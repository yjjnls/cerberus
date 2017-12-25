# cerbero - a multi-platform build system for Open Source software
# Copyright (C) 2012 Andoni Morales Alastruey <ylatuya@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import logging
import subprocess
import shlex
import sys
import os
import tarfile
import zipfile
import tempfile
import time
import glob
import shutil
import hashlib
import cerbero

from cerbero.enums import Platform
from cerbero.utils import _, system_info, to_unixpath
from cerbero.utils import messages as m
from cerbero.errors import FatalError



def cmd(cmd, cmd_dir='.', fail=True, verbose=False):
    '''
    Run a shell (dos cmd.exe) command

    @param cmd: the command to run
    @type cmd: str
    @param cmd_dir: directory where the command will be run
    @param cmd_dir: str
    @param fail: whether or not to raise an exception if the command fails
    @type fail: bool
    '''
    from cerbero.utils.shell import StdOut
    LOGFILE = cerbero.utils.shell.LOGFILE
    DRY_RUN = cerbero.utils.shell.DRY_RUN

    try:
        if LOGFILE is None:
            if verbose:
                m.message("Running command '%s'" % cmd)
        else:
            LOGFILE.write("Running command '%s'\n" % cmd)
            LOGFILE.flush()
        shell = True
        stream = LOGFILE or sys.stdout
        if DRY_RUN:
            # write to sdterr so it's filtered more easilly
            m.error("cd %s && %s && cd %s" % (cmd_dir, cmd, os.getcwd()))
            ret = 0
        else:
            ret = subprocess.check_call(cmd, cwd=cmd_dir,
                                       stderr=subprocess.STDOUT,
                                       stdout=StdOut(stream),
                                       env=os.environ.copy(), shell=shell)
    except subprocess.CalledProcessError:
        if fail:
            raise FatalError(_("Error running command: %s") % cmd)
        else:
            ret = 0
    return ret


def cache(url , cache_dir='.', md5=None, NotCheck=False):
    '''
    cache the url to cache_dir ,and return new local file path
    raise exception
    '''
    from hacks.utils import MD5

    if os.path.exists(url):
        return url

    assert url.startswith('http'),'''
    url %s must be local exists file or http for setup
    '''%url

    

    basename = os.path.basename(url)
    if not os.path.exists(self.cache_dir):                
        os.makedirs(self.cache_dir)

    path = os.path.join(self.cache_dir,basename)
    if os.path.isfile(path):
        
        if NotCheck:
            return path
        
        if  md5 and md5 == MD5( path ):
            return path

        os.remove(path)

    assert not os.path.exists(path),'''
    failed remove %s,when we want update from %s
    '''%(path,url)

    shell.download( url, path)
    if md5:
        val = MD5(path)
        assert val == md5,'''
        error md5 check for %s
        expect : %s
        real : %s
        '''%(url,sha1,val)
    return path    