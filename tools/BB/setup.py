import urllib2
import sys
import subprocess
import os
import yaml
import tarfile
import bz2

__BB__='BB1-2'
#__repo__='http://172.16.0.119/WMS/mirrors/cerbero'
__repo__='D:/cerberus/releases'
__instd__='c:/wms/%s'%__BB__
__cached__='%s/download'%__instd__

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

def MD5(fileMd5):
    import hashlib
    md5_value = hashlib.md5()
    with open(fileMd5,'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            md5_value.update(data)
    return md5_value.hexdigest()


def cache(url , cache_dir='.', md5=None, NotCheck=False):
    '''
    cache the url to cache_dir ,and return new local file path
    raise exception
    '''
    if os.path.exists(url):
        return url

    assert url.startswith('http'),'''
    url %s must be local exists file or http for setup
    '''%url

    basename = os.path.basename(url)
    if not os.path.exists(cache_dir):
        print 'cacd ', cache_dir
        os.makedirs(cache_dir)

    path = os.path.join(cache_dir,basename)
    if os.path.isfile(path):
        
        if NotCheck:
            return path
        
        if  md5 and md5 == MD5( path ):
            return path

        os.remove(path)

    assert not os.path.exists(path),'''
    failed remove %s,when we want update from %s
    '''%(path,url)

    import cerbero.utils.shell

    download( url, path)
    if md5:
        val = MD5(path)
        assert val == md5,'''
        error md5 check for %s
        expect : %s
        real : %s
        '''%(url,sha1,val)
    return path    


def unbz2(filename,output_dir):
    archive = tarfile.open(filename,'r:bz2')
    archive.extractall(output_dir)
    archive.close()

if not os.path.exists(__instd__):
    os.makedirs(__instd__)

if not os.path.exists(__cached__):
    os.makedirs(__cached__)

release_file = cache('%s/%s/release.yaml'%(__repo__,__BB__),__cached__)

release = yaml.load( open(release_file) )

for name,build in release['package'].viewitems():
    #description filename

    print build
    print '=========='
    durl = os.path.join(__repo__,__BB__,build['desc'])
    print durl
    dfile = cache(durl)
    desc = yaml.load(open(dfile))

    for pkg in desc['packages']:
        for pkgname , prop in pkg.viewitems():
            if prop['type'] != 'runtime':
                continue
            url = os.path.join( __repo__,__BB__ , pkgname )
            tarball = cache(url,__cached__,md5=prop['MD5Sum'] )
            unbz2(tarball,__instd__)
print '''
   Install success !
'''
