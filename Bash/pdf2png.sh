# Brodie Davis
# January 2016
# REQUIREMENTS: imagemagick package

# From the Debian Docs: 
#IFS - Contains a string of characters which are used as word seperators in the command line. The string normally consists of the space, tab and the newline characters.

# Store old IFS and set a new one
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")

for file in `ls *pdf` # for each pdf in directory
do

  pdf="$file"
  png="`echo "$file" | sed 's/pdf/png/'`" # replace 'pdf' with 'png'

  echo "$pdf -> $png"
  convert -density 150 "$pdf" -quality 90 "$png"


done

# restore previous IFS
IFS=$SAVEIFS
