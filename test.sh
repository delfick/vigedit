#!/bin/bash
# Set nose args for tests
export NOSE_ARGS="--pdb --with-noy"

# Set variable for current gedit plugins so it may be set back when gedit finishes
previous_plugins=`gsettings get org.gnome.gedit.plugins "active-plugins"`

# Set active plugins to just vigedit_specs and then start gedit
gsettings set org.gnome.gedit.plugins "active-plugins" "['vigedit_specs']"
if [ $1 = '-m' ]
then
    # User wants to manually start tests
    # Useful if user wants to use nose.tools.set_trace in the test
    gedit -s
else
    # User wants to auto start the tests
    gedit -s &
    pid=$!

    # Print to the screen pid for gedit and the pid of the window xdotool finds
    # Useful to see it is getting the correct window
    ps aux | grep gedit | grep -v grep
    echo "Found $pid"

    # Focus gedit and tell it to start the tests
    wmctrl -a gedit && sleep 0.5 && xdotool key ctrl+alt+u

    # Foreground gedit and set back previous active-plugins list when it's done
    wait %1
fi
gsettings set org.gnome.gedit.plugins "active-plugins" "$previous_plugins"
