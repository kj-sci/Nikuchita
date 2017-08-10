# -*- coding: utf-8 -*-

import sys
import math
import numpy as np
from PIL import Image

write = sys.stdout.write

class get_shape:
	def __init__(self, image_in):
		self.image_in = image_in
		self.size_in = self.image_in.size
		
		self.flg_calc_value = 0
		self.label_1 = ''
		self.label_2 = ''

	##########################################################################
	#                                                                        #
	#          Optimization                                                  #
	#                                                                        #
	##########################################################################
	# parms, parms_init = (centroid_x, centroid_y, radius)
	def optimization(self, parms_init):
		sys.stderr.write('In optimization\n')
		parms = parms_init
		
		delta = np.ones(3)
		#delta[2] = 2
		
		momentum = np.zeros(3)
		momentum_decay = 0
		
		self.max_loop = 100
		self.loop = 0
		sys.stderr.write('Init: centroid: ('+str(parms[0])+', '+str(parms[1])+'), radius: '+str(parms[2])+'\n')

		sys.stderr.write('Value_old: \n')
		self.label_1 = 'Value(old)'
		self.label_2 = ''
		value_old = self.calc_value(parms, self.flg_calc_value)
		parms_delta = np.ones(3)
		
		grad = np.zeros(3)
		self.label_1 = 'Derivation'
		self.label_2 = 'x'
		grad[0] = self.calc_derivation(parms, (delta[0], 0, 0))
		self.label_2 = 'y'
		grad[1] = self.calc_derivation(parms, (0, delta[1], 0))
		self.label_2 = 'r'
		grad[2] = self.calc_derivation(parms, (0, 0, delta[2]))
		
		grad_norm = math.sqrt(pow(grad[0], 2) + pow(grad[1], 2) + pow(grad[2], 2))
		
		sys.stderr.write('### Grad: ('+str(grad[0])+', '+str(grad[1])+', '+str(grad[2])+')\n')
		# init multiplier
		multiplier = 1
		if grad_norm > 5:
			multiplier = 5.0/grad_norm
		elif grad_norm > 0.000001 and grad_norm < 5:
			multiplier = 5.0/grad_norm

		sys.stderr.write('Init Multiplier:'+str(multiplier)+'\n')
		
		step = grad * multiplier
		sys.stderr.write('Step: ('+str(step[0])+', '+str(step[1])+', '+str(step[2])+')\n')
		new_parms = parms + step
		sys.stderr.write('New parms: centroid: ('+str(new_parms[0])+', '+str(new_parms[1])+'), radius: '+str(new_parms[2])+'\n')
		momentum = step * momentum_decay
		
		self.label_1 = 'Value(new)'
		self.label_2 = ''
		value_new = self.calc_value(parms + step, self.flg_calc_value)
		
		if value_new > value_old:
			parms = parms + step
			sys.stderr.write('centroid: ('+str(parms[0])+', '+str(parms[1])+'), radius: '+str(parms[2])+'\n')
			sys.stderr.write('Value: '+str(value_old)+' => '+str(value_new)+'\n')
			value_old = value_new
		else:
			sys.stderr.write('NA (Error: '+str(value_old)+' => '+str(value_new)+')\n')
			multiplier *= 0.9
			sys.stderr.write('Multiplier: ('+str(multiplier)+'\n')
		
		# temporary
		'''
		parms = parms + step
		result_parms = [0, 0, 0]
		result_parms[0] = int(parms[0]+0.5)
		result_parms[1] = int(parms[1]+0.5)
		result_parms[2] = int(parms[2]+0.5)
		self.parms = result_parms
		sys.stderr.write('centroid: ('+str(result_parms[0])+', '+str(result_parms[1])+'), radius: '+str(result_parms[2])+'\n')
		return result_parms
		'''
		
		self.loop += 1
		while self.loop < self.max_loop:
			#multiplier *= 0.9
			sys.stderr.write('---------- '+str(self.loop)+'-th run ---------------\n')
			#write('---------- '+str(self.loop)+'-th run ---------------\n')
			self.label_1 = 'Derivation'
			self.label_2 = 'x'
			grad[0] = self.calc_derivation(parms, (delta[0], 0, 0))
			self.label_2 = 'y'
			grad[1] = self.calc_derivation(parms, (0, delta[1], 0))
			self.label_2 = 'r'
			grad[2] = self.calc_derivation(parms, (0, 0, delta[2]))
			
			grad_norm = math.sqrt(pow(grad[0], 2) + pow(grad[1], 2) + pow(grad[2], 2))
			sys.stderr.write('### Grad: ('+str(grad[0])+', '+str(grad[1])+', '+str(grad[2])+')\n')
			#write('### Grad: (\t'+str(grad[0])+'\t'+str(grad[1])+'\t'+str(grad[2])+'\t)\n')

			step = grad * multiplier + momentum
			
			sys.stderr.write('Value_new: \n')
			value_new = self.calc_value(parms + step, self.flg_calc_value)
			'''
			while value_new < value_old:
				sys.stderr.write('NA (Error: '+str(value_old)+' => '+str(value_new)+')\n')
				multiplier *= 0.9
				sys.stderr.write('Multiplier: ('+str(multiplier)+'\n')
				step = grad * multiplier
				value_new = self.calc_value(parms + step)
				self.loop += 1
				if self.loop > self.max_loop:
					break
			'''
					
			sys.stderr.write('step: ('+str(step[0])+', '+str(step[1])+'), radius: '+str(step[2])+'\n')
			parms = parms + step
			momentum = step * momentum_decay
			
			self.label_1 = 'Value(new)'
			self.label_2 = ''
			value_new = self.calc_value(parms, self.flg_calc_value)
			
			sys.stderr.write('Value: '+str(value_old)+' => '+str(value_new)+'\n')
			sys.stderr.write('centroid: ('+str(parms[0])+', '+str(parms[1])+'), radius: '+str(parms[2])+'\n')
			#write('centroid: (\t'+str(parms[0])+'\t'+str(parms[1])+'\t), radius: \t'+str(parms[2])+'\n')
			
			value_old = value_new

			self.loop += 1
		
		result_parms = [0, 0, 0]
		result_parms[0] = int(parms[0]+0.5)
		result_parms[1] = int(parms[1]+0.5)
		result_parms[2] = int(parms[2]+0.5)
		self.parms = result_parms
		sys.stderr.write('centroid: ('+str(result_parms[0])+', '+str(result_parms[1])+'), radius: '+str(result_parms[2])+'\n')
		return result_parms
			
	# target: circle with centroid(=self.centroid) and radius(=self.radius)
	# Value(centroid, radius) = sum_{x,y}{val(x,y)*target(x,y)}
	# where target(x, y) = 1 (on circle), 0 (other)
	def calc_value(self, parms, flg):
		#sys.stderr.write('In calc_value\n')
				
		value_pos = 0
		value_neg = 0
		this_range = int(parms[2]*1.5+0.5)
		for dx0 in range(this_range*2):
			dx = dx0 - this_range
			x = parms[0] + dx
			for dy0 in range(this_range*2):
				dy = dy0 - this_range
				y = parms[1] + dy
				
				if x < 0 or y < 0 or x >= self.size_in[0] or y >= self.size_in[1]:
					continue
				r = int(math.sqrt(pow(dx, 2) + pow(dy, 2))+0.5)
				if r <= parms[2]:
					this_pixel = self.image_in.getpixel((x,y))
					value_pos += (this_pixel[0] + this_pixel[1] + this_pixel[2])*pow(r, 2)
				else:
					this_pixel = self.image_in.getpixel((x,y))
					value_neg += (this_pixel[0] + this_pixel[1] + this_pixel[2]) #*pow(r-parms[2], 2)
		
		'''
		for x in range(self.size_in[0]):
			for y in range(self.size_in[1]):
				# get target_value
				# target_value = get_target_value(parms)
				# value += (this_pixel[0] + this_pixel[1] + this_pixel[2]) * target_value
				r = int(0.5 + math.sqrt(pow(x-centroid[0], 2)+pow(y-centroid[1], 2)))
				if r == radius:
					this_pixel = self.image_in.getpixel((x,y))
					value += (this_pixel[0] + this_pixel[1] + this_pixel[2])
		'''
		if flg == 1:
			write('calc_value\t'+self.label_1+'\t'+self.label_2+'\t')
			write('parms:\t'+str(parms[0])+'\t'+str(parms[1])+'\t'+str(parms[2])+'\t')
			write('value\t'+str(value_pos)+'\t'+str(value_neg)+'\t'+str(parms[2]*parms[2]*3.14)+'\n')
		
		return(value_pos/parms[2]/parms[2] - value_neg)
	
	# {val(x+dx,y+dy, r+dr)-val(x-dx, y-dy, r-dr)}/2/delta
	def calc_derivation(self, parms, parms_delta):
		this_param = parms + parms_delta
		val_1 = self.calc_value(this_param, self.flg_calc_value)
		
		this_param = parms - parms_delta
		val_2 = self.calc_value(this_param, self.flg_calc_value)
		
		sys.stderr.write('-----\n')
		
		delta = 2 * math.sqrt(pow(parms[0], 2) + pow(parms[1], 2) + pow(parms[2], 2))

		derivation = (val_1 - val_2)/delta
		
		return derivation
		
		
	

def main():
	if len(sys.argv) < 2:
		sys.stderr.write('Usage: python $0 img_fname_in\n')
		sys.exit(1)
	
	img_fname_in = sys.argv[1]
	
	hd = get_shape(img_fname_in)
	
	parms = np.ones(3)
	hd.optimization(parms)
	
if __name__ == '__main__':
	main()


		