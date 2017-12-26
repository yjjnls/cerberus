# Cerbero Package Manager ,Inspire by ArchLinux Pacman
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

from cerbero.commands import Command, register_command
from cerbero.build.cookbook import CookBook
from cerbero.build.oven import Oven
from cerbero.utils import _, N_, ArgparseArgument

from cerbero.utils import messages as m
from hacks.build.abstract import Abstract 

class Clear(Command):
    doc = N_('Clear install install files.')
    name = 'clear'

    def __init__(self, force=None, no_deps=None):
            args = [
                ArgparseArgument('name', nargs='*',
                    help=_('name of the package to clear'))
                ]
            
            Command.__init__(self, args)

    def run(self, config, args):
        for name in args.name:
            d = None
            if name == 'build-tools':
                d = config.build_tools_prefix

            if name == 'builds':
                d = config.prefix

            print 'remove %s at %s'%(name,d)
            if os.path.exists(d):
                import shutil
                shutil.rmtree(d)


   


register_command(Clear)
