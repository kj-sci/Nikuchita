# -*- coding: utf-8 -*-

import sys
import adjust_image

write = sys.stdout.write

def main():
	base_dir = 'C:\\Users\\kfehvb1\\Documents\\Docs\\private\\Peechee\\Moon_Comp\\Final'
	header = sys.stdin.readline()
	
	for line in sys.stdin:
		if line[0] == '#':
			continue
			
		data = line[:-1].split('\t')
		sys.stderr.write(data[0]+' + '+data[1]+' => '+data[2]+'\n')
		
		fname_1 = base_dir + '\\' + data[0]
		fname_2 = base_dir + '\\' + data[1]
		fname_out = base_dir + '\\' + data[2]
		
		#write(fname_1+' + '+fname_2+' => '+fname_out+'\n')

		hd = adjust_image.adjust_image(fname_1, fname_2, fname_out)
		hd.process()
		
if __name__ == '__main__':
	main()


		