# memory_test
The code to run a laptop based sculpture.

Python reads `/dev/mem` as a file, formats the data into an image frame, and then pushes to FFMEG using a named pipe. FFMEG then combines the frames into a video and streams to `localhost:1234`

## Dependencies:
* NumPy
* PILLOW
* FFMEG
* VLC (or any video playback software capable of opening a network stream)

For `/dev/mem` and `/dev/kmem` to appear, open Terminal and enter:
```bash

sudo nvram boot-args="kmem=1"

```

And then reboot the system. This will likely have to be redone if NVRAM is ever reset or the system is updated.

###Automatic Startup
Two launchdd files were created, one to launch VLC in fullscreen and the other to run the python script. This will allow the 'sculpture' to launch when the computer starts. Information for setting up launchd can be found [here](http://launchd.info/). plist files are put in `/Library/LaunchDaemons` so they can be run as root (needed for the python application to read `/dev/mem`)