set img_dir=C:\Users\kfehvb1\Documents\Docs\private\Peechee\Moon_Comp\Final
set file_list=%img_dir%\file_list.txt

type %file_list% | python adjust_all_images.py

