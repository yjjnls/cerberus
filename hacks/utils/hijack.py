import os
import hacks
from cerbero.utils import shell
from cerbero.utils import messages as m


#to avoid download warning 
_old_shell_download=shell.download        
def hijacked_download(url, destination=None, recursive=False, check_cert=True, overwrite=False):
    check_cert = False
    _old_shell_download( url,destination,recursive,check_cert,overwrite)


shell.download = hijacked_download

import hacks.utils.shell
shell.cmd = hacks.utils.shell.cmd

shell.enter_build_environment = hacks.utils.shell.enter_build_environment