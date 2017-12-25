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


import os
import hashlib
import yaml

from cerbero.commands import Command, register_command
from cerbero.build.cookbook import CookBook
from cerbero.build.oven import Oven
from cerbero.utils import _, N_, ArgparseArgument ,shell
from cerbero.utils import messages as m

from hacks.build.abstract import Abstract
from hacks.utils.shell import cache



class Installer(Command):
    doc = N_('Install componet/build/bundler .')
    name = 'install'

    def __init__(self, force=None, no_deps=None):
        args = [
            ArgparseArgument('name', nargs='*',
                help=_('name of the elements to be installed')),

            ArgparseArgument('--repo', type=str,                    
                help=_('respsitory of the objects stored')),
                

            ArgparseArgument('--cache-dir', type=str, default='',
                help=_('directory where dowanlod packaged to store'))

            ]
        
        Command.__init__(self, args)

    def run(self, config, args):
        abst = Abstract(config)        

        for name in args.name:
            prefix = config.prefix
            if name == 'build-tools':
                prefix = config.build_tools_prefix
            
            filename = abst.fullname(name) + '.yaml'
            url = os.path.join( args.repo , filename )
            path = cache( url, args.cache_dir )

            desc = yaml.load( open( path ) )
            
            for pkg in desc['packages']:
                for pkgname , prop in pkg.viewitems():
                    url = os.path.join( args.repo , pkgname )
                    tarball = cache(url,args.cache_dir,md5=prop['MD5Sum'] )

                    #install                    
                    shell.unpack( tarball, prefix)
            #write abstract
            path = os.path.join(prefix,name + '.yaml')

            f = open(path,'w')
            yaml.dump(desc,f)
            f.close()

        return






register_command(Installer)
