#__config__='config/win64.cbc'
function cerbero(){
    [[ "$1" == 'package' ]] && ping github.com -n 5

   ./cerbero-uninstalled -c ${__config__} $@
   if [ $? -ne 0 ]; then
      echo "Failed run command ./cerbero-uninstalled -c ${__config__} $@"
      exit 1
   fi


}

email=$(git config --global user.name)
if [[ $? -ne 0 || -z $email ]]; then
    git config --global user.name "Mingyi Zhang"
    git config --global user.email "zhangmingyi@kedacom.com"
fi

[ ! -d releases ] && mkdir releases
#export CERBERUS_CACHED_SOURCES='z:/share/cerbero/cerbero-1.12.3/sources'
echo "CERBERUS_CACHED_SOURCES: $CERBERUS_CACHED_SOURCES"

CLEARITEMS='build_tools_prefix prefix cache_file sources'

function build_tools(){

__config__='config/win64.cbc'
[ "$(uname)" == "Linux" ] && __config__='config/lin64.cbc'
echo "====================="
echo "    build-tools      "
echo "    $__config__      "
echo "====================="


cerbero clear $CLEARITEMS
cerbero bootstrap --build-tools-only 
cerbero tar-build-tools --output-dir releases
cerbero abstract build-tools --output-dir releases

}

function base(){

__config__='config/win64.cbc'
[ "$(uname)" == "Linux" ] && __config__='config/lin64.cbc'
echo "====================="
echo "    base      "
echo "    $__config__      "
echo "====================="

cerbero clear $CLEARITEMS
cerbero install build-tools --repo releases
cerbero package base --tarball --output-dir releases
cerbero abstract base --output-dir releases

}

function gstreamer(){

__config__='config/win64.cbc'
[ "$(uname)" == "Linux" ] && __config__='config/lin64.cbc'
echo "====================="
echo "    gstreamer      "
echo "    $__config__      "
echo "====================="

cerbero clear $CLEARITEMS
cerbero install build-tools --repo releases
cerbero install base --repo releases
cerbero package gstreamer --tarball --output-dir releases
cerbero abstract gstreamer --output-dir releases

}

function ribbon(){

__config__='config/win64.cbc'
[ "$(uname)" == "Linux" ] && __config__='config/lin64.cbc'
echo "====================="
echo "    ribbon      "
echo "    $__config__      "
echo "====================="

cerbero clear $CLEARITEMS
cerbero install build-tools --repo releases
cerbero install base --repo releases
cerbero install gstreamer --repo releases
cerbero package ribbon --tarball --output-dir releases
cerbero abstract ribbon --output-dir releases

}
function ribbon_debug(){

__config__='config/win64d.cbc'
[ "$(uname)" == "Linux" ] && __config__='config/lin64.cbc'
echo "====================="
echo "    ribbon(debug)      "
echo "    $__config__      "
echo "====================="

cerbero clear $CLEARITEMS
cerbero install build-tools --repo releases
cerbero install base --repo releases
cerbero install gstreamer --repo releases
cerbero package ribbon --tarball --output-dir releases
cerbero abstract ribbon --output-dir releases

}

function wms(){

__config__='config/win64.cbc'
[ "$(uname)" == "Linux" ] && __config__='config/lin64.cbc'
echo "====================="
echo "    wms      "
echo "    $__config__      "
echo "====================="

cerbero clear $CLEARITEMS
cerbero install build-tools --repo releases
cerbero install base --repo releases
cerbero install gstreamer --repo releases
cerbero install ribbon --repo releases
cerbero package wms --tarball --output-dir releases
cerbero abstract wms --output-dir releases

}
function wms_debug(){

__config__='config/win64d.cbc'
[ "$(uname)" == "Linux" ] && __config__='config/lin64.cbc'
echo "====================="
echo "    wms(debug)      "
echo "    $__config__      "
echo "====================="

cerbero clear $CLEARITEMS
cerbero install build-tools --repo releases
cerbero install base --repo releases
cerbero install gstreamer --repo releases
cerbero install ribbon --repo releases
cerbero package wms --tarball --output-dir releases
cerbero abstract wms --output-dir releases

}

echo "To build $1"

$1
