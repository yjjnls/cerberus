#__config__='config/win64.cbc'
function cerbero(){
   ./cerbero-uninstalled -c ${__config__} $@
   if [ $? -ne 0 ]; then
      echo "Failed run command ./cerbero-uninstalled -c ${__config__} $@"
      exit 1
   fi

    
}
git config --global user.name "Mingyi Zhang"
git config --global user.email "mingyi.z@outlook.com"

[ ! -d releases ] && mkdir releases
export CERBERUS_CACHED_SOURCES='z:/share/cerbero/cerbero-1.12.3/sources'



function build_tools(){

echo "====================="
echo "    build-tools "
echo "====================="
export __config__='config/win64.cbc'
cerbero clear build-tools builds
cerbero bootstrap --build-tools-only 
cerbero tar-build-tools --output-dir releases
cerbero abstract build-tools --output-dir releases

}

function base(){

echo "====================="
echo "    base "
echo "====================="
export __config__='config/win64.cbc'
cerbero clear build-tools builds
cerbero install build-tools --repo releases
cerbero package base --tarball --output-dir releases
cerbero abstract base --output-dir releases

}

function gstreamer(){

echo "====================="
echo "    gstreamer "
echo "====================="

export __config__='config/win64.cbc'
cerbero clear build-tools builds
cerbero install build-tools --repo releases
cerbero install base --repo releases
cerbero package gstreamer --tarball --output-dir releases
cerbero abstract gstreamer --output-dir releases

}

function ribbon(){

echo "====================="
echo "    ribbon  "
echo "====================="

export __config__='config/win64.cbc'
cerbero clear build-tools builds
cerbero install build-tools --repo releases
cerbero install base --repo releases
cerbero install gstreamer --repo releases
cerbero package ribbon --tarball --output-dir releases
cerbero abstract ribbon --output-dir releases

}
function ribbon_debug(){

echo "====================="
echo "    ribbon  (debug)"
echo "====================="
export __config__='config/win64d.cbc'
cerbero clear build-tools builds
cerbero install build-tools --repo releases
cerbero install base --repo releases
cerbero install gstreamer --repo releases
cerbero package ribbon --tarball --output-dir releases
cerbero abstract ribbon --output-dir releases

}
echo "To build $1"

$1

#cerbero clear build-tools builds
#cerbero install build-tools --repo releases
#cerbero install base --repo releases
#cerbero install gstreamer --repo releases
#cerbero install ribbon --repo releases
#cerbero package wms --tarball --output-dir releases
#cerbero abstract wms --output-dir releases
