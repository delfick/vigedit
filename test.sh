#!/bin/bash
# Set nose args for tests
export NOSE_ARGS="--pdb --with-noy $@"

# Set variable for current gedit plugins so it may be set back when gedit finishes
previous_plugins=`gsettings get org.gnome.gedit.plugins "active-plugins"`

# Set active plugins to just vigedit_specs and then start gedit
# Before putting back whatever plugins were set previously
gsettings set org.gnome.gedit.plugins "active-plugins" "['vigedit_specs']"
gedit -s
gsettings set org.gnome.gedit.plugins "active-plugins" "$previous_plugins"
