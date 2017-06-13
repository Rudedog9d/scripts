#!/usr/bin/env bash
function search(){
  # Brodie Davis
  # May 2017
  #
  ## USAGE: search json
  #          Searches all files (and files in subdirs) for lines containing the word 'json'
  #
  # USAGE: search json -f *html
  #           Searches all files (and files in subdirs) ENDING IN 'html' for lines containing the word 'json'
  #
  function print_usage(){
    echo "USAGE: search SEARCH_TERM [-f file_pattern] [-x file_pattern [-x ...]]"
    echo "     -f|--filename) File pattern to match, regex supported."
    echo "     -x|--exclude)  File pattern to exclude, regex supported."
    echo
    echo "Ex. search json -f '*html'"
    echo "Ex. search json -f '*html' -x bower_components -x '*.js'"
  }

  # Declare excludeList as an array
  declare -a excludeList
  # Put filenames and folders you wish to exclude in this list, single quoted, seperated with a space.
  # Wildcards supported :D
  excludeList=('*bower*' '*cache*')

  i=0          # positional arg counter
  filename='*' # Default filename (all files)

  # handle CLI args
  while [[ $# -gt 0 ]]; do  # for each paramter
    key="$1"
    case $key in
      -e|--exclude)
        excludeList+=("$2")
        shift
        ;;
      -f|--filename)
        filename="$2"
        shift
        ;;
      -h|--help)
        print_usage
        return 1
        ;;
      *)
        if [ $i -eq 0 ]; then
          keyword="$1"
          i=`expr $i + 1`
        else
          echo -ne "Unknown Paramter: $1"
        fi
       ;;
    esac
    shift
  done

  # Remove the print_usage function
  unset -f print_usage

  # Turn off globbing in bash (wildcard * expansion)
  set -f

  str=`for i in ${excludeList[@]}; do echo -ne '( -name '$i' -prune ) -o '; done`

  # Find will send all files (and dirs) to grep that match the pattern
  find . $str -name "$filename" -exec grep --color -Hn "$keyword" {} 2>/dev/null \;

  # Turn globbing back on
  set +f
}
