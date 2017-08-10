set mon_date=20170711
set mon_no=6179
REM set mon_date=20170728
REM set mon_no=6266
REM set img_dir=C:\Users\kfehvb1\Documents\Docs\private\Peechee\Moon\%mon_date%
set img_dir=C:\Users\kfehvb1\Documents\Docs\private\Peechee\Moon_Comp\Final

REM set img_fname_in=%img_dir%\MON_%mon_no%.BMP
set img_fname_in=%img_dir%\20170804_6338_ADJ.BMP
set img_fname_out=%img_dir%\20170804_6338_ADJ_2.BMP

python pretty-moon-data_new.py %img_fname_in% %img_fname_out%
