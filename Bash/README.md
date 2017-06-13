# Bash Scripts

A gathering place for some of the bash scripts I have created

#### java-init.sh
A quick script to create a folder, file, and copy a simple "Hello World" program into the file as a place to start. Used for my CS249 class at SUNY POLY

#### pdf2png.sh
Use the `imagemagick` package to convert all of the files matching the `Files` string to a png file

#### search.sh
This one is kind of cool. Basically runs `grep "search_term" * -R` and recursively searches the current directory tree, BUT allows you exclude file/directory names. 

Example: You need to find all ajax requests in the current directory tree, but you only want to search html files and not waste time/resources searching through all of the external libraries or any folders with 'cache' in the name.

```
search ajax -f '*html' -e bower_components -e '*cache*'
./templates/report.html:124:    $.ajax("/api/reports/{{id}}.json", {
./templates/report.html:1453:    $.ajax("/api/reports/{{id}}.json", {
```

#### bash_colors.sh
Created by [Max Tsepkov](https://github.com/maxtsepkov/bash_colors)

#### colors.sh
Simplier version of `bash_colors.sh`, adapted from [Stack Overflow](https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux)

