# -*- coding: utf-8 -*-

import sys
import math
import numpy as np
from PIL import Image
from PIL import ImageFilter

import get_shape

write = sys.stdout.write

class pretty_moon_data:
	def __init__(self, img_fname_in, img_fname_out):
		self.img_fname_in = img_fname_in
		self.img_fname_out = img_fname_out
		self.pixel = [0,0,0] # (r,g,b)
		self.image_no = img_fname_in[-8:-4]
		
	##########################################################################
	#                                                                        #
	#                  Process                                               #
	#                                                                        #
	##########################################################################
	# draw dummy moon
	def process_0(self):
		self.read_img()
	
		self.calc_centroid()
		self.init_radius()
		
		self.init_copy_image()
		self.make_dummy_image(self.centroid, self.radius_init)
		self.save_image(self.img_fname_out)

	# draw centroid & circle
	def process_1(self):
		self.read_img()
	
		self.calc_centroid()
		self.init_radius()
		
		self.init_copy_image()
		self.copy_image()
		self.draw_centroid(self.centroid)
		self.draw_circle(self.centroid, self.radius_init)
		self.save_image(self.img_fname_out)

	# draw centroid & circle
	def process_2(self):
		self.read_img()
		#self.get_total_val()
		#return
	
		self.calc_centroid()
		self.init_radius()
		
		#self.filtering()

		hd = get_shape.get_shape(self.image_in)
		this_parm = np.zeros(3)
		this_parm[0] = self.centroid[0]
		this_parm[1] = self.centroid[1]
		this_parm[2] = self.radius_init
		param = hd.optimization(this_parm)

		self.centroid[0] = param[0]
		self.centroid[1] = param[1]
		self.radius = param[2]
		
		self.init_copy_image()
		self.copy_image()
		self.draw_centroid(self.centroid)
		self.draw_circle(self.centroid, self.radius)
		self.save_image(self.img_fname_out)

	# cut moon image
	def process_3(self):
		self.read_img()
		#self.get_total_val()
		#return
	
		self.calc_centroid()
		self.init_radius()
		
		#self.filtering()

		hd = get_shape.get_shape(self.image_in)
		this_parm = np.zeros(3)
		this_parm[0] = self.centroid[0]
		this_parm[1] = self.centroid[1]
		this_parm[2] = self.radius_init
		param = hd.optimization(this_parm)

		self.centroid[0] = param[0]
		self.centroid[1] = param[1]
		self.radius = param[2]
		
		self.init_moon_image(self.radius)
		self.make_moon_image(self.centroid)
		self.save_image(self.img_fname_out)
		
		write('STAT\t'+self.image_no+'\t'+str(self.centroid[0])+'\t'+str(self.centroid[1])+'\t'+str(self.radius)+'\n')
		
	# find edge
	def process_10(self):
		self.read_img()
	
		self.filtering()
		self.save_image(self.img_fname_out)
		
	# extract small part
	def process_99(self):
		self.read_img()
		
		self.calc_centroid()
		self.init_radius()		
		self.init_moon_image(self.radius_init)
		self.make_moon_image(self.centroid)
		self.save_image(self.img_fname_out)
	
	
	##########################################################################
	#                                                                        #
	#          Handler: Image_In                                             #
	#                                                                        #
	##########################################################################
	def read_img(self):
		self.image_in = Image.open(self.img_fname_in)
		self.size = self.image_in.size
	
	def get_pixel(self, x, y):
		self.pixel = self.image_in.getpixel((x,y))
		
	def show_img(self):
		self.image_in.show()
		
	def get_total_val(self):
		total_val = 0
		for x in range(self.size[0]):
			for y in range(self.size[1]):
				self.pixel = self.image_in.getpixel((x,y))
				total_val += self.pixel[0]+self.pixel[1]+self.pixel[2]
		sys.stderr.write('total_val: '+str(total_val)+'\n')
		return total_val
		
	##########################################################################
	#                                                                        #
	#          Calculation (process_1)                                       #
	#                                                                        #
	##########################################################################
	def calc_centroid(self):
		sys.stderr.write('In calc_centroid\n')

		'''
		sys.stderr.write('Temporary\n')
		self.centroid = [0, 0]
		self.centroid[0] = 1386
		self.centroid[1] = 721
		#self.centroid[0] = 950
		#self.centroid[1] = 1000
		sys.stderr.write('Centroid: '+str(self.centroid[0])+', '+str(self.centroid[1])+'\n')
		return
		'''
		
		self.centroid = [0,0]
		denom = 0
		for x in range(self.size[0]):
			for y in range(self.size[1]):
				self.pixel = self.image_in.getpixel((x,y))
				self.centroid[0] += x*(self.pixel[0] + self.pixel[1] + self.pixel[2])
				self.centroid[1] += y*(self.pixel[0] + self.pixel[1] + self.pixel[2])
				denom += (self.pixel[0] + self.pixel[1] + self.pixel[2])
		self.centroid[0] = int(self.centroid[0]/denom + 0.5)
		self.centroid[1] = int(self.centroid[1]/denom + 0.5)
		sys.stderr.write('Centroid: '+str(self.centroid[0])+', '+str(self.centroid[1])+'\n')
	
	def init_radius(self):
		sys.stderr.write('In init_radius\n')

		'''
		'''
		sys.stderr.write('Temporary\n')
		#self.radius_init = 50
		#self.radius_init = int(132*0.5+0.5)
		self.radius_init = 100
		sys.stderr.write('radius(init):'+str(self.radius_init)+'\n')
		return
		
		############################## Pending
		max_radius = self.centroid[0]
		if max_radius < self.centroid[1]:
			max_radius = self.centroid[1]
		if max_radius < self.size[0] - self.centroid[0]:
			max_radius = self.size[0] - self.centroid[0]
		if max_radius < self.size[1] - self.centroid[1]:
			max_radius = self.size[1] - self.centroid[1]
		
		sys.stderr.write('max_radius: '+str(max_radius)+'\n')
		
		val_by_radius = np.zeros(max_radius+1)
		num_by_radius = np.zeros(max_radius+1)
		for x in range(self.size[0]):
			for y in range(self.size[1]):
				self.pixel = self.image_in.getpixel((x,y))
				r = math.floor(math.sqrt(pow(x - self.centroid[0], 2) + pow(y - self.centroid[1], 2)))
				if r > max_radius:
					r = max_radius
				self.pixel = self.image_in.getpixel((x,y))
				val_by_radius[r] += (self.pixel[0] + self.pixel[1] + self.pixel[2])
				num_by_radius[r] += 1
		
		#write('val_by_radius\n')
		#for r in range(max_radius):
		#	write(str(r)+'\t'+str(num_by_radius[r])+'\t'+str(val_by_radius[r])+'\n')
		
		min_val = 9999999999
		max_val = 0
		for r in range(max_radius):
			if min_val > val_by_radius[r] / num_by_radius[r]:
				min_val = val_by_radius[r] / num_by_radius[r]
			if max_val < val_by_radius[r] / num_by_radius[r]:
				max_val = val_by_radius[r] / num_by_radius[r]
		threshold = 3.0/4.0*min_val + 1.0/4.0*max_val
		sys.stderr.write('min_val:'+str(min_val)+'\n')
		sys.stderr.write('max_val:'+str(max_val)+'\n')
		sys.stderr.write('threshold:'+str(threshold)+'\n')
			
		cnt = 0
		self.radius_init = 0
		for r in range(max_radius):
			if val_by_radius[max_radius-r] / num_by_radius[max_radius-r] < threshold:
				cnt += 1
			else:
				cnt = 0
			if cnt >= 10:
				self.radius_init = max_radius - r
		sys.stderr.write('radius(init):'+str(self.radius_init)+'\n')
		self.radius_init = math.floor(self.radius_init*1.0)
		sys.stderr.write('radius(init2):'+str(self.radius_init)+'\n')

	##########################################################################
	#                                                                        #
	#                 Find edge (process_10)                                  #
	#                                                                        #
	##########################################################################
	def filtering(self):
		self.image_out = self.image_in.filter(ImageFilter.FIND_EDGES)
	
		
	##########################################################################
	#                                                                        #
	#          Handler: Image_Out                                            #
	#                                                                        #
	##########################################################################
	##########################################################
	#                                                        #
	#           Init Image with size                         #
	#                                                        #
	##########################################################
	def init_new_image(self, size_x, size_y):
		self.size_out = [size_x, size_y]
		self.image_out = Image.new('RGBA', self.size_out)
		
	def init_moon_image(self, radius):
		width = int(radius*2.6)
		self.init_new_image(width, width)

	def init_copy_image(self):
		self.init_new_image(self.size[0], self.size[1])
		
	##########################################################
	#                                                        #
	#           Draw Image                                   #
	#                                                        #
	##########################################################

	def copy_image(self):
		for x in range(self.size[0]):
			for y in range(self.size[1]):
				self.pixel = self.image_in.getpixel((x,y))
				self.image_out.putpixel((x,y), (self.pixel[0], self.pixel[1], self.pixel[2], 0))
	
	def draw_centroid(self, centroid):
		for dx in range(10):
			for dy in range(10):
				self.image_out.putpixel((centroid[0]+dx,centroid[1]+dy), (255, 0, 0, 0))

	def draw_circle(self, centroid, radius):
		thres = 1
		for x in range(self.size[0]):
			for y in range(self.size[1]):
				r = int(math.sqrt(pow(x - centroid[0], 2) + pow(y - centroid[1], 2))+0.5)
				if r >= radius - thres and r <= radius + thres:
					self.image_out.putpixel((x,y), (255, 0, 0, 0))
				
	def draw_frame(self, centroid, radius):
		for dx_0 in range(radius*2):
			dx = dx_0-radius
			self.image_out.putpixel((centroid[0]+dx,centroid[1]-radius), (255, 0, 0, 0))
			self.image_out.putpixel((centroid[0]+dx,centroid[1]+radius), (255, 0, 0, 0))
			
		for dy_0 in range(radius*2):
			dy = dy_0-radius
			self.image_out.putpixel((centroid[0]-radius,centroid[1]+dy), (255, 0, 0, 0))
			self.image_out.putpixel((centroid[0]+radius,centroid[1]+dy), (255, 0, 0, 0))

	def make_dummy_image(self, centroid, radius):
		for x in range(self.size[0]):
			for y in range(self.size[1]):
				if x > centroid[0]:
					self.image_out.putpixel((x,y), (0, 0, 0, 0))
				else:
					r = int(math.sqrt(pow(x-centroid[0], 2)+pow(y-centroid[1], 2))+0.5)
					if r <= radius:
						self.image_out.putpixel((x,y), (255, 255, 255, 0))
					else:
						self.image_out.putpixel((x,y), (0, 0, 0, 0))
			
	##########################################################
	#                                                        #
	#           Cut & draw small moon image                  #
	#                                                        #
	##########################################################
	def make_moon_image(self, centroid):
		centroid_out = [int(self.size_out[0]/2+0.5), int(self.size_out[1]/2+0.5)]
		for dx_0 in range(self.size_out[0]):
			dx = dx_0 - centroid_out[0]
			x_in = centroid[0] + dx
			for dy_0 in range(self.size_out[1]):
				dy = dy_0 - centroid_out[1]
				y_in = centroid[1] + dy
				if x_in >= 0 and y_in >= 0 and x_in < self.size[0] and y_in < self.size[1]:
					self.pixel = self.image_in.getpixel((x_in,y_in))
				else:
					self.pixel = [0, 0, 0]
				self.image_out.putpixel((dx_0,dy_0), (self.pixel[0], self.pixel[1], self.pixel[2], 0))
			
	##########################################################
	#                                                        #
	#                                                        #
	#                                                        #
	##########################################################
	def put_pixel(self, x, y):
		self.image_out.putpixel((x,y), (self.pixel[0], self.pixel[1], self.pixel[2], 0))
		
	def save_image(self, img_fname_out):
		self.image_out.save(img_fname_out, 'bmp')
		
	##########################################################################
	#                                                                        #
	#                                                                        #
	#                                                                        #
	##########################################################################
	##########################################################################
	#                                                                        #
	#                                                                        #
	#                                                                        #
	##########################################################################
	##########################################################
	#                                                        #
	#                                                        #
	#                                                        #
	##########################################################
		
	

def main():
	if len(sys.argv) < 3:
		sys.stderr.write('Usage: python $0 img_fname(in) img_fname(out)\n')
		sys.exit(1)
	
	img_fname_in = sys.argv[1]
	img_fname_out = sys.argv[2]
	
	hd = pretty_moon_data(img_fname_in, img_fname_out)
	flg = 3
	if flg == 0:
		hd.process_0()
	elif flg == 1:
		hd.process_1()
	elif flg == 2:
		hd.process_2()
	elif flg == 3:
		hd.process_3()
	elif flg == 10:
		hd.process_10()
	elif flg == 99:
		hd.process_99()

	
if __name__ == '__main__':
	main()


		