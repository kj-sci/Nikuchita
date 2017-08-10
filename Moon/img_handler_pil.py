# -*- coding: utf-8 -*-

import sys
from PIL import Image
from PIL import ImageFilter

write = sys.stdout.write

class img_handler_pil:
	def __init__(self, img_fname_in):
		self.img_fname_in = img_fname_in
		self.pixel = [0,0,0] # (r,g,b)
		
	##########################################################################
	#                                                                        #
	#          Handler: Image_In                                             #
	#                                                                        #
	##########################################################################
	def read_img(self):
		self.image_in = Image.open(self.img_fname_in)
	
	def get_rgb_img(self):
		self.rgb_image_in = self.image_in.convert('RGB')
		self.size = self.rgb_image_in.size

	def get_pixel(self, x, y):
		self.pixel = self.image_in.getpixel((x,y))
		
	def show_img(self):
		self.image_in.show()
		
	def calc_centroid(self):
		self.centroid = [0,0]
		denom = 0
		for x in range(self.size[0]):
			for y in range(self.size[1]):
				self.pixel = self.rgb_image_in.getpixel((x,y))
				self.centroid[0] += x*(self.pixel[0] + self.pixel[1] + self.pixel[2])
				self.centroid[1] += y*(self.pixel[0] + self.pixel[1] + self.pixel[2])
				denom += (self.pixel[0] + self.pixel[1] + self.pixel[2])
		self.centroid[0] = int(self.centroid[0]/denom + 0.5)
		self.centroid[1] = int(self.centroid[1]/denom + 0.5)
		sys.stderr.write('Centroid: '+str(self.centroid[0])+', '+str(self.centroid[1])+'\n')
				
	##########################################################################
	#                                                                        #
	#          Handler: Image_Out                                            #
	#                                                                        #
	##########################################################################
	def make_new_image(self):
		self.image_out = Image.new('RGBA', self.size)
	
	def test(self):
		for x in range(self.size[0]):
			for y in range(self.size[1]):
				self.pixel = self.rgb_image_in.getpixel((x,y))
				self.image_out.putpixel((x,y), (self.pixel[0], self.pixel[1], self.pixel[2], 0))
	
		self.calc_centroid()
		for dx in range(10):
			for dy in range(10):
				self.image_out.putpixel((self.centroid[0]+dx,self.centroid[1]+dy), (255, 0, 0, 0))
		
	def put_pixel(self, x, y):
		self.image_out.putpixel((x,y), (self.pixel[0], self.pixel[1], self.pixel[2], 0))
		
	def save_image(self, img_fname_out):
		self.image_out.save(img_fname_out, 'bmp')
		
	##########################################################################
	#                                                                        #
	#                                                                        #
	#                                                                        #
	##########################################################################
	def filtering(self):
		self.image_out = self.image_in.filter(ImageFilter.FIND_EDGES)
	
	
	##########################################################################
	#                                                                        #
	#                                                                        #
	#                                                                        #
	##########################################################################
	

def main():
	if len(sys.argv) < 3:
		sys.stderr.write('Usage: python $0 img_fname(in) img_fname(out)\n')
		sys.exit(1)
	
	img_fname_in = sys.argv[1]
	img_fname_out = sys.argv[2]
	
	hd = img_handler_pil(img_fname_in)
	hd.read_img()
	#hd.get_rgb_img()
	#hd.make_new_image()
	#hd.test()
	hd.filtering()
	hd.save_image(img_fname_out)

	
if __name__ == '__main__':
	main()


		