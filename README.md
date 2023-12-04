# FS Watch Daemon
A simple tool for watching filesystem changes and logging them to systemd-journal.


## Install
sudo ./install


## Configuration
Edit /etc/fswatchd.yaml

This file is a list of paths and operations to watch for. The tool will watch each path recursively.
Possible options for the operations field include the following:
* IN_CREATE
* IN_OPEN
* IN_MODIFY
* IN_ATTRIB
* IN_CLOSE_NOWRITE
* IN_CLOSE_WRITE
* IN_DELETE
* IN_MOVED_FROM
* IN_MOVED_TO
* all

The all tag will log any and all file operations done to a path.
