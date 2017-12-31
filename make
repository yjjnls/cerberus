config=win64
if [ $(uname) == 'Linux' ] ; then
   config=lin64
fi

recipe=$1
shift

if [[ ! -d projects/$recipe ]]; then
   echo "Can not filed <$recipe> dir in projects/$recipe"
   exit 1
fi


debug=

configure=
compile=
install=
check=

steps=(
   '--configure'
   '--compile'
   '--install'
   '--check'
)
options=

for opt in $@
do

  if [[ $opt == "--debug" ]]; then
     debug=YES
	 config=${config}d
  else
		for step in '--configure' '--compile' '--install' '--check'
		do
		   if [[ "$opt" == "$step" ]]; then
		      options="$options $step"
		   fi
		done
  fi  
done

if [ -z $options ] ; then
   options='--configure --compile --install'
fi
config=${config}.cbc
echo ""
echo "       ========================================="
echo "              build recipe <$recipe>"
for o in $options
do
echo "               + ${o:2}"
done
[ ! -z $debug ] && \
echo "                debug"
echo "      ========================================="
echo ""

./cerbero-uninstalled -c config/${config} make $recipe $options --directory projects/$recipe --local-source projects/$recipe