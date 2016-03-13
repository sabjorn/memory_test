# memory_test
The code to run a laptop based sculpture.

Python reads `/dev/mem` as a file, formats the data into an image frame, and then pushes to FFMEG using a named pipe. FFMEG then combines the frames into a video and streams to `localhost:1234`

## Dependencies:
* NumPy
* PILLOW
* FFMEG
* VLC (or any video playback software capable of opening a network stream)
