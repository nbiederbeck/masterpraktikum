#!/bin/bash
# Text in wiki.txt
TMP=/tmp/convert_magic_wiki_to_pdf.md
cp $1 ${TMP}
# (Sub)Titles
sed -i "s/^===== */##### /g" ${TMP}
sed -i "s/^==== */#### /g" ${TMP}
sed -i "s/^=== */### /g" ${TMP}
sed -i "s/^== */## /g" ${TMP}
sed -i "s/^= */# /g" ${TMP}
sed -i "s/ *=====$//g" ${TMP}
sed -i "s/ *====$//g" ${TMP}
sed -i "s/ *==$//g" ${TMP}
sed -i "s/ *=$//g" ${TMP}
# Lists
sed -i "s/*/-/" ${TMP}
# Bold/Italic Text
sed -i "s/'''/__/g" ${TMP}
# Math Environments
sed -i "s/''/_/g" ${TMP}
sed -i "s/<math>/$/g" ${TMP}
sed -i "s/<\/math>/$/g" ${TMP}
# Code Blocks
sed -i "/^  /a\`\`\`" ${TMP}
sed -i "/^  /i\`\`\`bash" ${TMP}
sed -i "s/^  /    /g" ${TMP}
# Replace Links With Placeholder
sed -i "s/\[\[.*\]\]/\[link\]/g" ${TMP}

# Convert to pdf with pandoc
pandoc -i ${TMP} -o $2 --pdf-engine=xelatex
