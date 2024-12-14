# pistol terminal guide

## commands:
- cd - change current working directory
- ucd - undo last cd
- - example:
```
<posix> /home/astridot/Desktop> cd ..
<posix> /home/astridot> cd Documents/MyProject
<posix> /home/astridot/Documents/MyProject>cd /home/astridot
<posix> /home/astridot> cd /
<posix> /> ucd
<posix> /home/astridot> ucd
<posix> /home/astridot/Documents> ucd
<posix> /home/astridot> ucd
<posix> /home/astridot/Desktop> exit
➤➤ Exited pistol
```
- exit - exit pistol
- help - go to the pistol github page
- ### solo
- - solo uses the system's default shell to run further commands
- - example:
```
<posix> /home/astridot/Desktop/Project> solo dir
pistol	README.md  setup.py
<posix> /home/astridot/Desktop/Project> solo ls
pistol	README.md  setup.py
<posix> /home/astridot/Desktop/Project> solo echo Hello, world!
Hello, world!
<posix> /home/astridot/Desktop/Project> solo cd ..
⚠️  warning: cd may not work properly when executing using solo
🚨 error: solo: [Errno 2] No such file or directory: 'cd'
<posix> /home/astridot/Desktop/Project> solo exit
⚠️  warning: exit may not work properly when executing using solo
🚨 error: solo: [Errno 2] No such file or directory: 'exit'
<posix> /home/astridot/Desktop/Project> solo help
⚠️  warning: help may not work properly when executing using solo
🚨 error: solo: [Errno 2] No such file or directory: 'help'
<posix> /home/astridot/Desktop/Project> solo
<posix> /home/astridot/Desktop/Project [solo]> echo hi
hi
<posix> /home/astridot/Desktop/Project [solo]> dir
pistol	README.md  setup.py
<posix> /home/astridot/Desktop/Project [solo]> ls
pistol	README.md  setup.py
<posix> /home/astridot/Desktop/Project [solo]> cd ..
⚠️  warning: cd may not work properly when executing using solo
🚨 error: solo: [Errno 2] No such file or directory: 'cd'
<posix> /home/astridot/Desktop/Project [solo]> exit
➤➤ Exited solo
<posix> /home/astridot/Desktop/Project> exit
➤➤ Exited pistol
```