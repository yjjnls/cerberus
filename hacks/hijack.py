import os
import sys
import platform
import tempfile
import cerbero

try:
    import yaml
except ImportError, e:
    print "Could not import yaml. Try installing it with "\
          "'pip install pyyaml"
    raise e

_origin_os_path_expanduser = os.path.expanduser
_origin_os_path_abspath = os.path.abspath
_origin_os_path_realpath = os.path.realpath
_origin_os_path_relpath = os.path.relpath

from cerbero import hacks
def _relpath(path,start='.'):
    #recover abspath
    os.path.abspath = _origin_os_path_abspath
    ret = _origin_os_path_relpath(path,start)
    os.path.abspath = _origin_os_path_abspath
    return ret

if platform.system() == 'Windows':
    os.path.relpath = _relpath

from cerbero.utils import shell

import hacks.utils.hijack
import hacks.build.hijack
import cerbero.commands
_origin_load_commands=cerbero.commands.load_commands
#----------------------------------------------#
#       hijack commands of cerbero             #
#----------------------------------------------#
def _load_commands(subparsers):
    ''' hijack commands of cerbero
    '''
    from cerbero.utils import messages as m

    _origin_load_commands(subparsers)

    
    
    commands_dir = os.path.abspath(os.path.dirname(__file__)+'/commands')

    for name in os.listdir(commands_dir):
        name, extension = os.path.splitext(name)
        if extension != '.py':
            continue
        try:
            __import__('hacks.commands.%s' % name)
        except ImportError, e:
            m.warning("Error importing command %s:\n %s" % (name, e))
    for command in cerbero.commands._commands.values():
        command.add_parser(subparsers)

cerbero.commands.load_commands = _load_commands

#hijack 
def _get_name(self, package_type, ext='tar.bz2'):
    prefix=''
    if self.config.build_type == 'debug':
        prefix = '@'

    return "%s%s-%s-%s-%s%s.%s" % (prefix, self.package.name,
            self.config.target_platform, self.config.target_arch,
            self.package.version, package_type, ext)

from cerbero.packages.disttarball import DistTarball
DistTarball._get_name = _get_name

#
#
import hacks.tools
import hacks.tools.mswin
import hacks.tools.MSVSVersion
import cerbero.tools
cerbero.tools.mswin = hacks.tools.mswin
cerbero.tools.MSVSVersion = hacks.tools.MSVSVersion

#Config
import cerbero.config
cerbero.config.Config._properties.append('build_type')
_originConfig_load_defaults=cerbero.config.Config.load_defaults
def _load_defaults(self):
    self.set_property('build_type', 'release')
    _originConfig_load_defaults(self)
    self.interactive = False
    if platform.system() == 'Windows':
        self.toolchain_prefix = 'c:/MinGW/w64'
    

    CERBERUS_CACHED_SOURCES = os.environ.get('CERBERUS_CACHED_SOURCES')
    if CERBERUS_CACHED_SOURCES and os.path.isdir(CERBERUS_CACHED_SOURCES):
        self.cached_sources = CERBERUS_CACHED_SOURCES

    rootd = os.path.abspath( os.path.dirname(__file__) + '/..')

    self.recipes_dir = os.path.join( rootd ,'recipes' )
    self.packages_dir = os.path.join( rootd ,'packages' )

def _default_home_dir(self):
    if self.uninstalled:
        p = os.path.join(os.path.dirname(__file__), '..', 'build')
    else:
        p = os.path.expanduser('~/cerbero')
    return os.path.abspath(p)
def _relative_path(self, path):
    if not self.uninstalled:
        p = os.path.join(self.data_dir, path)
    else:
        p = os.path.join(os.path.dirname(__file__), '..', path)
    return os.path.abspath(p)
    
cerbero.config.Config._default_home_dir = _default_home_dir
cerbero.config.Config._relative_path = _relative_path

cerbero.config.Config.load_defaults = _load_defaults

