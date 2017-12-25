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
from hacks.cpm.utils import SHA1
from hacks.cpm.buildsystem import BuildSystem
from hacks.cpm.packager import  Description,Component,PkgFile
from hacks.cpm.packager import  Pack as MakePackage
from hacks.build.abstract import Abstract 

class AbstractCommand(Command):
    doc = N_('Generate abstract for package')
    name = 'abstract'

    def __init__(self, force=None, no_deps=None):
            args = [
                ArgparseArgument('name', nargs='*',
                    help=_('name of the package to generate abstract')),

                ArgparseArgument('--output-dir', type=str,
                    default='.',
                    help=_('directory of package stored'))
                ]
            
            Command.__init__(self, args)

    def run(self, config, args):
        import datetime

        start = datetime.datetime.now()

        abst = Abstract( config )
        for name in args.name:
            print name,'**'
            desc = abst.dump( name, args.output_dir)
            filename = abst.fullname(name) + '.yaml'
            path = os.path.join(args.output_dir,filename)
            import yaml
            f = open( path,'w')
            yaml.dump( desc, f ,default_flow_style=False)
            f.close()

   


register_command(AbstractCommand)