#!/usr/local/bin/ipython
#streams content of /dev/mem to VLC as RGB images.
#NOTE: Needs to be run with sudo
from PIL import Image
import time
import numpy as np
from subprocess import Popen, PIPE
from scipy.misc import imresize

size = 4 * 1024 * 8 #8 pages of memory
x = 2**8
y = size/x
z=4
fps = 30.

p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-framerate', str(fps), \
'-re', '-i', '-', '-tune', 'zerolatency','-b', '900k', '-c:v', 'libx264', \
'-f', 'mpegts', '-r', str(fps), 'udp://localhost:1234'], stdin=PIPE, bufsize=size*10) #stream output

#p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-framerate', '30', '-i', '-', '-pix_fmt', 'yuv420p', '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-r', '30', 'memory.mov'], stdin=PIPE) #for saving to file
signature = np.asarray(Image.open('/Users/blank/Desktop/sigs.png'))
signature = imresize(signature, (signature.shape[0]/10, signature.shape[1]/10, 3))

x_offset = y - signature.shape[0]
y_offset = x - signature.shape[1]
thresh = 230
temp = np.ones((y, x, z))
for i in np.arange(signature.shape[0]):
	for j in np.arange(signature.shape[1]):
		for k in np.arange(z):
			if signature[i, j, 0] > thresh:
				temp[i+x_offset, j+y_offset, k] = 1
			else:
				temp[i+x_offset, j+y_offset, k] = 0

old_im = np.zeros((y,x,z))
print('opening udp://localhost:1234')
while (True):
	last_sig = old_im * np.abs(temp-1)
	newfp = np.fromfile("/dev/mem", dtype='uint8', count=x*y*z, sep='')
	im = np.reshape(np.copy(newfp),(y,x,z))
	old_im = im
	im = np.copy(old_im) * temp
	im = np.copy(im) + last_sig
	im_out = Image.fromarray(np.uint8(im))
	im_out.save(p.stdin, 'JPEG')
