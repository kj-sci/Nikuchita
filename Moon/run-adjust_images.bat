set img_dir=C:\Users\kfehvb1\Documents\Docs\private\Peechee\Moon_Comp\Final
REM set img_dir=C:\Users\kfehvb1\Documents\Docs\private\Peechee\Dummy
REM #1
REM set file_name0_1=20170711_6180
REM set file_name0_2=20170712_6205
REM #2
set file_name0_1=20170712_6205_ADJ
set file_name0_2=20170713_6220

REM set img_fname_in_1=%img_dir%\upper.bmp
REM set img_fname_in_2=%img_dir%\left.bmp
REM set img_fname_out=%img_dir%\left_ADJ.BMP

REM set img_fname_in_1=%img_dir%\left.bmp
REM set img_fname_in_2=%img_dir%\left_2.bmp
REM set img_fname_out=%img_dir%\left_2_ADJ.BMP

set img_fname_in_1=%img_dir%\%file_name0_1%.BMP
set img_fname_in_2=%img_dir%\%file_name0_2%.BMP
set img_fname_out=%img_dir%\%file_name0_2%_ADJ.BMP

python adjust_images.py %img_fname_in_1% %img_fname_in_2% %img_fname_out%
