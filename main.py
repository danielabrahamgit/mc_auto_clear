from operator import pos
from re import A
import sys
import time
import numpy as np
import pyautogui
import matplotlib.pyplot as plt
from box_reader import get_dict_from_file, detect_boxes
from image_utils import get_values
from control import move_feadback, set_mining_angle, turn, move, set_torch
from pywinauto import Application, Desktop
from pywinauto.keyboard import send_keys

# Direction for turn right or left
right = True

# Minecraft toolbar (9 items)
toolbar = [
	'pick',
	'pick',
	'pick',
	'pick',
	'pick',
	'pick',
	'pick',
	'torch',
	'food',
	1
]

# Defines the area to clear out
x_max, z_min = -1047.3, 486
x_min, z_max = -1057.3, 496


if ( __name__ == "__main__" ):
	assert len(sys.argv) <= 2

	# Find minecraft window name
	mc_win_name = ''
	for w in Desktop(backend="uia").windows():
		w_text = w.window_text()
		if 'Minecraft' in w_text:
			mc_win_name = w_text
			break
	
	# Link python to minecraft 
	minecraft_handle = Application().connect(title_re=mc_win_name, class_name="GLFW30")
	main_window = minecraft_handle.top_window()
	
	# Handle mouse stuff
	rect = main_window.rectangle()
	xc = rect.width()//2
	yc = rect.height()//2 + 11

	
	# OCR setup
	if len(sys.argv) == 2:
		detect_boxes()

	pos_dict = get_dict_from_file()

	# -------------------------- MINING BEGIN -------------------------- 
	set_mining_angle(main_window, pos_dict, xc, yc)

	# for turns in range(3):
	# 	for torch_steps in range(2):
	# 		pyautogui.mouseDown(button='left')
	# 		move(7, main_window)
	# 		pyautogui.mouseUp(button='left')

	# 		set_torch(toolbar, main_window, pos_dict, xc, yc)

	# 	# Turn break two move in, turn again
	# 	if right:
	# 		turn('right', main_window, pos_dict, xc, yc)
	# 		pyautogui.mouseDown(button='left')
	# 		move(1, main_window)
	# 		pyautogui.mouseUp(button='left')
	# 		move(1, main_window)
	# 		turn('right', main_window, pos_dict, xc, yc)
	# 		right = False
	# 	else: 
	# 		turn('left', main_window, pos_dict, xc, yc)
	# 		pyautogui.mouseDown(button='left')
	# 		move(1, main_window)
	# 		pyautogui.mouseUp(button='left')
	# 		move(1, main_window)
	# 		turn('left', main_window, pos_dict, xc, yc)
	# 		right = True
	move_feadback(2, main_window, pos_dict)