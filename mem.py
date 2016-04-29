#streams content of /dev/mem to VLC as RGB images.
#NOTE: Needs to be run with sudo
from PIL import Image
import time
import numpy as np
from subprocess import Popen, PIPE

size = 4 * 1024 * 8 #8 pages of memory
x = 2**8
y = size/x
z=4
fps = 30.

p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-framerate', str(fps), \
'-re', '-i', '-', '-tune', 'zerolatency','-b', '900k', '-c:v', 'libx264','-f', 'mpegts', '-r', str(fps), 'udp://localhost:1234'], stdin=PIPE, bufsize=size*4) #stream output
#p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-framerate', '30', '-i', '-', '-pix_fmt', 'yuv420p', '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-r', '30', 'memory.mov'], stdin=PIPE) #for saving to file

print('opening udp://localhost:1234')
while (True):
	#print (t)
	newfp = np.fromfile("/dev/mem", dtype='uint8', count=x*y*z, sep='')
	im = np.reshape(np.copy(newfp),(y,x,z))
	im_out = Image.fromarray(np.uint8(im))
	im_out.save(p.stdin,'PNG')
	time.sleep(1/float(fps)) #pause to prevent rapid succession
