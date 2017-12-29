
import cerbero.build.build
from hacks.build.cmake import AutoCMake
from cerbero.build.build import BuildType
BuildType.AUTOCMAKE = AutoCMake

import hacks.build.cookbook
from hacks.build.cookbook import CookBook,CookBookBase

cerbero.build.cookbook.CookBook = CookBook

#to support libssl-1_1-x64 format in windows
import platform
if platform.system() == "Windows":
    from cerbero.config import Platform
    from cerbero.build.filesprovider import FilesProvider
    FilesProvider._DLL_REGEX = r'^(lib)?{}(-[0-9]+)?([\-_][0-9]+)?(-x64)?\.dll$'
    FilesProvider.EXTENSIONS[Platform.WINDOWS]['sregex']=FilesProvider._DLL_REGEX

    from cerbero.utils import shell

    def _search_devel_libraries(self):
        devel_libs = []
        for category in self.categories:
            if category != self.LIBS_CAT and \
               not category.startswith(self.LIBS_CAT + '_'):
                continue

            pattern = 'lib/%(f)s.a lib/%(f)s.la '
            if self.platform == Platform.LINUX:
                pattern += 'lib/%(f)s.so '
            elif self.platform == Platform.WINDOWS:
                pattern += 'lib/%(f)s.dll.a '
                pattern += 'lib/%(f)s.def '
                pattern += 'lib/%(fnolib)s.lib '
                pattern += 'lib/%(f)s.lib '
            elif self.platform in [Platform.DARWIN, Platform.IOS]:
                pattern += 'lib/%(f)s.dylib '

            libsmatch = [pattern % {'f': x, 'fnolib': x[3:]} for x in
                         self._get_category_files_list(category)]
            devel_libs.extend(shell.ls_files(libsmatch, self.config.prefix))
        return devel_libs
    FilesProvider._search_devel_libraries = _search_devel_libraries
    
from hacks.build.oven import Oven

_old_cook_recipe = Oven._cook_recipe
def _cook_recipe(self, recipe, count, total):
    if not self.cookbook.recipe_needs_build(recipe.name) and \
            not self.force and \
            self.cookbook._installed_recipes.has_key(recipe.name):

        m.build_step(count, total, recipe.name, _("already installed"))
        return
    _old_cook_recipe(self, recipe, count, total)
