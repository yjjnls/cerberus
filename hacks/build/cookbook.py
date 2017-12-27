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

from collections import defaultdict
import os
import pickle
import time
import imp

import cerbero.build.cookbook

CookBookBase = cerbero.build.cookbook.CookBook


from cerbero.config import CONFIG_DIR, Platform, Architecture, Distro,\
    DistroVersion, License
from cerbero.build.build import BuildType
from cerbero.build.source import SourceType
from cerbero.errors import FatalError, RecipeNotFoundError, InvalidRecipeError,PackageNotFoundError
from cerbero.utils import _, shell, parse_file
from cerbero.utils import messages as m
from cerbero.build.recipe import Recipe,BuildSteps
from cerbero.build.cookbook import RecipeStatus 

class CookBook (CookBookBase):
    '''
    Stores a list of recipes and their build status saving it's state to a
    cache file

    @ivar recipes: dictionary with L{cerbero.recipe.Recipe} availables
    @type recipes: dict
    @ivar status: dictionary with the L{cerbero.cookbook.RecipeStatus}
    @type status: dict
    '''

    RECIPE_EXT = '.recipe'

    def __init__(self, config, load=True):
        CookBookBase.__init__(self,config,load)
        self._installed_recipes=None

    

    def get_recipe(self, name):
        '''
        Gets a recipe from its name

        @param name: name of the recipe
        @type name: str
        '''
        try :
            CookBookBase.get_recipe(self,name)

            status = self.status.get(name,None)

            # user never build such recipe
            if status is None or not BuildSteps.COMPILE in status.steps:
                version = self.recipe_version_from_installation(name)

                # user installed such recipe and same version, then
                # we make the recipe as 'built' to avoid build again
                if version and version == self.recipes[name].version:
                    self.status[name] = RecipeStatus(None, 
                    steps=[BuildSteps.INSTALL,BuildSteps.POST_INSTALL],
                    needs_build=False,
                    built_version = version )

        except RecipeNotFoundError, e:
            print 'RecipeNotFoundError'
            # a recipe not include in recipes folder, but installed
            # we fake one to let build continue
            version = self.recipe_version_from_installation(name)
            if version:
                r = Recipe(self._config)
                r.name = name
                r.version = version
                self.status[name] = RecipeStatus(None, 
                    steps=[BuildSteps.INSTALL,BuildSteps.POST_INSTALL],
                    needs_build=False,
                    built_version = version )


        return self.recipes[name]

    def _load_recipes_from_dir(self, repo):
        recipes = {}
        recipes_files = shell.find_files('*/*%s' % self.RECIPE_EXT, repo)
        recipes_files.extend(shell.find_files('*/*/*%s' % self.RECIPE_EXT, repo))
        try:
            custom = None
            m_path = os.path.join(repo, 'custom.py')
            if os.path.exists(m_path):
                custom = imp.load_source('custom', m_path)
        except Exception:
            custom = None
        for f in recipes_files:
            # Try to load the custom.py module located in the recipes dir
            # which can contain private classes to extend cerbero's recipes
            # and reuse them in our private repository
            try:
                recipe = self._load_recipe_from_file(f, custom)
            except RecipeNotFoundError:
                m.warning(_("Could not found a valid recipe in %s") % f)
            if recipe is None:
                continue
            recipes[recipe.name] = recipe
        return recipes

    def recipe_version_from_installation(self,name):
        instd = os.path.join(self._config.prefix)
        if not os.path.exists(instd):
            return None
        import glob

        if self._installed_recipes is None:
            self._installed_recipes={}
            for filename in  glob.glob( instd +'/*.yaml'):
                import yaml
                f = open(filename,'r')
                desc = yaml.load(f)
                f.close()

                if desc.has_key('recipes'):
                    self._installed_recipes.update(desc['recipes'])

        return self._installed_recipes.get(name,None)
        



