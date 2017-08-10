REM set mon_date=20170711
REM set mon_no=6179
set mon_date=20170728
set mon_no=6266
set img_dir=C:\Users\kfehvb1\Documents\Docs\private\Peechee\Moon\%mon_date%
set img_fname_in=%img_dir%\IMG_%mon_no%.JPG
REM set img_fname_in=%img_dir%\DUMMY.BMP
set img_fname_out=%img_dir%\MON_%mon_no%_2.BMP
REM set img_fname_out=%img_dir%\DUMMY_OUT.BMP

python pretty-moon-data.py %img_fname_in% %img_fname_out%
