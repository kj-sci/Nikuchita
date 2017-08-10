set img_dir=C:\Users\kfehvb1\Documents\Docs\private\Peechee\Moon
set img_fname_in=%img_dir%\IMG_6205.JPG
set img_fname_out=%img_dir%\TEST_6205.JPG

python img_handler_pil.py %img_fname_in% %img_fname_out%
REM python img_handler_cv2.py %img_fname_in% %img_fname_out%
