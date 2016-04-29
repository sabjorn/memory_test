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
