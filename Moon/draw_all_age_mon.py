# -*- coding: utf-8 -*-

import sys
import draw_mon

write = sys.stdout.write

class draw_all_age_mon:
	def __init__(self, img_fname_out_0):
		self.img_fname_out_0 = img_fname_out_0
		
	def process(self):
		for age in range(30):
			if age < 9:
				img_fname_out = self.img_fname_out_0 + '_0' + str(age+1) + '.bmp'
			else:
				img_fname_out = self.img_fname_out_0 + '_' + str(age+1) + '.bmp'
			
			hd = draw_mon.draw_mon(age, img_fname_out)
			hd.process()

def main():
	if len(sys.argv) < 2:
		sys.stderr.write('Usage: python $0 img_fname0(out)\n')
		sys.exit(1)
	
	img_fname_out = sys.argv[1]
	
	hd = draw_all_age_mon(img_fname_out)
	hd.process()

	
if __name__ == '__main__':
	main()


		