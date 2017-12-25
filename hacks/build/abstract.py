


import os
import sys
import re
import tempfile
import platform
import tarfile
import json  

from cerbero.build.cookbook import CookBook
from cerbero.packages.packagesstore import PackagesStore
from cerbero.packages.package import SDKPackage
from cerbero.utils import messages as m
from cerbero.utils import shell

from cerbero.packages import PackageType
from cerbero.packages.disttarball import DistTarball
from hacks.utils import MD5
from cerbero.errors import FatalError

#
# Build is SDK
#


class Abstract(object):



    def __init__(self,config ):
        self.config = config

    def __getattr__(self, name):
        if name not in self.__dict__:
            
            if name == 'store':
                self.__dict__[name] =PackagesStore(self.config)

            if name == 'cookbook':
                self.__dict__[name] = CookBook(self.config)
                
        return self.__dict__[name]


    def sdk(self,name):
        for pkg in self.store.get_packages_list():
            print pkg.name,isinstance (pkg,SDKPackage),'@',pkg.name == name

            if isinstance (pkg,SDKPackage) and pkg.name == name:
                return pkg
        return None

    def package(self,name):
        for pkg in self.store.get_packages_list():

            if pkg.name == name:
                return pkg
        return None

    def recipes_of_package(self,name):
        '''
        return the recipes included in packages (not include in deps packages)
        type is str NOT object of Recipe !!!
        '''
        
        package = self.store.get_package(name)
        all = package.recipes_dependencies()
        
        rdeps=[]
        for pkg in self.store.get_package_deps( name):
            rdeps.extend( pkg.recipes_dependencies())
        return list(set(all).difference(set(rdeps)))

    def packages_of_sdk(self,name):
        '''
        return the packages included in build (SDK) (not include depedens)
        '''
        sdk = self.sdk(name)
        pkgs=[]
        for (name, required, selected) in sdk.packages:
            pkg = self.package(name)
            pkgs.append( pkg )
        return pkgs

    def recipes_of_package(self,name):
        '''
        return the recipes included in packages (not include in deps packages)
        type is str NOT object of Recipe !!!
        '''

        deps = self.store.get_package_deps( name, False)
        
        package = self.store.get_package(name)
        all = package.recipes_dependencies()
        
        rdeps=[]
        for pkg in self.store.get_package_deps( name):
            rdeps.extend( pkg.recipes_dependencies())
        return list(set(all).difference(set(rdeps)))

    def recipes_of_sdk(self,name):
        recipes=[]
        for pkg in self.packages_of_sdk( name ):
            recipes.extend(self.recipes_of_package(pkg.name))
        return recipes

    def recipe(self,name):        
        return self.cookbook.get_recipe(name)
        
    def fullname(self,name):
        '''
        fullname use for filename of this abstract
        '''
        prefix=''
        if self.config.build_type == 'debug':
            prefix = '@'

        if name in ['build-tools','base','gstreamer']:
            prefix =''
            
        sdk = self.sdk(name)
        return "%s%s-%s-%s-%s" % (prefix, sdk.name,
            self.config.target_platform, self.config.target_arch,
            sdk.version)



    def dump(self,name, output_dir = '.'):
        sdk = self.sdk(name)
        desc={
            'name':name,
            'version':sdk.version,
            'platform':self.config.target_platform,
            'arch':self.config.target_arch,
            'recipes':[],
            'commit': self.commit()
        }

        for rname in self.recipes_of_sdk(name):
            recipe = self.recipe(rname)
            desc['recipes'].append({
                'name':rname,
                'version': recipe.version            
            })

        tarball = DistTarball(self.config,sdk,self.store)

        files=[]
        for ptype in [PackageType.DEVEL,PackageType.RUNTIME]:
            TNAME={PackageType.DEVEL:'devel',PackageType.RUNTIME:'runtime'}

            filename = tarball._get_name(ptype)
            path = os.path.join( output_dir,filename)
            if os.path.exists( path ):
                files.append({ filename : {                    
                    'type': TNAME[ptype],
                    'MD5Sum': MD5(path)
                }})
            else:
                if (name == 'build-tools') and (ptype == PackageType.DEVEL):
                    continue # build-tools has no devel package

                reason = "abstract %s, but no %s package at %s"%(name,TNAME[ptype],path)
                m.error( reason )
                raise FatalError(reason)

        desc['packages']=files
        if name == 'build-tools':
            desc['prefix']=self.config.build_tools_prefix
        else:
            desc['prefix']=self.config.prefix
        
        return desc
        

    
    def commit(self):
        rootd = os.path.join( os.path.dirname(__file__),'../..' )
        rootd = os.path.abspath( rootd )

        commit = shell.check_call('git rev-parse HEAD',rootd).strip()
        tag = shell.check_call('git tag --contain %s'%commit,rootd).strip()
        branch = shell.check_call('git branch',rootd).strip('*').strip()
        return {
            'commit':commit,
            'branch':branch,
            'tag':tag
        }




    def test(self):
        info = self.dump('base')
        print info

        


 