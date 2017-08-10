# -*- coding: utf-8 -*-

import sys
import math
import numpy as np
from PIL import Image
from PIL import ImageFilter

write = sys.stdout.write

class adjust_image:
	def __init__(self, img_fname_in_1, img_fname_in_2, img_fname_out_2):
		self.img_fname_in = []
		self.img_fname_in.append(img_fname_in_1)
		self.img_fname_in.append(img_fname_in_2)
		
		self.img_fname_out = img_fname_out_2
		
		self.unit_arg = math.pi/180.0

		self.max_loop = 100
		
		self.pixel = [0,0,0] # (r,g,b)
	
	def process(self):
		self.read_img()
		
		parm_optimal = self.adjust_out_image()
		
		self.init_out_image()
		self.draw_out_image(parm_optimal)
		self.save_image(self.img_fname_out)

	##########################################################################
	#                                                                        #
	#          Handler: Image_In                                             #
	#                                                                        #
	##########################################################################
	def read_img(self):
		self.image_in = []
		for loop in range(2):
			self.image_in.append(Image.open(self.img_fname_in[loop]))

		self.size_in = []
		for loop in range(2):
			self.size_in.append(self.image_in[loop].size)
		
		self.centroid_in = []
		for loop1 in range(2):
			this_centroid = [0, 0]
			for loop2 in range(2):
				this_centroid[loop2] = int(self.size_in[loop][loop2]/2.0+0.5)
			self.centroid_in.append(this_centroid)
		
		self.size_out = [0, 0]
		self.size_out[0] = self.size_in[0][0]
		self.size_out[1] = self.size_in[0][1]
		
	##########################################################################
	#                                                                        #
	#          Optimization                                                  #
	#                                                                        #
	##########################################################################
	# parameter: centroid(x_offset, y_offset), theta (in rad)
	def adjust_out_image(self):
		# parms = (x_offset, y_offset, theta)
		parms = np.zeros(3)
		#self.x_offset = 0
		#self.y_offset = 0
		parms_delta = np.ones(3)
		
		error_old = self.calc_sqrd_error(parms)
		
		grad = np.zeros(3)
		grad[0] = -self.calc_derivation(parms, (parms_delta[0], 0, 0))
		grad[1] = -self.calc_derivation(parms, (0, parms_delta[1], 0))
		grad[2] = -self.calc_derivation(parms, (0, 0, parms_delta[2]))
		grad_norm = math.sqrt(math.pow(grad[0], 2) + math.pow(grad[1], 2) + math.pow(grad[2], 2))
		
		write('Grad: ('+str(grad[0])+', '+str(grad[1])+', '+str(grad[2])+')\n')
		# init multiplier
		multiplier = 1
		if grad_norm > 5:
			multiplier = 5.0/grad_norm
		elif grand_norm > 0.000001 and grad_norm < 2:
			multiplier = 2.0/grad_norm

		write('Multiplier: ('+str(multiplier)+'\n')
		step = grad * multiplier
		parms = parms + step
		write('parms: ('+str(parms[0])+', '+str(parms[1])+', '+str(parms[2])+')\n')
		
		error_new = self.calc_sqrd_error(parms)
		
		write('Error: '+str(error_old)+' => '+str(error_new)+'\n')
		
		error_old = error_new
		
		loop = 0
		while loop < self.max_loop:
			#multiplier *= 0.9
			write('---------- '+str(loop)+'-th run ---------------\n')
			grad[0] = -self.calc_derivation(parms, (parms_delta[0], 0, 0))
			grad[1] = -self.calc_derivation(parms, (0, parms_delta[1], 0))
			grad[2] = -self.calc_derivation(parms, (0, 0, parms_delta[2]))
			grad_norm = math.sqrt(math.pow(grad[0], 2) + math.pow(grad[1], 2) + math.pow(grad[2], 2))			
			write('Grad: ('+str(grad[0])+', '+str(grad[1])+', '+str(grad[2])+')\n')

			step = grad * multiplier
			parms = parms + step
			write('parms: ('+str(parms[0])+', '+str(parms[1])+', '+str(parms[2])+')\n')
			
			error_new = self.calc_sqrd_error(parms)
			
			write('Error: '+str(error_old)+' => '+str(error_new)+'\n')
			
			error_old = error_new
			
			loop += 1
			
		return parms

	
	# Err(x_offset, y_offset) = sum_{x,y}{(in1(x,y) - in2(x-x_offset,y-y_offset)}^2
	# compare image_in & image_out (treaked by parms (centroid, theta(unit = 2pi/60)))
	def calc_sqrd_error(self, parms):
		sqrd_error = 0
		# (x1, y1): dot in img1
		for x1 in range(self.size_in[0][0]):
			# (dx1, dy1): coord in img1
			dx1 = x1 - self.centroid_in[0][0]
			for y1 in range(self.size_in[0][1]):
				dy1 = y1 - self.centroid_in[0][1]
				
				# (dx2, dy2): coord in img2
				dx2 = (dx1-parms[0])*np.cos(parms[2]*self.unit_arg) - (dy1-parms[1])*np.sin(parms[2]*self.unit_arg)
				dy2 = (dx1-parms[0])*np.sin(parms[2]*self.unit_arg) + (dy1-parms[1])*np.cos(parms[2]*self.unit_arg)
				
				# (x2, y2): dot in img2
				x2 = self.centroid_in[1][0] + dx2
				y2 = self.centroid_in[1][1] + dy2
				
				if x2 < 0 or x2 >= self.size_in[1][0] or y2 < 0 or y2 >= self.size_in[1][1]:
					continue
					
				this_val = [0, 0]
				
				this_pixel = self.image_in[0].getpixel((x1,y1))
				this_val[0] = this_pixel[0] + this_pixel[1] + this_pixel[2]
				this_pixel = self.image_in[1].getpixel((x2,y2))
				this_val[1] = this_pixel[0] + this_pixel[1] + this_pixel[2]
				sqrd_error += math.pow(this_val[0]-this_val[1], 2)
		return sqrd_error
	
	# {Err(x+dx,y+dy)-Err(x-dx, y-dy)}/2/dh (dh = sqrt(dx^2+dy^2))
	def calc_derivation(self, parms, parms_delta):
		dh = 2 * math.sqrt(math.pow(parms_delta[0], 2)+math.pow(parms_delta[1], 2)+math.pow(parms_delta[2], 2))
		err_1 = self.calc_sqrd_error(parms + parms_delta)
		err_2 = self.calc_sqrd_error(parms - parms_delta)
		derivation = (err_1 - err_2)/dh
		
		return derivation
		
		
	##########################################################################
	#                                                                        #
	#          Handler: Image_Out                                            #
	#                                                                        #
	##########################################################################
	##########################################################
	#                                                        #
	#                                                        #
	#                                                        #
	##########################################################
	def init_out_image(self):
		self.image_out = Image.new('RGBA', self.size_out)
		
	
	def draw_out_image(self, parms):
		for x1 in range(self.size_in[0][0]):
			# (dx1, dy1): coord in img1
			dx1 = x1 - self.centroid_in[0][0]
			for y1 in range(self.size_in[0][1]):
				dy1 = y1 - self.centroid_in[0][1]
				
				# (dx2, dy2): coord in img2
				dx2 = (dx1-parms[0])*np.cos(parms[2]*self.unit_arg) - (dy1-parms[1])*np.sin(parms[2]*self.unit_arg)
				dy2 = (dx1-parms[0])*np.sin(parms[2]*self.unit_arg) + (dy1-parms[1])*np.cos(parms[2]*self.unit_arg)
				
				# (x2, y2): dot in img2
				x2 = self.centroid_in[1][0] + dx2
				y2 = self.centroid_in[1][1] + dy2

				if x2 < 0 or y2 < 0 or x2 >= self.size_in[1][0] or y2 >= self.size_in[1][1]:
					self.image_out.putpixel((x1, y1), (0,0,0,0))
				else:
					self.pixel = self.image_in[1].getpixel((x2,y2))
					self.image_out.putpixel((x1,y1), (self.pixel[0], self.pixel[1], self.pixel[2], 0))
					
	def save_image(self, img_fname_out):
		self.image_out.save(img_fname_out, 'bmp')
		
	##########################################################
	#                                                        #
	#                                                        #
	#                                                        #
	##########################################################


	##########################################################
	#                                                        #
	#                                                        #
	#                                                        #
	##########################################################
	def put_pixel(self, x, y):
		self.image_out.putpixel((x,y), (self.pixel[0], self.pixel[1], self.pixel[2], 0))
		
		
	##########################################################################
	#                                                                        #
	#                                                                        #
	#                                                                        #
	##########################################################################
	

def main():
	if len(sys.argv) < 4:
		sys.stderr.write('Usage: python $0 img_fname(in1) img_fname(in2) img_fname(out2)\n')
		sys.exit(1)
	
	img_fname_in_1 = sys.argv[1]
	img_fname_in_2 = sys.argv[2]
	img_fname_out_2 = sys.argv[3]
	
	hd = adjust_image(img_fname_in_1, img_fname_in_2, img_fname_out_2)
	hd.process()
	
if __name__ == '__main__':
	main()


		