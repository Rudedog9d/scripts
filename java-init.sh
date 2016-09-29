if [ -z $1 ] || [ -z $2 ]; then
    echo 'Usage: init.sh "folderName" "fileName"'
    exit
fi
folderName="$1"
fileName="$2"
className="$3"
template="template.java"

if [[ "$fileName" =~ ".java" ]]; then
    fileName=`echo "$fileName" | sed s/.java//`
fi

mkdir -p "$folderName"
if [ -f "$folderName/$fileName.java" ]; then
    # Set $x to answer
    echo "File $folderName/$fileName.java already exists!"
    exit
#    if [[ $x -ne 'y'  ]]; then
#        exit
#    fi
fi
if [ -f "$template" ]; then
    # replace "Hello World" with classname (Not perfect!)
    sed s/HelloWorld/"$fileName"/ template.java > "$folderName/$fileName.java"
else
    echo "$template: File not found"
fi
