#!/usr/bin/env bash

# Go through all python scripts and find the names of the imports to regenerate a new requirements.txt file, project.toml file, and others.
# Step 1, find all import statements in the python scripts
# Step 2, find the names of the imports
# Step 3, build a pip install command for all imports
# Step 4, build a project.toml file for all imports

# Step 0, clear out the old files. We should put all the working files of this script in a tmp dir
rm -rf tmp/
mkdir tmp/

# Step 1, find all import statements in the python scripts in src.
# This will occur either as start of line: import <name>
# or as from <name> import <submodule>. Extract both forms into imports.txt
# Restrict import and from to the start of the line
# The src/ dir has subdirectories. Recurse. Remove the filename

# Find all import statements. Exclude filename and path from the grep output.
grep -r -o "^import [a-zA-Z0-9_]*" src/ >> tmp/imports.txt
grep -r -o "^from [a-zA-Z0-9_]* import [a-zA-Z0-9_]*" src/ >> tmp/imports.txt

# Remove everything before the colon
sed -i 's/.*://g' tmp/imports.txt


# Step 2a clean the imports file of the words, import, from and duplicates. 
# In the next step we will scan for packages which already exist.
# Clean import only from start of line.
sed -ri 's/^import //g' tmp/imports.txt
# find the from <name we keep> import .*, and keep only name we keep.
sed -ri 's/^from ([a-zA-Z0-9_]*) import .*/\1/g' tmp/imports.txt



# Also run uniq to remove duplicates
sort -u tmp/imports.txt | uniq > tmp/imports2.txt





# Step 2b, use python to remove imports which do not need pip installing because they are part of the default python distribution
# We should iterate through each line to see if python *can* import it, if it can, we skip the package. If it can't, we add it to the list of packages to install
# We should also remove the packages which are part of the standard python distribution
for line in $(cat tmp/imports2.txt); do
    python -c "import $line" 2> /dev/null
    if [ $? -eq 0 ]; then
        echo "Skipping $line"
    else
        echo "Adding $line"
        echo $line >> tmp/imports3.txt
    fi
done


# Run pip on all imports from imports3
# Step 3, build a pip install command for all imports
pip install -r tmp/imports3.txt

# Also install jupyter notebooks and extensions to autorun cells. This should be runnable on mybinder.
pip install jupyter jupyter_contrib_nbextensions && jupyter contrib nbextension install --user

# also install pytest
pip install pytest

# update the requirements.txt file and toml and conda env file
pip freeze > requirements.txt




# Step 4, build a project.toml file for all imports


# # clean up
# rm -rf tmp/

