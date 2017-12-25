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
import sys
import re
import tempfile
import platform
import tarfile
import json    

from cerbero.build.cookbook import CookBook
#from cerbero.tools.cpm import Pack,Desc
from cerbero.packages.packagesstore import PackagesStore
from cerbero.packages.package import SDKPackage
from cerbero.utils import messages as m


class BuildSystem(object):
    _config =None
    _cookbook = None
    _store = None
    _SDKs=None
    _packages=None

    _BUILDs=None
    _PACKAGEs =None

    def __init__(self, config):
        if self._config is None:
            self._config = config
        else:
            assert self.config.arch == config.arch and \
            self.config.platform == config.platform

        assert config or self._config
        
        
    def cookbook(self):
        if self._cookbook is None:
            self._cookbook = CookBook(self._config)
        return self._cookbook

    def store(self):
        if self._store is None:
            self._store = PackagesStore(self._config)
        return self._store


    def _load(self):
        if self._BUILDs is None or self._PACKAGEs is None:
            store = self.store()
            self._BUILDs={}
            self._PACKAGEs={}

            for pkg in store.get_packages_list():
                if isinstance (pkg,SDKPackage):
                    self._BUILDs[pkg.name] = pkg
                else:
                    self._PACKAGEs[pkg.name] = pkg
        assert type(self._BUILDs) == type({}) and type(self._PACKAGEs) == type({})






    def recipe(self,name):
        
        return self.cookbook().get_recipe(name)

    def recipe_deps(self,name):
        deps={}
        for recipe in self.cookbook().list_recipe_deps(name):
            if recipe.name == name:
                continue
            deps[recipe.name]=recipe.version
        return deps

    def filename(self,name, package_type, ext='tar.bz2'):
        ''' filename of the build '''
        build = self.build(name)
        version = build.version



        prefix  = ''

        if self._config.build_type == 'debug' and \
           not name in ['build-tools','base','gstreamer'] :
           prefix = '@'

        return "%s%s-%s-%s-%s%s.%s" % (prefix, name,
                self._config.target_platform, self._config.target_arch,
                version, package_type, ext)
                
    def desc_filename(self,name):
        return self.filename(name,'','yaml')

    def builds(self):
        ''' dict of builds (key=build name, value object of Package'''
        self._load()
        return self._BUILDs

    def packages(self):
        self._load()
        return self._PACKAGEs

    def build(self,name):        
        return self.builds().get(name,None)

    def package(self,name):
        packages = self.packages()
        return packages.get(name,None)

    def packages_of_build(self,name):
        '''
        return the packages included in build (SDK) (not include depedens)
        '''
        build = self.build(name)
        pkgs=[]
        for (name, required, selected) in build.packages:
            pkg = self.package(name)
            pkgs.append( pkg )
        return pkgs

    def recipes_of_package(self,name):
        '''
        return the recipes included in packages (not include in deps packages)
        type is str NOT object of Recipe !!!
        '''
        package = self.package(name)
        assert package

        store = self.store()

        deps = store.get_package_deps( name, False)
        
        package = store.get_package(name)
        all = package.recipes_dependencies()
        
        rdeps=[]
        for pkg in store.get_package_deps( name):
            rdeps.extend( pkg.recipes_dependencies())
        return list(set(all).difference(set(rdeps)))

    def recipes_of_build(self,name):
        recipes=[]
        for pkg in self.packages_of_build( name ):
            recipes.extend(self.recipes_of_package(pkg.name))
        return recipes




    #
    # DEPRECATED !!!!!
    #





    def SDKs(self):
        if self._SDKs is None:
            store = self.store()
            self._SDKs={}
            pkgs={}
            #construct SDK tree first
            for pkg in store.get_packages_list():
                if not isinstance (pkg,SDKPackage):
                    pkgs[pkg.name] = pkg
                    continue
                self._SDKs[pkg.name] = pkg
            if self._packages is None:
                self._packages = pkgs
        return self._SDKs

    def Packages(self):
        if self._packages is None:
            sdk = self.SDKs()
            assert self._packages
        return self._packages


    def get_packages(self,name):
        ''' get SDK (build) packages '''
        pass
        

    def get_package_recipes(self,pkg_name, with_deps=False):
        ''' get package recipes '''
        store = self.store()

        deps = store.get_package_deps( pkg_name, False)
        
        package = store.get_package(pkg_name)
        all = package.recipes_dependencies()
        
        if not with_deps:
            for pkg in deps:
                print '*deps ',pkg.name
                r = pkg.recipes_dependencies()
                all = list(set(all).difference(set(r)))
        return all
        