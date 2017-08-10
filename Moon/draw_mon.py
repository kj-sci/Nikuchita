# -*- coding: utf-8 -*-

import sys
import math
import numpy as np
from PIL import Image

write = sys.stdout.write

class draw_mon:
	def __init__(self, age, img_fname_out):
		self.age = age
		self.img_fname_out = img_fname_out
		
		self.theta = 12.0/360.0 * 2.0 * math.pi
		
		self.radius = 100
		self.r_sqr = pow(self.radius, 2)
		
		self.size_out = [0, 0]
		self.centroid = [0, 0]
		
		# Temporary
		#self.buffer = int(self.radius*2.4*0.618+0.5)
		self.buffer = 0
		
		for loop in range(2):
			self.size_out[loop] = int(self.radius*2.4+0.5)
			self.centroid[loop] = int(self.size_out[loop]/2+0.5)
		# Temporary
		self.size_out[0] = int(self.radius*2.4+0.5) + self.buffer
		
		write('Size: ('+str(self.size_out[0])+', '+str(self.size_out[1])+')\n')
		write('Centroid: ('+str(self.centroid[0])+', '+str(self.centroid[1])+')\n')
		
	##########################################################################
	#                                                                        #
	#                  Process                                               #
	#                                                                        #
	##########################################################################
	# draw dummy moon
	def process(self):
		self.init_img()
		
		self.init_mon()
		self.do_draw_mon()
		#self.do_draw_mon_upper()
		#self.do_draw_mon_left()
		#self.do_draw_mon_left_2()
		
		#self.gradation()
		
		self.save_image(self.img_fname_out)

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
	# input: self.size_out
	def init_img(self):
		self.image_out = Image.new('RGBA', self.size_out)
		
		
	##########################################################
	#                                                        #
	#           Draw Image                                   #
	#                                                        #
	##########################################################
	# input:
	# - self.age
	def calc_sun_dir(self):
		self.sun_dir = np.zeros(3)
		self.sun_dir[0] = -math.sin(self.age*self.theta)
		self.sun_dir[1] = 0
		self.sun_dir[2] = math.cos(self.age*self.theta)

	def inner_product(self, v1, v2):
		val = 0
		for loop in range(3):
			val += v1[loop] * v2[loop]
		
		return val
		
	def init_mon(self):
		# (x0, y0): coord in img
		for x in range(self.size_out[0]):
			for y in range(self.size_out[1]):
				self.image_out.putpixel((x,y), (0, 0, 0, 0))

	# input:
	# - self.size_out
	# - self.centroid
	# - self.radius
	# - self.age
	def do_draw_mon(self):
		sys.stderr.write('do_draw_mon\n')
		self.calc_sun_dir()
		
		# (x0, y0): coord in img
		# pt (x, y, z): coord in graph
		pt = np.zeros(3)
		#for x0 in range(self.size_out[0]):
		for x0 in range(self.size_out[0]-self.buffer):
			pt[0] = x0 - self.centroid[0]
			for y0 in range(self.size_out[1]):
				pt[1] = - (y0 - self.centroid[1])
				xy_sqr = pow(pt[0], 2) + pow(pt[1], 2)
				if self.r_sqr < xy_sqr:
					#self.image_out.putpixel((x0,y0), (0, 0, 0, 0))
					continue
					
				pt[2] = math.sqrt(self.r_sqr - xy_sqr)
				val = -self.inner_product(pt, self.sun_dir)
				#write('pt: ('+str(pt[0])+', '+str(pt[1])+'): '+str(val)+'\n')
				if val > 0:
					rgb_val = int(val/(self.radius+0.0)*255.0)
					self.image_out.putpixel((x0+self.buffer,y0), (rgb_val, rgb_val, rgb_val, 0))
					#self.image_out.putpixel((x0,y0), (rgb_val, rgb_val, rgb_val, 0))
				else:
					self.image_out.putpixel((x0+self.buffer,y0), (0, 0, 0, 0))
					#self.image_out.putpixel((x0,y0), (0, 0, 0, 0))
					

	def do_draw_mon_0(self):
		self.calc_sun_dir()
		
		# (x0, y0): coord in img
		# pt (x, y, z): coord in graph
		pt = np.zeros(3)
		for x0 in range(self.size_out[0]):
			pt[0] = x0 - self.centroid[0]
			for y0 in range(self.size_out[1]):
				pt[1] = - (y0 - self.centroid[1])
				#write(str(pt[0])+', '+str(pt[1])+'\n')
				xy_sqr = pow(pt[0], 2) + pow(pt[1], 2)
				if self.r_sqr < xy_sqr:
					self.image_out.putpixel((x0,y0), (0, 0, 0, 0))
				else:
					self.image_out.putpixel((x0,y0), (255, 255, 255, 0))

	def do_draw_mon_upper(self):
		# (x0, y0): coord in img
		# pt (x, y, z): coord in graph
		pt = np.zeros(3)
		for x0 in range(self.size_out[0]):
			pt[0] = x0 - self.centroid[0]
			for y0 in range(self.size_out[1]):
				pt[1] = - (y0 - self.centroid[1])
				#write(str(pt[0])+', '+str(pt[1])+'\n')
				xy_sqr = pow(pt[0], 2) + pow(pt[1], 2)
				if self.r_sqr < xy_sqr:
					self.image_out.putpixel((x0,y0), (0, 0, 0, 0))
				elif pt[1] >= 0:
					self.image_out.putpixel((x0,y0), (255, 255, 255, 0))
				else:
					self.image_out.putpixel((x0,y0), (0, 0, 0, 0))
					
	def do_draw_mon_left(self):
		# (x0, y0): coord in img
		# pt (x, y, z): coord in graph
		pt = np.zeros(3)
		for x0 in range(self.size_out[0]):
			pt[0] = x0 - self.centroid[0]
			for y0 in range(self.size_out[1]):
				pt[1] = - (y0 - self.centroid[1])
				#write(str(pt[0])+', '+str(pt[1])+'\n')
				xy_sqr = pow(pt[0], 2) + pow(pt[1], 2)
				if self.r_sqr < xy_sqr:
					self.image_out.putpixel((x0,y0), (0, 0, 0, 0))
				elif pt[0] <= 0:
					self.image_out.putpixel((x0,y0), (255, 255, 255, 0))
				else:
					self.image_out.putpixel((x0,y0), (0, 0, 0, 0))

	def do_draw_mon_left_2(self):
		# (x0, y0): coord in img
		# pt (x, y, z): coord in graph
		pt = np.zeros(3)
		for x0 in range(self.size_out[0]):
			pt[0] = x0 - (self.centroid[0]+50)
			for y0 in range(self.size_out[1]):
				pt[1] = - (y0 - self.centroid[1])
				#write(str(pt[0])+', '+str(pt[1])+'\n')
				xy_sqr = pow(pt[0], 2) + pow(pt[1], 2)
				if self.r_sqr < xy_sqr:
					self.image_out.putpixel((x0,y0), (0, 0, 0, 0))
				elif pt[0] <= 0:
					self.image_out.putpixel((x0,y0), (255, 255, 255, 0))
				else:
					self.image_out.putpixel((x0,y0), (0, 0, 0, 0))


	def gradation(self):
		for x in range(self.size_out[0]):
			for y in range(self.size_out[1]):
				val = int((x+0.0)/(self.size_out[0]+0.0)*255)
				self.image_out.putpixel((x,y), (val, val, val, 0))
		
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
		sys.stderr.write('Usage: python $0 age(0-29) img_fname(out)\n')
		sys.exit(1)
	
	age = int(sys.argv[1])
	img_fname_out = sys.argv[2]
	
	hd = draw_mon(age, img_fname_out)
	hd.process()

	
if __name__ == '__main__':
	main()


		