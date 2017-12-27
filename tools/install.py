import urllib2
import sys
import subprocess
import os
def download(url, filename ):
    print 'download %s => %s'%(url,filename)
    u = urllib2.urlopen(url)  
    f = open(filename, 'wb')  
    meta = u.info()  
    size = int(meta.getheaders("Content-Length")[0])  
    n = 0 
    while True:  
        buffer = u.read(8192)  
        if not buffer:
            break 
        
        n += len(buffer)  
        f.write(buffer)  
        per = 40*n/size
        bar='='*per
        space=' '*(40-per)

        print '\r [%s%s] %2.2f%%'%(bar,space,100*n/size) , 
    f.close()  
    print 'Done'
    

def unzip(filename,output_dir):
    import zipfile
    print 'unzip %s => %s'%(filename,output_dir)
    azip = zipfile.ZipFile(filename)
    azip.extractall(output_dir)


class StdOut:

    def __init__(self, stream=sys.stdout):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)

def cmd(cmd, cmd_dir='.'):
    ret = subprocess.check_call(cmd, cwd=cmd_dir,
                                stderr=subprocess.STDOUT,
                                stdout=StdOut(sys.stdout),
                                env=os.environ.copy(), shell=True)
    return ret

def bash(cmd, cmd_dir='.'):
    env=os.environ.copy()
    env['PATH']='c:/MinGW/msys/1.0/bin;'+env['PATH']
    ret = subprocess.check_call('bash.exe -c "%s" '%cmd, cwd=cmd_dir,
                                stderr=subprocess.STDOUT,
                                stdout=StdOut(sys.stdout),
                                env=env, shell=True)
def Check():
    print '''
       checking for tools
    '''
    cmd('cmake --version')
    cmd('git --version')

__WD__=os.path.abspath( os.getcwd() )
__TMP__=os.path.join(__WD__,'~tmp')

if not os.path.exists(__TMP__):
    os.makedirs(__TMP__)

def MinGW():
    os.chdir(__TMP__)
    if not os.path.exists('c:/MinGW'):
        tarball = os.path.join(__TMP__,'MinGW.zip')
        download('http://172.16.0.119/WMS/mirrors/cerbero/toolchain/MinGW.zip',tarball)
        unzip(tarball,'c:/')

        for pkg in ['mingw-developer-toolkit',
                    'msys-base','msys-wget',
                    'msys-flex','msys-bison','msys-perl' ]:

            cmd('mingw-get install %s'%pkg, 'c:/MinGW/bin')

    if not os.path.exists('c:/MinGW/w64'):
        tarball = os.path.join(__TMP__,'w64.zip')
        download('http://172.16.0.119/WMS/mirrors/cerbero/toolchain/w64.zip',tarball)
        unzip(tarball,'c:/MinGW')
    os.chdir(__WD__)

def PythonMdoules():
    os.chdir(__TMP__)
    try:
        import gyp
    except:
        cmd('git clone https://github.com/Mingyiz/gyp.git')
        cmd('python setup.py install','gyp')

    try:
        import yaml
    except:
        cmd('git clone https://github.com/yaml/pyyaml.git')
        cmd('python setup.py install','pyyaml')
    os.chdir(__WD__)
print '''
    ================================================

          Install cerbero build enviroment

    ================================================
'''
Check()
MinGW()
PythonMdoules()
if not os.path.exists('./cerberus'):
    cmd('git clone https://github.com/Mingyiz/cerberus.git --recursive')

print "Install Success!!"
cmd('start bash.bat','./cerberus')
