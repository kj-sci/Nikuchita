# -*- coding: utf-8 -*-

import sys
import cv2

write = sys.stdout.write

class img_handler_cv2:
	def __init__(self):
		self.img_fname_in = img_fname_in
		
	##########################################################################
	#                                                                        #
	#          Handler: Image_In                                             #
	#                                                                        #
	##########################################################################
	def read_img(self):
		self.image_in = cv2.imread(self.img_fname_in)
		

	def process(self):
		img = cv2.GaussianBlur(self.image_in,(3,3),0)
		 
		lap = cv2.Laplacian(img,cv2.CV_32F)
		 
		edge_lap = cv2.convertScaleAbs(lap)
		 
		cv2.imshow('edge_lap',edge_lap)
		cv2.waitKey(0)
		cv2.destroyAllWindows()


def main():
	if len(sys.argv) < 3:
		sys.stderr.write('Usage: python $0 img_fname(in) img_fname(out)\n')
		sys.exit(1)
	
	img_fname_in = sys.argv[1]
	img_fname_out = sys.argv[2]

	hd = img_handler_cv2(img_fname_in)
	hd.read_img()
	hd.process()
	
if __name__ == '__main__':
	main()


		