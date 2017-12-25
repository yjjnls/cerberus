  #
  # init file for MinGW bash in Windows
  #  
  __dir__=$(cd $(/usr/bin/dirname ${BASH_SOURCE[0]}); pwd )
  source /usr/etc/profile
  HOME=$USERPROFILE
  cd $__dir__/..

  if [ ! -z $1 ]; then
      WD=${__WD__/\\//}
      cd "$WD"
      if [ "$1" == "-c" ] ; then
          bash.exe -c "$2"
      else
          $@
      fi
  fi
