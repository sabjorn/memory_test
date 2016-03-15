#streams content of /dev/mem to VLC as RGB images.
#NOTE: Needs to be run with sudo
from PIL import Image
import time
#from subprocess import Popen, PIPE #pipe data
import subprocess as sp

#16:9 aspect ratio
x = 1600/16
y = 900/16

size = 4 * 1024 * 8 #8 pages of memory
x = 2**8
y = size/x
#x = 2**8
#	y = 2**7
z = 4

#fps = 2.66*4 #bpm!
fps = 30.

#code from http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/
#trying to get it to work.
command = [ FFMPEG_BIN,
        '-y', # (optional) overwrite output file if it exists
        '-f', 'rawvideo',
        '-vcodec','rawvideo',
        '-s', '420x360', # size of one frame
        '-pix_fmt', 'rgb24',
        '-r', '24', # frames per second
        '-i', '-', # The imput comes from a pipe
        '-an', # Tells FFMPEG not to expect any audio
        '-vcodec', 'mpeg',
        'udp://localhost:1234' ]

pipe = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE)
#p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-framerate', str(fps), \
#'-re', '-i', '-', '-tune', 'zerolatency','-b', '900k', '-c:v', 'libx264','-f', 'mpegts', '-r', str(fps), 'udp://localhost:1234'], stdin=PIPE) #stream output
#p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-framerate', '30', '-i', '-', '-pix_fmt', 'yuv420p', '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-r', '30', 'memory.mov'], stdin=PIPE) #for saving to file

# newfp = np.fromfile("/dev/mem", dtype='uint8', count=x*y*3, sep='')
# im = np.reshape(np.copy(newfp),(x,y,3))
	#for t in range(100):

print('opening udp://localhost:1234')
while (True):
	#print (t)
	newfp = np.fromfile("/dev/mem", dtype='uint8', count=x*y*z, sep='')
	im = np.reshape(np.copy(newfp),(y,x,z))
    pipe.proc.stdin.write(im.tostring())
	#im_out = Image.fromarray(np.uint8(im))
	#im_out.save(p.stdin,'PNG')
	time.sleep(1/float(fps)) #pause to prevent rapid succession
